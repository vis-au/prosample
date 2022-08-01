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


class SubdivisionDensityClustering(Subdivision):
    def __init__(self, chunk_size: int, subspace: list[int], eps=3, min_samples=10) -> None:
        super().__init__()
        self.chunk_size = chunk_size  # number of items/subdivisions to produce
        self.subspace = subspace  # list of columns used for clustering
        self.eps = eps  # espsilon neighborhood to be checked
        self.min_samples = min_samples  # number of minimum samples for density connectivity

    def subdivide(self):
        subdivision = {}

        # run dbscan over the linearized data, then place all items into the buckets matching their
        # label
        X = self.linearization[:, self.subspace]

        # HACK: train dbscan on random sample :) otherwise this takes too long
        p = (self.chunk_size / len(X)) * 10  # make sure that there are enough training points
        X_sample = X[np.random.rand(len(X)) < p]
        y_sample = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(X_sample)

        # HACK: use the nearest neighbor of each point as prediction for the cluster label
        tree = KDTree(X_sample)
        y = y_sample[tree.query(X, k=1, return_distance=False).reshape(-1, )]

        # HACK: to get the number of buckets up to chunk_size, further subdivide each each bucket
        n_labels = len(np.unique(y))
        groups_per_label = self.chunk_size // n_labels
        y = y * groups_per_label  # for g_p_l:=3, this means that 0, 1, 2 becomes 0, 3, 6
        y = y + np.random.randint(0, groups_per_label, len(y))  # means that 0 becomes 0 - 3

        # y contains the labels per element
        buckets = list(np.unique(y))

        for i in range(len(buckets)):
            bucket = buckets[i]
            subdivision[i] = list(self.linearization[y == bucket])

        return subdivision


class SubdivisionRepresentativeClustering(Subdivision):
    def __init__(self, subspace: list[int], k: int) -> None:
        super().__init__()
        self.subspace = subspace
        self.k = k

    def subdivide(self):
        subdivision = {}

        X = self.linearization[:, self.subspace]

        # HACK: train clustering on random sample :) otherwise this takes too long
        p = (self.k / len(X)) * 10
        X_sample = X[np.random.rand(len(X)) < p]
        clustering = KMeans(n_clusters=self.k, random_state=0).fit(X_sample)
        y = clustering.predict(X)

        # y contains the labels per element
        for i in range(self.k):
            subdivision[i] = list(self.linearization[y == i])

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


class SubdivisionNaiveMultivariate(Subdivision):
    def __init__(self, chunk_size: int) -> None:
        super().__init__()
        self.chunk_size = chunk_size

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
