from . import *


class Pipeline:
  def __init__(self, config):
    self.config = {
      "data": config["data"],
      "linearization": config["linearization"],
      "subdivision": config["subdivision"],
      "selection": config["selection"],
      "params": config["params"],
      "dimension": int(config["dimension"])
    }

    # retrieves next chunk given the current_selection
    self.sampler = self._get_sampler()
    # defines the way by which the next chunk is retrieved
    self.selection = self._get_selection(config["selection"])

  def _get_sampler(self):
    dataset_name = _resolve_data(self.config["data"])
    lin_class = _resolve_linearization(self.config["linearization"])
    sub_class = _resolve_subdivision(self.config["subdivision"])

    if None in [dataset_name, lin_class, sub_class]:
      return None

    self.linearization = lin_class()

    if sub_class == SubdivisionStandard:
      self.subdivision = sub_class(chunk_size=1000)
    elif sub_class == SubdivisionRepresentativeClustering:
      subspace = self.config["params"]["subspace"]
      k = self.config["params"]["k"]
      self.subdivision = sub_class(subspace=subspace, k=k)
    elif sub_class == SubdivisionDensityClustering:
      subspace = self.config["params"]["subspace"]
      eps = self.config["params"]["eps"]
      min_samples = self.config["params"]["min_samples"]
      self.subdivision = sub_class(
        chunk_size=1000, subspace=subspace, eps=eps, min_samples=min_samples
      )
    elif sub_class == SubdivisionNaiveStratified:
      subspace = self.config["params"]["subspace"]
      self.subdivision = sub_class(chunk_size=1000, attributes=subspace)

    return Sampler(dataset_name, self.linearization, self.subdivision)

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

  def get_next_chunk(self, chunk_size: int = 1000):
    return self.sampler.sample(self.selection, chunk_size)

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
  elif subdivision == "representative":
    return SubdivisionRepresentativeClustering
  elif subdivision == "density":
    return SubdivisionDensityClustering
  elif subdivision == "stratified":
    return SubdivisionNaiveStratified
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
