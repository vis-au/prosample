import server.pipeline as pl


class Pipeline:
  def __init__(self, config):
    self.configuration = {
      "data": config.data,
      "linearization": config.linearization,
      "subdivision": config.subdivision,
      "selection": config.selection,
      "attribute": 3
    }

    # retrieves next chunk given the current_selection
    self.sampler = self._get_sampler()
    # defines the way by which the next chunk is retrieved
    self.selection = self._get_selection()


  def _get_sampler(self):
    data = _resolve_data(self.config.data)
    lin_class = _resolve_linearization(self.config.linearization)
    sub_class = _resolve_subdivision(self.config.subdivision)

    if None in [data, lin_class, sub_class]:
      print("cannot get sampler, configuration flawed")
      return None

    self.linearization = lin_class()
    self.subdivision = sub_class()

    return pl.Sampler(data, self.linearization, self.subdivision)


  def _get_selection(self, selection_string):
    sel_class = _resolve_selection(selection_string)

    if sel_class == None:
      print("cannot resolve selection.")
      return None

    return sel_class(self.configuration.attribute)


  def update_attribute(self, attribute):
    self.configuration["attribute"] = attribute


  def update_selection(self, new_selection):
    sel_class = self._get_selection(new_selection)
    self.selection = sel_class(self.configuration.attribute)





def _resolve_data(data):
  if data == "mountain peaks":
    return pl.MOUNTAIN_PEAKS
  else:
    return None

def _resolve_linearization(linearization):
  if linearization == "z-order":
    return pl.LinearizationZOrder
  elif linearization == "knn":
    return pl.LinearizationNearestNeighbour
  elif linearization == "strip":
    return pl.LinearizationStrip
  elif linearization == "random":
    return pl.LinearizationRandom
  else:
    return None

def _resolve_subdivision(subdivision):
  if subdivision == "standard":
    return pl.SubdivisionStandard
  elif subdivision == "bucket size":
    return pl.SubdivisionBucketSize
  else:
    return None

def _resolve_selection(selection):
  if selection == "random":
    return pl.SelectionRandom
  elif selection == "first":
    return pl.SelectionFirst
  elif selection == "minimum":
    return pl.SelectionMinimum
  elif selection == "maximum":
    return pl.SelectionMaximum
  elif selection == "median":
    return pl.SelectionMedian
  else:
    return None