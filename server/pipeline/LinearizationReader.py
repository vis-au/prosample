from abc import ABC, abstractmethod
import numpy as np
import pathlib


class LinearizationReader(ABC):

    @abstractmethod
    def read_linearization(self, data_set_name):
        pass


class LinearizationReaderZOrder(LinearizationReader):

    def read_linearization(self, data_set_name):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_to_read = current_folder / 'linearization_files' / (data_set_name + 'LinearizationZOrder.csv')
        linearization = np.genfromtxt(file_to_read, skip_header=1, delimiter=';')
        return linearization


class LinearizationReaderNearestNeighbour(LinearizationReader):

    def read_linearization(self, data_set_name):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_to_read = current_folder / 'linearization_files' / (data_set_name + 'LinearizationNN.csv')
        linearization = np.genfromtxt(file_to_read, skip_header=1, delimiter=';')
        return linearization


class LinearizationReaderStrip(LinearizationReader):

    def read_linearization(self, data_set_name):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_to_read = current_folder / 'linearization_files' / (data_set_name + 'LinearizationStrip.csv')
        linearization = np.genfromtxt(file_to_read, skip_header=1, delimiter=';')
        return linearization


class LinearizationReaderRandom(LinearizationReader):

    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)

    def read_linearization(self, data_set_name):
        current_folder = pathlib.Path(__file__).parent.absolute()
        file_to_read = current_folder / 'linearization_files' / (data_set_name + 'LinearizationZOrder.csv')
        linearization = np.genfromtxt(file_to_read, skip_header=1, delimiter=';')
        np.random.shuffle(linearization)
        return linearization
