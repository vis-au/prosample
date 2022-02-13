import type { ViewConfig, ViewType } from "$lib/util/types";
import { writable } from "svelte/store";
import { primarySample, secondarySample } from "./sampled-data";

export const globalViewConfig = writable({
  showCenter: false,
  useRelativeDifferenceScale: false,
  areLeftAndRightLinked: true,
  binSize: 10
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

let viewType: ViewType = null;
leftView.subscribe(left => {
  if (left.viewType !== viewType) {
    viewType = left.viewType;
    rightView.update(right => {
      if (right.viewType !== viewType) {
        right.viewType = left.viewType
      }
      return right;
    });
  }
});
rightView.subscribe(right => {
  if (right.viewType !== viewType) {
    viewType = right.viewType;
    leftView.update(left => {
      if (left.viewType !== viewType) {
        left.viewType = right.viewType;
      }
      return left;
    });
  }
})