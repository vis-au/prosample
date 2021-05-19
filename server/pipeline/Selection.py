from abc import ABC, abstractmethod
import numpy as np
import random


class Selection(ABC):

    def load_subdivision(self, subdivision):
        self.subdivision = subdivision

    @abstractmethod
    def next_chunk(self):
        pass


class SelectionRandom(Selection):

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision[0]) == 0:
            return None
        data_dimension = len(self.subdivision[0][0])                    # <-- Problem if first list is empty
        chunk = np.full((len(self.subdivision), data_dimension), None)
        for i in range(0, len(self.subdivision)):
            subdivision_size = len(self.subdivision[i])
            if subdivision_size > 0:
                next_index = random.randint(0, subdivision_size - 1)
                chunk[i] = self.subdivision[i][next_index]
                del self.subdivision[i][next_index]
        return chunk


class SelectionFirst(Selection):

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision[0]) == 0:
            return None
        data_dimension = len(self.subdivision[0][0])                    # <-- Problem if first list is empty
        chunk = np.full((len(self.subdivision), data_dimension), None)
        for i in range(0, len(self.subdivision)):
            subdivision_size = len(self.subdivision[i])
            if subdivision_size > 0:
                next_index = 0
                chunk[i] = self.subdivision[i][next_index]
                del self.subdivision[i][next_index]
        return chunk


class SelectionMinimum(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision[0]) == 0:
            return None
        data_dimension = len(self.subdivision[0][0])                    # <-- Problem if first list is empty
        chunk = np.full((len(self.subdivision), data_dimension), None)
        for i in range(0, len(self.subdivision)):
            subdivision_size = len(self.subdivision[i])
            if subdivision_size > 0:
                min_index = np.array(self.subdivision[i]).argmin(axis=0)        # <-- Slow (converts every subdivision list to numpy array)
                chunk[i] = self.subdivision[i][min_index[self.attribute]]
                del self.subdivision[i][min_index[self.attribute]]
        return chunk


class SelectionMaximum(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision[0]) == 0:
            return None
        data_dimension = len(self.subdivision[0][0])                    # <-- Problem if first list is empty
        chunk = np.full((len(self.subdivision), data_dimension), None)
        for i in range(0, len(self.subdivision)):
            subdivision_size = len(self.subdivision[i])
            if subdivision_size > 0:
                max_index = np.array(self.subdivision[i]).argmax(axis=0)        # <-- Slow (converts every subdivision list to numpy array)
                chunk[i] = self.subdivision[i][max_index[self.attribute]]
                del self.subdivision[i][max_index[self.attribute]]
        return chunk


class SelectionMedian(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision[0]) == 0:
            return None
        data_dimension = len(self.subdivision[0][0])                        # <-- Problem if first list is empty
        chunk = np.full((len(self.subdivision), data_dimension), None)
        for i in range(0, len(self.subdivision)):
            subdivision_size = len(self.subdivision[i])
            if subdivision_size > 0:
                median_index = np.argsort(np.array(self.subdivision[i])[:, 3])[int(subdivision_size / 2)]   # <-- Slow
                chunk[i] = self.subdivision[i][median_index]
                del self.subdivision[i][median_index]
        return chunk
