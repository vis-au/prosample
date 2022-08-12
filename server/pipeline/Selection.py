from abc import ABC, abstractmethod
from typing import List
import random
import itertools
import numpy as np
from sklearn.utils.random import sample_without_replacement


class Selection(ABC):
    chunk_counter = 0  # used for seeding randomness

    def __init__(self, random_state=0) -> None:
        super().__init__()
        self.steering_filters = {}  # a dict mapping a steered dimension to a min-max filter.
        self.random_state = random_state  # used for seeding randomness

    def steer(self, dimension: int = None, min_value: int = 0, max_value: int = 1):
        steering_filter = {
            "min_value": float(min_value),
            "max_value": float(max_value)
        }
        self.steering_filters[dimension] = steering_filter

    def clear_steering(self):
        self.steering_filters = {}

    def load_subdivision(self, subdivision):
        self.subdivision = subdivision

    def is_steered_subspace_empty(self):
        # FIXME: this is a sinful hack, compacting all items into a numpy array for "fast" checking
        all_items = np.array(list(itertools.chain.from_iterable(list(self.subdivision.values()))))
        check = np.full(len(all_items), True)  # boolean index indicating items matching steering

        for dim in self.steering_filters:
            min_value = self.steering_filters[dim]["min_value"]
            max_value = self.steering_filters[dim]["max_value"]
            dim = int(dim)
            check = (all_items[:, dim] >= min_value) & (all_items[:, dim] <= max_value) & check

        is_empty = check.sum() == 0
        return is_empty

    def get_indeces_matching_steering_in_bucket(self, bucket_index: int) -> List[int]:
        bucket = np.array(self.subdivision[bucket_index])
        check = np.full(len(bucket), True)  # boolean index indiciating items matching steering

        for dim in self.steering_filters:
            min_value = self.steering_filters[dim]["min_value"]
            max_value = self.steering_filters[dim]["max_value"]
            values = bucket[:, int(dim)]
            check = (values >= min_value) & (values <= max_value) & check

        # use the 0 index below, because nonzero() gets indeces, but returns a tuple
        indeces = check.nonzero()[0].tolist()
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

    def next_chunk(self, chunk_size: int = -1) -> np.ndarray:
        # If the first subdivision is empty, None is returned
        if len(self.subdivision) == 0:
            return None

        first_key = next(iter(self.subdivision))  # iterator over the subdivision bins
        data_dimension = len(self.subdivision[first_key][0])

        chunk_size = chunk_size if chunk_size > -1 else len(self.subdivision)
        chunk = np.full((chunk_size, data_dimension), None)

        # this is a simple extension for enabling steering: check if steering parameters are set,
        # if that steering subspace is not empty and then sample from there, otherwise use the
        # default strategy for selecting
        if len(self.steering_filters.keys()) > 0:
            if not self.is_steered_subspace_empty():
                print("using steering ...")
                # use number of buckets as chunk size
                chunk = self.create_steered_chunk(chunk_size)
                return chunk

        # seed any randomness in the selections
        random.seed(self.random_state + self.chunk_counter)
        self.chunk_counter += 1

        pos_in_chunk = 0
        while pos_in_chunk < chunk_size:
            bucket_keys = list(self.subdivision.copy().keys())

            # prevent ordering bias when chunk_size is bigger than number of bins
            random.shuffle(bucket_keys)

            for bucket_key in bucket_keys:
                if pos_in_chunk >= chunk_size:
                    break
                next_index = self.select_element(chunk, pos_in_chunk, bucket_key)
                pos_in_chunk += 1
                del self.subdivision[bucket_key][next_index]
                if len(self.subdivision[bucket_key]) == 0:
                    del self.subdivision[bucket_key]
        return chunk

    # Selects from bucket bucket_key, expands chunk at index pos_in_chunk with it and returns
    # which index was selected
    @abstractmethod
    def select_element(self, chunk: np.ndarray, pos_in_chunk: int, bucket_key: str or int) -> int:
        pass

    # Same as select_element, but selects multiple items per run
    @abstractmethod
    def select_elements(
        self, n_elements: int, chunk: np.ndarray, pos_in_chunk: int, bucket_key: int
    ) -> int:
        pass


class SelectionRandom(Selection):

    def select_element(self, chunk, pos_in_chunk, bucket_index):
        subdivision_size = len(self.subdivision[bucket_index])
        next_index = random.randint(0, subdivision_size - 1)
        chunk[pos_in_chunk] = self.subdivision[bucket_index][next_index]
        return next_index

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        subdivision_size = len(self.subdivision[bucket_key])
        indeces = sample_without_replacement(
            n_population=subdivision_size,
            n_samples=n_elements,
            random_state=random.randint(0, subdivision_size - 1)
        )
        chunk[pos_in_chunk: pos_in_chunk + n_elements] = self.subdivision[bucket_key][indeces]
        return indeces


class SelectionFirst(Selection):

    def select_element(self, chunk, pos_in_chunk, bucket_key):
        next_index = 0
        chunk[pos_in_chunk] = self.subdivision[bucket_key][next_index]
        return next_index

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        indeces = range(0, n_elements)
        chunk[pos_in_chunk: pos_in_chunk + n_elements] = self.subdivision[bucket_key][indeces]
        return indeces


class SelectionMinimum(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, pos_in_chunk, bucket_key):
        min_indexes = np.array(self.subdivision[bucket_key]).argmin(axis=0)  # <-- Slow
        min_index = min_indexes[self.attribute]
        chunk[pos_in_chunk] = self.subdivision[bucket_key][min_index]
        return min_index

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        sorted_indeces = self.subdivision[bucket_key][:, self.attribute].argsort(axis=0)
        n_min_indeces = np.argpartition(sorted_indeces, n_elements)[:n_elements]
        chunk[pos_in_chunk: pos_in_chunk + n_elements] = self.subdivision[bucket_key][n_min_indeces]
        return n_min_indeces


class SelectionMaximum(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, pos_in_chunk, bucket_key):
        max_indexes = np.array(self.subdivision[bucket_key]).argmax(axis=0)  # <-- Slow
        max_index = max_indexes[self.attribute]
        chunk[pos_in_chunk] = self.subdivision[bucket_key][max_index]
        return max_index

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        sorted_indeces = self.subdivision[bucket_key][:, self.attribute].argsort(axis=0)
        n_min_indeces = np.argpartition(sorted_indeces, -n_elements)[-n_elements:]
        chunk[pos_in_chunk: pos_in_chunk + n_elements] = self.subdivision[bucket_key][n_min_indeces]
        return n_min_indeces


class SelectionMedian(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def select_element(self, chunk, pos_in_chunk, bucket_key):
        subdivision_size = len(self.subdivision[bucket_key])
        med = int(subdivision_size / 2)
        median_index = np.argsort(np.array(self.subdivision[bucket_key])[:, 3])[med]  # <-- Slow
        chunk[pos_in_chunk] = self.subdivision[bucket_key][median_index]
        return median_index

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        sorted_indeces = self.subdivision[bucket_key][:, self.attribute].argsort(axis=0)

        # the central element in sorted_indeces is the index of the "median" in the bucket
        center_pos = len(sorted_indeces) // 2

        # padding around the center position. If even number of elements is returned, right end
        # of the window is bigger than left end by 1
        pad_left = (n_elements - 1) // 2
        pad_right = (n_elements - 1) // 2 if n_elements % 2 == 0 else n_elements // 2

        # as a heuristic, get n/2 elements before and after that element as "medians"
        if len(self.subdivision[bucket_key]) < n_elements:
            # if less than n_elements in bucket, just return all elements in bucket
            n_median_indeces = np.arange(0, len(self.subdivision[bucket_key]))
        else:
            # otherwise us a window centered around center_pos
            n_median_indeces = np.arange(center_pos - pad_left, center_pos + pad_right)

        chunk[pos_in_chunk:pos_in_chunk+n_elements] = self.subdivision[bucket_key][n_median_indeces]
        return n_median_indeces
