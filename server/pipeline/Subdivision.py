from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import KDTree


class Subdivision(ABC):

    def load_linearization(self, linearization):
        self.linearization = linearization

    @abstractmethod
    def subdivide(self):
        pass


class SubdivisionStandard(Subdivision):
    sampling_rate = 0

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def subdivide(self):
        bucket_size = int(len(self.linearization) / self.chunk_size)
        no_of_points = len(self.linearization)
        subdivision = {}
        division_number = 0
        for i in range(0, no_of_points, bucket_size):
            next_division = self.linearization[i:i + bucket_size]
            next_division = list(next_division)                     # <-- for deleting in selection
            subdivision[division_number] = next_division
            division_number += 1
        return subdivision


class SubdivisionDistance(Subdivision):
    def __init__(self, attributes: list(int), n_bins: int) -> None:
        super().__init__()
        self.attributes = attributes
        self.n_bins = n_bins

    def subdivide(self):
        subdivision = {}

        # find the n_bins biggest jumps in the data along the attribute column
        X = self.linearization[:, self.attributes]
        X_ = np.empty_like(X)
        X_[:-1] = X[1:]
        X_[-1] = X[0]

        X_jump = np.linalg.norm(X - X_, axis=1)  # computes euclidean distance
        biggest_jump_indeces = np.argsort(X_jump)[-self.n_bins-1:]  # one larger than n_bins

        for i in range(self.n_bins):
            if i == 0:
                first = 0
                last = biggest_jump_indeces[i]
                subdivision[i] = X[first:last + 1]
            elif i == self.n_bins - 1:
                first = biggest_jump_indeces[i - 1]
                last = -1
                subdivision[i] = X[first+1:]
            else:
                first = biggest_jump_indeces[i - 1]
                last = biggest_jump_indeces[i]
                subdivision[i] = X[first+1:last+1]

        return subdivision


class SubdivisionNaiveStratified(Subdivision):
    def __init__(self, chunk_size: int, attributes: list[int]) -> None:
        super().__init__()
        self.chunk_size = chunk_size
        self.attributes = attributes

    def subdivide(self):
        subdivision = {}

        X = self.linearization[:, self.attributes]

        # assigns a label (i.e., a bin) along every attribute
        y = np.digitize(X, bins=np.histogram(X, bins=self.chunk_size)[1])

        # for each item, gets the most frequent label per row
        most_frequent_label = mode(y, axis=1)[0].reshape(-1, )

        for label in np.unique(most_frequent_label):
            subdivision[label] = list(self.linearization[most_frequent_label == label])

        return subdivision
