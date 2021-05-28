import type { ViewConfig } from "$lib/util/types";
import { writable } from "svelte/store";
import { primarySample, secondarySample } from "./sampled-data";

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

primarySample.subscribe(value => {
  leftView.update(view => {
    view.pointsRetrieved = value.length;
    return view;
  });
});

export const rightView = writable<ViewConfig>({
  id: "right",
  initialized: false,
  viewType: "bins (absolute)",
  colorScaleType: "log",
  pointsRetrieved: 0
});

secondarySample.subscribe(value => {
  rightView.update(view => {
    view.pointsRetrieved = value.length;
    return view;
  });
});