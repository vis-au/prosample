import pandas as pd
from . import *


class Sampler:
    def __init__(self, data_set_name, linearization: LinearizationReader, subdivision: Subdivision,
                 selection: Selection):
        self.data_set_name = data_set_name
        self.linearization_frame = linearization
        self.subdivision_frame = subdivision
        self.selection = selection
        self.dataset_size = -1
        self.pre_processing()

    def pre_processing(self):
        print("preprocessing pipeline ...")
        linearization = self.linearization_frame.read_linearization(self.data_set_name)
        self.dataset_size = linearization.shape[0]
        self.subdivision_frame.load_linearization(linearization)
        bins = self.subdivision_frame.subdivide()
        self.subdivision = bins
        self.update_selection(self.selection)
        print("Done with the pre-processing")

    def update_subdivision(self, subdivision: Subdivision):
        print("updating the subdivision")
        # load the remaining data from the linearization into the new subdivision
        subdivision.load_linearization(self.subdivision_frame.linearization)

        # generate the bins with the new subdivision over the remaining data
        bins = subdivision.subdivide()
        self.subdivision = bins
        self.selection.load_subdivision(self.subdivision)
        print("Done updating the subdivision")

    def update_selection(self, selection: Selection):
        selection.load_subdivision(self.subdivision)
        self.selection = selection

    def sample(self, selection: Selection, chunk_size: int = -1):
        # return the next chunk of data points
        return selection.next_chunk(chunk_size)

    def get_dataset_size(self):
        return self.dataset_size
