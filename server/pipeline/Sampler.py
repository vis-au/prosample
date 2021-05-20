from pipeline import *

class Sampler:

    def __init__(self, data_set_name, linearization: Linearization, subdivision: Subdivision):
        self.data_set_name = data_set_name
        self.linearization_frame = linearization
        self.subdivision_frame = subdivision
        self.pre_processing()

    def pre_processing(self):
        print("preprocessing pipeline ...")
        linearization = self.linearization_frame.read_linearization(self.data_set_name)
        self.subdivision_frame.load_linearization(linearization)
        subdivision = self.subdivision_frame.subdivide()
        self.subdivision = subdivision
        print("Done with the pre-processing")

    def sample(self, selection: Selection):
        # return the next chunk of data points
        selection.load_subdivision(self.subdivision)
        return selection.next_chunk()                           # <-- Check for None!

