from abc import ABC, abstractmethod
import numpy as np
from sklearn.utils.random import sample_without_replacement


class Subdivision(ABC):
    def load_linearization(self, linearization):
        self.linearization = linearization

    @abstractmethod
    def subdivide(self):
        pass


class SubdivisionCardinality(Subdivision):
    sampling_rate = 0

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def subdivide(self):
        bucket_size = int(len(self.linearization) / self.chunk_size)
        no_of_points = len(self.linearization)
        subdivision = {}
        division_number = 0
        for i in range(0, no_of_points, bucket_size):
            next_division = self.linearization[i : i + bucket_size]
            subdivision[division_number] = next_division
            division_number += 1
        return subdivision


class SubdivisionRandom(Subdivision):
    def __init__(self, n_bins: int) -> None:
        super().__init__()
        self.n_bins = n_bins

    def subdivide(self):
        subdivision = {}

        # generate n_bins indeces to split up the linearized data
        bin_edges = sample_without_replacement(
            n_population=len(self.linearization), n_samples=self.n_bins, random_state=0
        )
        bin_edges = bin_edges[np.argsort(bin_edges)]

        for i in range(self.n_bins):
            if i == 0:
                first = 0
                last = bin_edges[i]
                subdivision[i] = self.linearization[first : last + 1]
            elif i == self.n_bins - 1:
                first = bin_edges[i - 1]
                last = -1
                subdivision[i] = self.linearization[first + 1 :]
            else:
                first = bin_edges[i - 1]
                last = bin_edges[i]
                subdivision[i] = self.linearization[first + 1 : last + 1]

        # throw out empty bins (can happen when two edges are right after each one another)
        for i in range(self.n_bins):
            if len(subdivision[i]) == 0:
                del subdivision[i]

        return subdivision


class SubdivisionCohesion(Subdivision):
    def __init__(self, attributes: list[int], n_bins: int) -> None:
        super().__init__()
        self.attributes = attributes
        self.n_bins = n_bins

    def subdivide(self):
        subdivision = {}

        # find the n_bins biggest jumps in the data along the attribute column
        X = self.linearization[:, self.attributes].astype(np.float64)

        # creates a copy of X where rows are shifted by 1 for faster subtraction
        X_ = np.empty_like(X)
        X_[:-1] = X[1:]
        X_[-1] = X[0]

        X_jump = np.linalg.norm(X - X_, axis=1)  # computes euclidean distance
        biggest_jump_indeces = np.argsort(X_jump)[
            -self.n_bins - 1 :
        ]  # one larger than n_bins

        for i in range(self.n_bins):
            if i == 0:
                first = 0
                last = biggest_jump_indeces[i]
                subdivision[i] = self.linearization[first : last + 1]
            elif i == self.n_bins - 1:
                first = biggest_jump_indeces[i - 1]
                last = -1
                subdivision[i] = self.linearization[first + 1 :]
            else:
                first = biggest_jump_indeces[i - 1]
                last = biggest_jump_indeces[i]
                subdivision[i] = self.linearization[first + 1 : last + 1]

        # throw out empty bins (can happen when two jumps are right after each one another)
        for i in range(self.n_bins):
            if len(subdivision[i]) == 0:
                del subdivision[i]
        return subdivision


class SubdivisionCoverage(Subdivision):
    attribute: int = -1
    low_quantile: float = 0.05
    high_quantile: float = 0.95

    def __init__(self, attribute: int, low_quantile: float = 0, high_quantile: float = 1):
        super().__init__()
        self.attribute = attribute
        self.low_quantile = low_quantile
        self.high_quantile = high_quantile

    def subdivide(self):
        subdivision = {}

        X = self.linearization[:, self.attribute]

        # find all instances outside the 0.05 quantiles
        low_value = np.quantile(X, self.low_quantile)
        high_value = np.quantile(X, self.high_quantile)

        is_low = X < low_value
        is_high = X > high_value

        # divide the data into bins that contain both the "min" and the "max"
        bin_edge_indeces = []

        bin_has_low = True
        bin_has_high = True

        # detect bin edges, i.e., every time a low and a high value lie on the same segment
        for i in range(len(X)):
            bin_has_low = bin_has_low or is_low[i]
            bin_has_high = bin_has_high or is_high[i]

            if bin_has_low and bin_has_high:
                bin_edge_indeces += [i]
                bin_has_low = False
                bin_has_high = False

        # put all items into their bins
        bin_edge_indeces = sorted(bin_edge_indeces)
        previous_index = 0
        for i, edge_index in enumerate(bin_edge_indeces):
            # avoid creating empty bins
            if len(self.linearization[previous_index:edge_index]) == 0:
                continue

            subdivision[i] = self.linearization[previous_index:edge_index]
            previous_index = edge_index

        # create a bin for the remaining items "after" the last bin edge
        subdivision[len(bin_edge_indeces)] = self.linearization[previous_index:]

        return subdivision


class SubdivisionInterval(Subdivision):
    def __init__(self, chunk_size: int, attribute: int) -> None:
        super().__init__()
        self.chunk_size = chunk_size
        self.attribute = attribute

    def subdivide(self):
        # NOTE: this subdivision requires that the data was sorted by self.attribute in the
        # linearization step, otherwise it re-sorts the input (breaking the linearization idea)
        subdivision = {}

        X = self.linearization[:, self.attribute]

        # assigns a label (i.e., a bin) along every attribute
        y = np.digitize(X, bins=np.histogram(X, bins=self.chunk_size)[1])

        for label in np.unique(y):
            subdivision[label] = self.linearization[y == label]

        return subdivision
