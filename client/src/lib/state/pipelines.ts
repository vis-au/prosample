import type { Pipeline } from "$lib/util/types";
import { writable } from "svelte/store";


export const leftPipeline = writable<Pipeline>({
  id: "left",
  initialized: false,
  config: {
    linearization: "knn",
    subdivision: "standard",
    selection: "minimum",
    selectionDimension: "3"
  },
  viewType: "bins (absolute)",
  colorScaleType: "log",
  pointsRetrieved: 0
});

export const rightPipeline = writable<Pipeline>({
  id: "right",
  initialized: false,
  config: {
    linearization: "knn",
    subdivision: "standard",
    selection: "random",
    selectionDimension: "3"
  },
  viewType: "bins (absolute)",
  colorScaleType: "log",
  pointsRetrieved: 0
});