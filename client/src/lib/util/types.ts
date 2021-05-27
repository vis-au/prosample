export type ViewType = "scatterplot" | "bins (absolute)" | "bins (delta)";
export type BinColorScaleType = "linear" | "log";
export type LinearizationType = "z-order" | "knn" | "strip" | "random";
export type SubdivisionType = "standard" | "bucket_size";
export type SelectionType = "random" | "first" | "minimum" | "maximum" | "median";

export type ProgressionState = "paused" | "running";

export type PipelineId = "left" | "right";

export type PipelineConfig = {
  linearization: LinearizationType,
  subdivision: SubdivisionType,
  selection: SelectionType
};
export type Pipeline = {
  id: PipelineId,
  initialized: boolean,
  viewType: ViewType,
  colorScaleType: BinColorScaleType,
  config: PipelineConfig,
  pointsRetrieved: number
};