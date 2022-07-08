export type ViewType = "scatterplot" | "bins (absolute)" | "bins (delta)" | "bins (ground truth)";
export type BinColorScaleType = "linear" | "log";
export type LinearizationType = "z-order" | "knn" | "strip" | "random";
export type SubdivisionType = "standard" | "bucket_size";
export type SelectionType = "random" | "first" | "minimum" | "maximum" | "median";

export type ProgressionState = "paused" | "running";
export type Orientation = "left" | "center" | "right";

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