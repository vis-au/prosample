from abc import ABC, abstractmethod
import math


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