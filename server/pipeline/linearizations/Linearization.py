from abc import ABC, abstractmethod
import csv
import functools
import pathlib

import numpy as np
import pandas as pd
import pymorton as pm
from sklearn.neighbors import KDTree


class Linearization(ABC):
    def __init__(self, data_set_name, dimensions, exclude_attributes=[]):
        self.exclude_attributes = exclude_attributes
        self.data_set_name = data_set_name
        self.dimensions = dimensions
        self.linearization = None
        self.header = ""
        self.data = self.read_data()

    def read_data(self):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_to_read = (
            str(current_folder) + "/datasets/" + self.data_set_name + "Data.csv"
        )

        df = pd.read_csv(file_to_read, delimiter=";", header=None)
        df = df.drop(self.exclude_attributes, axis=1)
        data = df.to_numpy()

        data[:, 0] = np.array(range(0, len(data)))

        return data

    @abstractmethod
    def linearize(self):
        pass

    def write_data(self, linearization_type):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_name = self.data_set_name + "Linearization" + linearization_type + ".csv"
        file_name = str(current_folder) + "/../linearization_files/" + file_name
        pd.DataFrame(self.linearization).to_csv(
            file_name, sep=";", header=False, index=False
        )
        print(f"Saved linearized data in {file_name}")


class LinearizationRandom(Linearization):
    def linearize(self):
        order = np.argsort(np.random.rand(len(self.data)))
        self.linearization = self.data[order]
        self.write_data("Random")
        return self.linearization


class LinearizationNumericAttr(Linearization):
    def __init__(
        self, data_set_name, dimensions, sort_attr: int, exclude_attributes=[]
    ):
        super().__init__(data_set_name, dimensions, exclude_attributes)
        self.sort_attr = sort_attr

    def linearize(self):
        order = np.argsort(self.data[:, self.sort_attr])
        self.linearization = self.data[order]
        self.write_data("SortByNumAttr")
        return self.linearization


class LinearizationDatetimeAttr(LinearizationNumericAttr):
    def linearize(self):
        attr = self.data[:, self.sort_attr].astype(np.datetime64)
        attr_datetime = pd.to_datetime(attr)
        order = np.argsort(attr_datetime)
        self.linearization = self.data[order]
        self.write_data("SortByTempAttr")
        return self.linearization


class LinearizationZOrder2D(Linearization):
    def linearize(self):
        mins, maxs = self.find_extrema()
        diffs = maxs - mins
        normalized_data = (self.data - mins) / diffs

        indexes = self.construct_z_order_2d(
            list(range(len(normalized_data))), normalized_data[:, 1:3]
        )

        self.linearization = self.data[indexes]
        self.write_data("ZOrder")

    def find_extrema(self):
        data_dimension = len(self.data[0])
        mins = np.full(data_dimension, float("inf"))
        maxs = np.full(data_dimension, float("-inf"))

        for data_point in self.data:
            for attribute_index in range(data_dimension):
                attribute = data_point[attribute_index]
                if attribute < mins[attribute_index]:
                    mins[attribute_index] = attribute
                if attribute > maxs[attribute_index]:
                    maxs[attribute_index] = attribute

        return mins, maxs

    def construct_z_order_2d(self, indexes, data):
        def compare(i, j):
            if data[i][0] == data[j][0] and data[i][1] == data[j][1]:
                return 0
            ixbin, iybin = "", ""
            jxbin, jybin = "", ""
            xl, xr, yl, yr = 0, 1, 0, 1
            while ixbin == jxbin and iybin == jybin:
                xm = (xl + xr) / 2
                ym = (yl + yr) / 2
                if data[i][0] > xm:
                    ixbin += "1"
                else:
                    ixbin += "0"
                if data[j][0] > xm:
                    jxbin += "1"
                else:
                    jxbin += "0"

                if data[i][1] > ym:
                    iybin += "1"
                else:
                    iybin += "0"
                if data[j][1] > ym:
                    jybin += "1"
                else:
                    jybin += "0"

                if ixbin[-1] == "1":
                    xl = xm
                else:
                    xr = xm

                if iybin[-1] == "1":
                    yl = ym
                else:
                    yr = ym

            ipos = "".join("".join(x) for x in zip(iybin, ixbin))
            jpos = "".join("".join(x) for x in zip(jybin, jxbin))

            if ipos < jpos:
                return -1
            else:
                return 1

        indexes.sort(key=functools.cmp_to_key(compare))
        return np.array(indexes)


class LinearizationZOrderKD(Linearization):
    def linearize(self):
        mins, maxs = self.find_extrema()
        diffs = maxs - mins
        normalized_data = (self.data - mins) / diffs

        indexes = self.construct_z_order_kd(
            list(range(len(normalized_data))),
            normalized_data[:, 1 : self.dimensions + 1],
        )

        self.linearization = self.data[indexes]
        self.write_data("ZOrder")

    def find_extrema(self):
        data_dimension = len(self.data[0])
        mins = np.full(data_dimension, float("inf"))
        maxs = np.full(data_dimension, float("-inf"))

        for data_point in self.data:
            for attribute_index in range(data_dimension):
                attribute = data_point[attribute_index]
                if attribute < mins[attribute_index]:
                    mins[attribute_index] = attribute
                if attribute > maxs[attribute_index]:
                    maxs[attribute_index] = attribute

        return mins, maxs

    def construct_z_order_kd(self, indexes, data):
        def compare(i, j):
            dimensions = self.dimensions
            if np.equal(data[i], data[j]).all():
                return 0

            ipos = [""] * dimensions
            jpos = [""] * dimensions

            leftBounds = np.full(dimensions, 0.0)
            rightBounds = np.full(dimensions, 1.0)

            while ipos == jpos:
                mids = (leftBounds + rightBounds) / 2
                for dim in range(dimensions):
                    if data[i][dim] > mids[dim]:
                        ipos[dim] += "1"
                    else:
                        ipos[dim] += "0"
                    if data[j][dim] > mids[dim]:
                        jpos[dim] += "1"
                    else:
                        jpos[dim] += "0"

                for dim in range(dimensions):
                    if ipos[dim][-1] == "1":
                        leftBounds[dim] = mids[dim]
                    else:
                        rightBounds[dim] = mids[dim]

            izip = zip(*ipos[::-1])
            jzip = zip(*jpos[::-1])
            iposition = "".join("".join(x) for x in izip)
            jposition = "".join("".join(x) for x in jzip)
            if iposition < jposition:
                return -1
            else:
                return 1

        indexes.sort(key=functools.cmp_to_key(compare))
        return np.array(indexes)


class LinearizationNearestNeighbour(Linearization):
    def linearize(self):
        data_dim = self.data[:, 1 : self.dimensions + 1]
        indexes = self.construct_nn_order_kd(data_dim)

        self.linearization = self.data[indexes]
        self.write_data("NN")

    def construct_nn_order_kd(self, data):
        no_of_points = len(data)
        visited = np.full(no_of_points, False)

        indexes = np.full(no_of_points, None)

        current_index = 0  # <-- Hardcoded (0)

        indexes[0] = current_index
        counter = 1

        no_of_neighbours = 50  # <-- Hardcoded (50)
        kdt = KDTree(
            data, leaf_size=30, metric="euclidean"
        )  # <-- Hardcoded (euclidean)
        neighbours = kdt.query(data, k=no_of_neighbours, return_distance=False)

        for iter in range(no_of_points - 1):
            current_neighbours = neighbours[current_index]

            found = False
            for close in current_neighbours:
                if not visited[close] and not close == current_index:
                    found = True
                    visited[close] = True
                    indexes[counter] = close
                    counter += 1
                    current_index = close
                    break

            if not found:
                current_point = data[current_index]
                all_neighbours = kdt.query(
                    current_point.reshape(1, -1), k=no_of_points, return_distance=False
                )
                for close in all_neighbours[0]:
                    if not visited[close] and not close == current_index:
                        visited[close] = True
                        indexes[counter] = close
                        counter += 1
                        current_index = close
                        break

        return indexes.astype(int)


class LinearizationGeoZorder(Linearization):
    def __init__(
        self, data_set_name, dimensions, lat: int, lng: int, exclude_attributes=[]
    ):
        super().__init__(data_set_name, dimensions, exclude_attributes)
        self.lat = lat  # attribute containing latitude
        self.lng = lng  # attribute containing longitude

    def linearize(self):
        # this generates a hash for every element of the data, and sorting by that hash gives
        # the zorder of the data
        hashes = pd.DataFrame(self.data).apply(
            lambda row: pm.interleave_latlng(row[self.lat], row[self.lng]), axis=1
        )
        order = np.argsort(hashes)
        self.linearization = self.data[order]
        self.write_data("ZOrder")  # same as non-spatial z-order
        return self.linearization
