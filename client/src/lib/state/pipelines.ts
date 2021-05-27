import type { PipelineConfig } from "$lib/util/types";
import { writable } from "svelte/store";

export const leftPipelineConfig = writable<PipelineConfig>({
  id: "left",
  linearization: "knn",
  subdivision: "standard",
  selection: "minimum",
  selectionDimension: "3"
});

export const rightPipelineConfig = writable<PipelineConfig>({
  id: "right",
  linearization: "knn",
  subdivision: "standard",
  selection: "random",
  selectionDimension: "3"
});