// scatterplot: plot each data item as a dot
// bins (absolute): bin the data into hexagonal bins
// bins (ground truth): plot the difference in bin density from the final dataset
export type ViewType = "scatterplot" | "bins (absolute)" | "bins (ground truth)";

export type BinColorScaleType = "linear" | "log";

export type LinearizationType = "z-order" | "knn" | "strip" | "random" | "z-order-geo" | "numeric" |
                                "temporal";
export type SubdivisionType = "standard" | "bucket_size";
export type SelectionType = "random" | "first" | "minimum" | "maximum" | "median";

export const linearizationTypes: LinearizationType[] = ["z-order", "knn", "strip", "random", "numeric", "temporal"];
export const subdivisionTypes: SubdivisionType[] = ["standard", "bucket_size"];
export const selectionTypes: SelectionType[] = ["first", "median", "minimum", "maximum", "random"];

export type ProgressionState = "paused" | "running";
export type Orientation = "left" | "center" | "right";  // position of a view in the interface

export type InteractionMode = "zoom" | "brush";

export type PipelineConfig = {
  id: Orientation,
  linearization: LinearizationType,
  subdivision: SubdivisionType,
  selection: SelectionType,
  selectionDimension: string,
};

export type ViewConfig = {
  id: Orientation,
  initialized: boolean,
  viewType: ViewType,
  colorScaleType: BinColorScaleType,
  pointsRetrieved: number
};

export type Dataset = {
  name: string,
  size: number
};

export type Filter = {
  dimension: string,
  min: number,
  max: number
};