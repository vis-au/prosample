from abc import ABC, abstractmethod
import numpy as np
import random


class Selection(ABC):

    def load_subdivision(self, subdivision):
        self.subdivision = subdivision

    def next_chunk(self):
        # If the first subdivision is empty, None is returned
        if len(self.subdivision) == 0:
            return None
        first_key = next(iter(self.subdivision))
        data_dimension = len(self.subdivision[first_key][0])
        chunk = np.full((len(self.subdivision), data_dimension), None)
        chunk_index = 0
        keys = self.subdivision.copy()
        for i in keys:
            next_index = self.select_element(chunk, chunk_index, i)
            chunk_index += 1
            del self.subdivision[i][next_index]
            if len(self.subdivision[i]) == 0:
                del self.subdivision[i]
        return chunk

    # Selects from bucket bucket_number, expands chunk at index chunk_index with it and returns which index was selected
    @abstractmethod
    def select_element(self, chunk, chunk_index, bucket_number):
        pass


class SelectionRandom(Selection):

    def __init__(self, seed=1):
        if seed is not None:
            random.seed(seed)

    def select_element(self, chunk, chunk_index, bucket_number):
        subdivision_size = len(self.subdivision[bucket_number])
        next_index = random.randint(0, subdivision_size - 1)
        chunk[chunk_index] = self.subdivision[bucket_number][next_index]
        return next_index


class SelectionFirst(Selection):

    def select_element(self, chunk, chunk_index, bucket_number):
        next_index = 0
        chunk[chunk_index] = self.subdivision[bucket_number][next_index]
        return next_index


class SelectionMinimum(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        min_indexes = np.array(self.subdivision[bucket_number]).argmin(axis=0)  # <-- Slow
        min_index = min_indexes[self.attribute]
        chunk[chunk_index] = self.subdivision[bucket_number][min_index]
        return min_index


class SelectionMaximum(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        max_indexes = np.array(self.subdivision[bucket_number]).argmax(axis=0)  # <-- Slow
        max_index = max_indexes[self.attribute]
        chunk[chunk_index] = self.subdivision[bucket_number][max_index]
        return max_index


class SelectionMedian(Selection):
    attribute = 0

    def __init__(self, attribute):
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        subdivision_size = len(self.subdivision[bucket_number])
        median_index = np.argsort(np.array(self.subdivision[bucket_number])[:, 3])[int(subdivision_size / 2)]  # <-- Slow
        chunk[chunk_index] = self.subdivision[bucket_number][median_index]
        return median_index
