from abc import ABC, abstractmethod
from typing import List
import random
import itertools
import numpy as np


class Selection(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.steer()

    def steer(self, dimension: int = None, min_value: int = 0, max_value: int = 1):
        self.steering = {
            "dimension": int(dimension) if dimension is not None else dimension,
            "min_value": float(min_value),
            "max_value": float(max_value)
        }

    def clear_steering(self):
        self.steering["dimension"] = None

    def load_subdivision(self, subdivision):
        self.subdivision = subdivision

    def is_steered_subspace_empty(self):
        # FIXME: this is a sinful hack, compacting all items into a numpy array to make queries fast
        all_items = np.array(list(itertools.chain.from_iterable(list(self.subdivision.values()))))

        dim = self.steering["dimension"]
        min_value = self.steering["min_value"]
        max_value = self.steering["max_value"]
        check = (all_items[:, dim] >= min_value) & (all_items[:, dim] <= max_value)
        is_empty = check.sum() == 0

        return is_empty

    def get_indeces_matching_steering_in_bucket(self, bucket_index: int) -> List[int]:
        dim = self.steering["dimension"]
        bucket = np.array(self.subdivision[bucket_index])[:, dim]

        min_value = self.steering["min_value"]
        max_value = self.steering["max_value"]
        matches_query = (bucket >= min_value) & (bucket <= max_value)

        # use the 0 index below, because nonzero() gets indeces, but returns a tuple
        indeces = matches_query.nonzero()[0].tolist()
        return indeces

    def create_steered_chunk(self, chunk_size: int) -> np.ndarray:
        # proof-of-concept: steering means that we can prioritize data along ONE dimension in the
        # data. Thus, we go through all subdivision and collect items that match the steering
        # condition, until we have `chunk_size` items
        steered_chunk = []
        buckets = self.subdivision.copy()

        matches_query_tuples = []

        for b in buckets:
            matching_indeces = self.get_indeces_matching_steering_in_bucket(b)

            for matching_index in matching_indeces:
                matches_query_tuples += [(b, matching_index)]

        actual_chunk_size = min(chunk_size, len(matches_query_tuples))

        # add the number of matching items, but at most chunk_size items to the steered chunk
        for i in range(0, actual_chunk_size):
            b, matching_index = matches_query_tuples[i]
            steered_chunk += [buckets[b][matching_index]]
            buckets[b][matching_index] = None  # set flag for deletion

        for b in buckets:
            self.subdivision[b] = [
                item for item in buckets[b] if item is not None
            ]

            # delete the entire bucket if it's empty
            if len(self.subdivision[b]) == 0:
                del self.subdivision[b]

        steered_chunk = [c for c in steered_chunk if c is not None]
        return np.array(steered_chunk)

    def next_chunk(self) -> np.ndarray:
        # If the first subdivision is empty, None is returned
        if len(self.subdivision) == 0:
            return None
        first_key = next(iter(self.subdivision))
        data_dimension = len(self.subdivision[first_key][0])
        chunk = np.full((len(self.subdivision), data_dimension), None)
        chunk_index = 0

        # this is a simple extension for enabling steering: check if steering parameters are set,
        # if that steering subspace is not empty and then sample from there, otherwise use the
        # default strategy for selecting
        if self.steering["dimension"] is not None:
            if not self.is_steered_subspace_empty():
                print("using steering ...")
                # use number of buckets as chunk size
                chunk = self.create_steered_chunk(len(self.subdivision))
                return chunk

        keys = self.subdivision.copy()
        for i in keys:
            next_index = self.select_element(chunk, chunk_index, i)
            chunk_index += 1
            del self.subdivision[i][next_index]
            if len(self.subdivision[i]) == 0:
                del self.subdivision[i]
        return chunk

    # Selects from bucket bucket_number, expands chunk at index chunk_index with it and returns
    # which index was selected
    @abstractmethod
    def select_element(self, chunk, chunk_index, bucket_number) -> int:
        pass


class SelectionRandom(Selection):

    def __init__(self, seed=0):
        super().__init__()
        self.seed = seed

    def select_element(self, chunk, chunk_index, bucket_number):
        subdivision_size = len(self.subdivision[bucket_number])
        random.seed(self.seed + chunk_index)
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
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        min_indexes = np.array(self.subdivision[bucket_number]).argmin(axis=0)  # <-- Slow
        min_index = min_indexes[self.attribute]
        chunk[chunk_index] = self.subdivision[bucket_number][min_index]
        return min_index


class SelectionMaximum(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        max_indexes = np.array(self.subdivision[bucket_number]).argmax(axis=0)  # <-- Slow
        max_index = max_indexes[self.attribute]
        chunk[chunk_index] = self.subdivision[bucket_number][max_index]
        return max_index


class SelectionMedian(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, chunk_index, bucket_number):
        subdivision_size = len(self.subdivision[bucket_number])
        median_index = np.argsort(np.array(self.subdivision[bucket_number])[:, 3])[int(subdivision_size / 2)]  # <-- Slow
        chunk[chunk_index] = self.subdivision[bucket_number][median_index]
        return median_index
