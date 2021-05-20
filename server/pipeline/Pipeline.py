from . import *

class Pipeline:
  def __init__(self, config):
    self.config = {
      "data": config["data"],
      "linearization": config["linearization"],
      "subdivision": config["subdivision"],
      "selection": config["selection"],
      "attribute": 3
    }

    # retrieves next chunk given the current_selection
    self.sampler = self._get_sampler()
    # defines the way by which the next chunk is retrieved
    self.selection = self._get_selection(config["selection"])


  def _get_sampler(self):
    data = _resolve_data(self.config["data"])
    lin_class = _resolve_linearization(self.config["linearization"])
    sub_class = _resolve_subdivision(self.config["subdivision"])

    if None in [data, lin_class, sub_class]:
      print("cannot get sampler, configuration flawed")
      return None

    self.linearization = lin_class()
    self.subdivision = sub_class(0.1)

    return Sampler(data, self.linearization, self.subdivision)


  def _get_selection(self, selection_string):
    sel_class = _resolve_selection(selection_string)

    if sel_class == None:
      print("cannot resolve selection.")
      return None

    return sel_class(self.config["attribute"]) if sel_class not in [SelectionFirst, SelectionRandom] else sel_class()


  def update_attribute(self, attribute):
    self.config["attribute"] = attribute


  def update_selection(self, new_selection):
    self.selection = self._get_selection(new_selection)


  def get_next_chunk(self):
    return self.sampler.sample(self.selection)



def _resolve_data(data):
  if data == "mountain_peaks":
    return MOUNTAIN_PEAKS
  else:
    return None

def _resolve_linearization(linearization):
  if linearization == "z-order":
    return LinearizationZOrder
  elif linearization == "knn":
    return LinearizationNearestNeighbour
  elif linearization == "strip":
    return LinearizationStrip
  elif linearization == "random":
    return LinearizationRandom
  else:
    return None

def _resolve_subdivision(subdivision):
  if subdivision == "standard":
    return SubdivisionStandard
  elif subdivision == "bucket_size":
    return SubdivisionBucketSize
  else:
    return None

def _resolve_selection(selection):
  if selection == "random":
    return SelectionRandom
  elif selection == "first":
    return SelectionFirst
  elif selection == "minimum":
    return SelectionMinimum
  elif selection == "maximum":
    return SelectionMaximum
  elif selection == "median":
    return SelectionMedian
  else:
    return None