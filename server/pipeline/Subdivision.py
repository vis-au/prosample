from abc import ABC, abstractmethod
import math
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import KDTree
import numpy as np



class Subdivision(ABC):

    def load_linearization(self, linearization):
        self.linearization = linearization

    @abstractmethod
    def subdivide(self):
        pass


class SubdivisionStandard(Subdivision):
    sampling_rate = 0

    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate

    def subdivide(self):
        bucket_size = math.floor(1 / self.sampling_rate)
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
    def __init__(self, subspace: list[int], eps=3, min_samples=10) -> None:
        super().__init__()
        self.subspace = subspace  # list of columns used for clustering
        self.eps = eps  # espsilon neighborhood to be checked
        self.min_samples = min_samples  # number of minimum samples for density connectivity

    def subdivide(self):
        subdivision = {}

        # run dbscan over the linearized data, then place all items into the buckets matching their
        # label
        X = self.linearization[:, self.subspace]

        # HACK: train dbscan on random sample :) otherwise this takes too long
        X_sample = X[np.random.rand(len(X)) < 0.01]
        y_sample = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(X_sample)

        # HACK: use the nearest neighbor of each point as prediction for the cluster label
        tree = KDTree(X_sample)
        y = y_sample[tree.query(X, k=1, return_distance=False).reshape(-1, )]

        # y contains the labels per element
        labels = list(np.unique(y))

        for i in range(len(labels)):
            label = labels[i]
            subdivision[i] = list(X[y == label])

        return subdivision


class SubdivisionRepresentativeClustering(Subdivision):
    def __init__(self, subspace: list[int], k: int) -> None:
        super().__init__()
        self.subspace = subspace
        self.k = k

    def subdivide(self):
        subdivision = {}

        X = self.linearization[:, self.subspace]
        clustering = KMeans(n_clusters=self.k, random_state=0).fit(X[:10000])
        y = clustering.predict(X)

        # y contains the labels per element
        for i in range(self.k):
            subdivision[i] = list(X[y == i])

        return subdivision


class SubdivisionBucketSize(Subdivision):
    attribute = 0
    bucket_size = 0

    def __init__(self, attribute, bucket_size):
        self.attribute = attribute
        self.bucket_size = bucket_size

    def subdivide(self):
        no_of_points = len(self.linearization)
        subdivision = {}
        division_number = 0
        subdivision[division_number] = []
        current_size = 0
        for i in range(0, no_of_points):
            next_point = self.linearization[i]
            if current_size+next_point[self.attribute] < self.bucket_size:
                subdivision[division_number].append(next_point)
                current_size += next_point[self.attribute]
            else:
                division_number += 1
                subdivision[division_number] = [next_point]
                current_size = next_point[self.attribute]
        return subdivision
