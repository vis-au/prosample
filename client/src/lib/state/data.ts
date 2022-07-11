import type { Dataset } from "$lib/util/types";
import { range } from "d3";
import { derived, writable } from "svelte/store";

export const presetDatasetNames = writable(["mountain_peaks", "spotify"]);

export const selectedDataset = writable<Dataset>({
  name: null,
  size: null
});

export const dimensionsInData = derived([selectedDataset], ([$selectedDataset]) => {
  // HACK: hard coded dimension names ... not great but does the job
  if ($selectedDataset.name === "mountain_peaks") {
    return range(0, 4).map(d => d + "");
  } else if ($selectedDataset.name === "spotify") {
    return range(0, 13).map(d => d + "");
  } else {
    return [];
  }
});

export const dimensionNames = derived([selectedDataset], ([$selectedDataset]) => {
  // HACK: hard coded dimension names ... not great but does the job
  if ($selectedDataset.name === "mountain_peaks") {
    return ["id", "longitude", "latitude", "altitude"];
  } else if ($selectedDataset.name === "spotify") {
    return  ["id", "popularity", "duration_ms", "explicit", "danceability", "energy", "loudness",
             "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
  } else {
    return [];
  }
});

const _dimensionExtents: { mins: number[], maxs: number[] } = { mins: [], maxs: [] };
selectedDataset.subscribe($selectedDataset => {
  let mins: number[] = [];
  let maxs: number[] = [];

  // HACK: hard coded dimension extents ... not great but does the job
  if ($selectedDataset.name === "spotify") {
    mins = [0.000000, 0.000000, 3.344000e+03, 0.000000, 0.000000, 0.000000, -60.000000,
                  0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000];
    maxs = [586671.000000, 100.000000, 5.621218e+06, 1.000000, 0.991000, 1.000000, 5.376000,
                  0.971000, 0.996000, 1.000000, 1.000000, 1.000000, 246.381000];
  } else if ($selectedDataset.name === "mountain_peaks") {
    mins = [2.480150e+05, -179.880663, -85.347589, 1.000000];
    maxs = [7.838285e+09, 179.987292, 83.571472, 52.000000];
  }

  _dimensionExtents.mins = mins;
  _dimensionExtents.maxs = maxs;
});

export function getExtent(dimension: number): [number, number] {
  return [_dimensionExtents.mins[dimension], _dimensionExtents.maxs[dimension]];
};