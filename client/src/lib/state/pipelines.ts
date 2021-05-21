import type { PipelineConfig } from "$lib/util/types";
import { writable } from "svelte/store";


export const leftPipeline = writable<PipelineConfig>({
  id: "left",
  ready: false,
  linearization: "knn",
  selection: "first",
  subdivision: "standard",
  viewType: "bins (absolute)",
  pointsRetrieved: 0
});

export const rightPipeline = writable<PipelineConfig>({
  id: "right",
  ready: false,
  linearization: "knn",
  selection: "first",
  subdivision: "standard",
  viewType: "bins (absolute)",
  pointsRetrieved: 0
});