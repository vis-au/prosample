from abc import ABC, abstractmethod
from typing import List
import time
import random
import itertools
import numpy as np
from sklearn.utils.random import sample_without_replacement


class Selection(ABC):
    chunk_counter = 0  # used for seeding randomness

    def __init__(self, random_state=0) -> None:
        super().__init__()
        self.steering_filters = (
            {}
        )  # a dict mapping a steered dimension to a min-max filter.
        self.random_state = random_state  # used for seeding randomness

    def steer(self, dimension: int = None, min_value: int = 0, max_value: int = 1):
        steering_filter = {"min_value": float(min_value), "max_value": float(max_value)}
        self.steering_filters[dimension] = steering_filter

    def clear_steering(self):
        self.steering_filters = {}

    def load_subdivision(self, subdivision):
        self.subdivision = subdivision

    def _load_subdivision_sorted(self, subdivision, attribute: int):
        """Auxilary function for subdivsions that select elements based on some order in the bucket.
        Rather than sorting the buckets before each selection, this function sorts the data once.
        This is done for performance reasons."""
        _subdivision = {}

        bucket_keys = list(subdivision.copy().keys())
        for bucket_key in bucket_keys:
            bucket = np.array(subdivision[bucket_key])
            _subdivision[bucket_key] = bucket[bucket[:, attribute].argsort(axis=0)]

        self.subdivision = _subdivision

    def is_steered_subspace_empty(self):
        # FIXME: this is a sinful hack, compacting all items into a numpy array for "fast" checking
        all_items = np.array(
            list(itertools.chain.from_iterable(list(self.subdivision.values())))
        )
        check = np.full(
            len(all_items), True
        )  # boolean index indicating items matching steering

        for dim in self.steering_filters:
            min_value = self.steering_filters[dim]["min_value"]
            max_value = self.steering_filters[dim]["max_value"]
            dim = int(dim)
            check = (
                (all_items[:, dim] >= min_value)
                & (all_items[:, dim] <= max_value)
                & check
            )

        is_empty = check.sum() == 0
        return is_empty

    def get_indeces_matching_steering_in_bucket(self, bucket_index: int) -> List[int]:
        bucket = np.array(self.subdivision[bucket_index])
        check = np.full(
            len(bucket), True
        )  # boolean index indiciating items matching steering

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
            self.subdivision[b] = [item for item in buckets[b] if item is not None]

            # delete the entire bucket if it's empty
            if len(self.subdivision[b]) == 0:
                del self.subdivision[b]

        steered_chunk = [c for c in steered_chunk if c is not None]
        return np.array(steered_chunk)

    def select_into_chunk(self, chunk: np.ndarray, chunk_size: int) -> np.ndarray:
        pos_in_chunk = 0
        while pos_in_chunk < chunk_size:
            bucket_keys = list(self.subdivision.copy().keys())

            # prevent ordering bias when chunk_size is bigger than number of bins
            random.shuffle(bucket_keys)

            # select evenly from all bins, but at least 1 item (for cases where division is 0)
            n_elements_per_bucket = max(
                (chunk_size - pos_in_chunk) // len(bucket_keys), 1
            )

            for bucket_key in bucket_keys:
                if pos_in_chunk >= chunk_size:
                    break

                # ensure to only select at most as many items as there are in the bucket
                n_elements = min(
                    len(self.subdivision[bucket_key]), n_elements_per_bucket
                )

                next_indeces = self.select_elements(
                    n_elements, chunk, pos_in_chunk, bucket_key
                )
                next_indeces.sort(reverse=True)
                pos_in_chunk += len(next_indeces)

                self.subdivision[bucket_key] = np.delete(
                    self.subdivision[bucket_key], next_indeces, axis=0
                )

                if len(self.subdivision[bucket_key]) == 0:
                    del self.subdivision[bucket_key]

        return chunk

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

        return self.select_into_chunk(chunk, chunk_size)

    # Selects from bucket bucket_key, expands chunk at index pos_in_chunk with it and returns
    # which index was selected
    @abstractmethod
    def select_elements(
        self, n_elements: int, chunk: np.ndarray, pos_in_chunk: int, bucket_key: int
    ) -> list[int]:
        pass


class SelectionRandom(Selection):
    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        subdivision_size = len(self.subdivision[bucket_key])
        indeces = sample_without_replacement(
            n_population=subdivision_size,
            n_samples=n_elements,
            random_state=random.randint(0, subdivision_size - 1),
        )

        bucket = self.subdivision[bucket_key]
        chunk[pos_in_chunk : pos_in_chunk + n_elements] = bucket[indeces]
        return list(indeces)


class SelectionFirst(Selection):
    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        indeces = range(0, n_elements)

        bucket = self.subdivision[bucket_key]
        chunk[pos_in_chunk : pos_in_chunk + n_elements] = bucket[indeces]
        return list(indeces)


class SelectionMinimum(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def load_subdivision(self, subdivision):
        super()._load_subdivision_sorted(subdivision, self.attribute)

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        n_min_indeces = np.arange(0, n_elements)

        bucket = self.subdivision[bucket_key]
        chunk[pos_in_chunk : pos_in_chunk + n_elements] = bucket[n_min_indeces]
        return list(n_min_indeces)


class SelectionMaximum(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def load_subdivision(self, subdivision):
        super()._load_subdivision_sorted(subdivision, self.attribute)

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        size = len(self.subdivision[bucket_key])
        n_max_indeces = np.arange(size - n_elements, size)

        bucket = self.subdivision[bucket_key]
        chunk[pos_in_chunk : pos_in_chunk + n_elements] = bucket[n_max_indeces]
        return list(n_max_indeces)


class SelectionMedian(Selection):
    attribute = 0

    def __init__(self, attribute):
        super().__init__()
        self.attribute = attribute

    def load_subdivision(self, subdivision):
        super()._load_subdivision_sorted(subdivision, self.attribute)

    def select_elements(self, n_elements, chunk, pos_in_chunk, bucket_key):
        # the central element in sorted_indeces is the index of the "median" in the bucket
        center_pos = len(self.subdivision[bucket_key]) // 2

        # padding around the center position. If even number of elements is returned, right end
        # of the window is bigger than left end by 1
        pad_left = (n_elements - 1) // 2
        pad_right = (
            (n_elements - 1) // 2 + 1 if n_elements % 2 == 0 else n_elements // 2
        )

        # as a heuristic, get n/2 elements before and after that element as "medians"
        if len(self.subdivision[bucket_key]) <= n_elements:
            # if less than n_elements in bucket, just return all elements in bucket
            n_median_indeces = np.arange(0, len(self.subdivision[bucket_key]))
        else:
            # otherwise us a window centered around center_pos
            n_median_indeces = np.arange(
                center_pos - pad_left, center_pos + pad_right + 1
            )

        bucket = self.subdivision[bucket_key]
        chunk[pos_in_chunk : pos_in_chunk + n_elements] = bucket[n_median_indeces]

        return list(n_median_indeces)


class SelectionSpatialAutoCorrelation(Selection):
    value_h_index = 0
    lag_h_index = 0

    def __init__(self, value_h_index: int, lag_h_index: int) -> None:
        super().__init__()
        self.value_h_index = value_h_index
        self.lag_h_index = lag_h_index

    def select_elements(
        self, n_elements: int, chunk: np.ndarray, pos_in_chunk: int, bucket_key: int
    ) -> list[int]:
        bucket = self.subdivision[bucket_key]
        indeces = []

        # we should select up to n_elements. find out how many of those should be HH, HL, LH, and LL
        for value_is_H in [True, False]:
            for lag_is_H in [True, False]:
                # find all candidates in this quadrant
                bucket_value_h = bucket[:, self.value_h_index] == value_is_H
                bucket_lag_h = bucket[:, self.lag_h_index] == lag_is_H

                # select up to 25% points in this quadrant, but at least 1
                n_selection = max(n_elements // 4, 1)
                candidate_indeces = list(
                    (bucket_value_h & bucket_lag_h).nonzero()[0][:n_selection]
                )
                indeces += candidate_indeces

        random.shuffle(indeces)

        # make sure that at most n_elements are selected. This can be useful when n_elements < 4,
        # since we are selecting at least 1 element per quadrant.
        indeces = indeces[:n_elements]
        chunk[pos_in_chunk : pos_in_chunk + len(indeces)] = bucket[indeces]

        return indeces
