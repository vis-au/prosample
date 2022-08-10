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
