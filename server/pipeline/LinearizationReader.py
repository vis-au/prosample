from abc import ABC, abstractmethod
import numpy as np
import pathlib


class LinearizationReader(ABC):
    file_ending = ""

    def read_linearization(self, data_set_name):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_name = f"{data_set_name}{self.file_ending}"
        file_to_read = current_folder / "linearization_files" / file_name
        linearization = np.genfromtxt(file_to_read, skip_header=1, delimiter=";")
        return linearization


class LinearizationReaderTest(LinearizationReader):
    file_ending = "LinearizationTest.csv"


class LinearizationReaderZOrder(LinearizationReader):
    file_ending = "LinearizationZOrder.csv"


class LinearizationReaderNumeric(LinearizationReader):
    file_ending = "LinearizationSortByNumAttr.csv"


class LinearizationReaderTemporal(LinearizationReader):
    file_ending = "LinearizationSortByTempAttr.csv"


class LinearizationReaderNearestNeighbour(LinearizationReader):
    file_ending = "LinearizationNN.csv"


class LinearizationReaderStrip(LinearizationReader):
    file_ending = "LinearizationStrip.csv"


class LinearizationReaderRandom(LinearizationReader):
    file_ending = "LinearizationRandom.csv"

    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
