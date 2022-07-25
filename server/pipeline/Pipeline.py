from . import *


class Pipeline:
  def __init__(self, config):
    self.config = {
      "data": config["data"],
      "linearization": config["linearization"],
      "subdivision": config["subdivision"],
      "selection": config["selection"],
      "dimension": int(config["dimension"])
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
      print("cannot get sampler, because configuration contains unknown values.")
      return None

    self.linearization = lin_class()

    if sub_class == SubdivisionBucketSize:
      self.subdivision = sub_class(self.config["dimension"], 1000)
    else:
      self.subdivision = sub_class(0.001)

    return Sampler(data, self.linearization, self.subdivision)

  def _get_selection(self, selection_string):
    sel_class = _resolve_selection(selection_string)

    if sel_class is None:
      print("cannot resolve selection.")
      return None

    if sel_class not in [SelectionFirst, SelectionRandom]:
      return sel_class(self.config["dimension"])
    else:
      return sel_class()

  def update_dimension(self, dimension):
    self.config["dimension"] = int(dimension)

  def update_selection(self, new_selection):
    self.selection = self._get_selection(new_selection)

  def get_next_chunk(self):
    return self.sampler.sample(self.selection)

  def get_config(self):
    return self.config

  def get_dataset_size(self):
    return self.sampler.get_dataset_size()


def _resolve_data(data):
  if data == "mountain_peaks":
    return MOUNTAIN_PEAKS
  elif data == "spotify":
    return SPOTIFY
  elif data == "taxis":
    return TAXIS
  else:
    return None


def _resolve_linearization(linearization):
  if linearization == "z-order":
    return LinearizationReaderZOrder
  elif linearization == "z-order-geo":
    return LinearizationReaderGeoZOrder
  elif linearization == "numeric":
    return LinearizationReaderNumeric
  elif linearization == "temporal":
    return LinearizationReaderTemporal
  elif linearization == "knn":
    return LinearizationReaderNearestNeighbour
  elif linearization == "strip":
    return LinearizationReaderStrip
  elif linearization == "random":
    return LinearizationReaderRandom
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
