export type ViewType = "scatterplot" | "bins (absolute)" | "bins (delta)";
export type LinearizationType = "knn" | "sort by attribute" | "z-order";
export type SubdivisionType = "equal size" | "equal cardinality" | "equal density" | "equal attribute";
export type SelectionType = "first" | "median" | "min/max" | "random";

export type ProgressionState = "paused" | "running";

export type PipelineConfig = {
  viewType: ViewType,
  linearization: LinearizationType,
  subdivision: SubdivisionType,
  selection: SelectionType
};