import pandas as pd
from . import *


class Sampler:
    def __init__(self, data_set_name, linearization: LinearizationReader, subdivision: Subdivision):
        self.data_set_name = data_set_name
        self.linearization_frame = linearization
        self.subdivision_frame = subdivision
        self.dataset_size = -1
        self.pre_processing()

    def pre_processing(self):
        print("preprocessing pipeline ...")
        linearization = self.linearization_frame.read_linearization(self.data_set_name)
        self.dataset_size = linearization.shape[0]
        self.subdivision_frame.load_linearization(linearization)
        subdivision = self.subdivision_frame.subdivide()
        self.subdivision = subdivision
        print("Done with the pre-processing")

    def sample(self, selection: Selection, chunk_size: int = -1):
        # return the next chunk of data points
        selection.load_subdivision(self.subdivision)
        return selection.next_chunk(chunk_size)                           # <-- Check for None!

    def get_dataset_size(self):
        return self.dataset_size
