import type { Pipeline } from "$lib/util/types";
import { writable } from "svelte/store";


export const leftPipeline = writable<Pipeline>({
  id: "left",
  initialized: false,
  config: {
    linearization: "knn",
    subdivision: "standard",
    selection: "first",
  },
  viewType: "bins (absolute)",
  pointsRetrieved: 0
});

export const rightPipeline = writable<Pipeline>({
  id: "right",
  initialized: false,
  config: {
    linearization: "knn",
    subdivision: "standard",
    selection: "random",
  },
  viewType: "bins (absolute)",
  pointsRetrieved: 0
});