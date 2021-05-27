import type { ViewConfig } from "$lib/util/types";
import { writable } from "svelte/store";

export const viewConfig = writable({
  showCenter: false,
  useRelativeDifferenceScale: false
});

export const leftView = writable<ViewConfig>({
  id: "left",
  initialized: false,
  viewType: "bins (absolute)",
  colorScaleType: "log",
  pointsRetrieved: 0
});

export const rightView = writable<ViewConfig>({
  id: "right",
  initialized: false,
  viewType: "bins (absolute)",
  colorScaleType: "log",
  pointsRetrieved: 0
});