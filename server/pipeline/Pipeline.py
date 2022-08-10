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
    self.linearization = self._get_linearization(self.config["linearization"])
    self.subdivision = self._get_subdivision(self.config["subdivision"])

    if None in [dataset_name, self.linearization, self.subdivision]:
      return None

    return Sampler(dataset_name, self.linearization, self.subdivision)

  def _get_linearization(self, linearization_string):
    lin_class = _resolve_linearization(linearization_string)
    linearization = lin_class()
    return linearization

  def _get_subdivision(self, subdivision_string: str):
    sub_class = _resolve_subdivision(subdivision_string)
    subdivision = None

    if sub_class == SubdivisionStandard:
      subdivision = sub_class(chunk_size=1000)
    elif sub_class == SubdivisionNaiveStratified:
      subspace = self.config["params"]["subspace"]
      subdivision = sub_class(chunk_size=1000, attribute=subspace[0])
    elif sub_class == SubdivisionDistance:
      subspace = self.config["params"]["subspace"]
      subdivision = sub_class(n_bins=100, attributes=subspace)
    elif sub_class is not None:
      subdivision = sub_class()

    return subdivision

  def _get_selection(self, selection_string):
    sel_class = _resolve_selection(selection_string)

    if sel_class is None:
      print("cannot resolve selection.")
      return None

    # some selection strategies work on specific dimensions, so pass that parameter in those cases
    if sel_class not in [SelectionFirst, SelectionRandom]:
      return sel_class(self.config["dimension"])
    else:
      return sel_class()

  def update_dimension(self, dimension):
    self.config["dimension"] = int(dimension)

  def update_selection(self, new_selection: str):
    self.selection = self._get_selection(new_selection)

  def update_subdivision(self, new_subdivision: str):
    self.subdivision = self._get_subdivision(new_subdivision)
    self.sampler.update_subdivision(self.subdivision)

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
  elif subdivision == "stratified":
    return SubdivisionNaiveStratified
  elif subdivision == "distance":
    return SubdivisionDistance
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
