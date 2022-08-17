import type { Dataset } from "$lib/util/types";
import { range, scaleLinear } from "d3";
import { derived, writable } from "svelte/store";

export const presetDatasetNames = writable(["mountain_peaks", "spotify", "taxis"]);

export const selectedDataset = writable<Dataset>({
  name: null,
  size: null
});

let _dimensionsInData: string[] = [];
export const dimensionsInData = derived([selectedDataset], ([$selectedDataset]) => {
  // HACK: hard coded dimension names ... not great but does the job
  if ($selectedDataset.name === "mountain_peaks") {
    _dimensionsInData = range(0, 4).map(d => d + "");
  } else if ($selectedDataset.name === "spotify") {
    _dimensionsInData = range(0, 13).map(d => d + "");
  } else if ($selectedDataset.name === "taxis") {
    _dimensionsInData = range(0, 25).map(d => d + "");
  } else {
    _dimensionsInData = [];
  }

  return _dimensionsInData;
});

export const dimensionNames = derived([selectedDataset], ([$selectedDataset]) => {
  // HACK: hard coded dimension names ... not great but does the job
  if ($selectedDataset.name === "mountain_peaks") {
    return ["id", "longitude", "latitude", "altitude"];
  } else if ($selectedDataset.name === "spotify") {
    return  ["id", "popularity", "duration_ms", "explicit", "danceability", "energy", "loudness",
             "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
  } else if ($selectedDataset.name === "taxis") {
    return ["tripID", "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
    "passenger_count", "trip_distance", "RatecodeID", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "total_amount", "PURepresentativeX", "PURepresentativeY",
    "DORepresentativeX", "DORepresentativeY", "normalized_value", "normalized_spatial_lag",
    "value_is_H", "spatial_lag_is_H"];
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
    mins = [0.000000, 0.000000, 3344, 0.000000, 0.000000, 0.000000, -60.000000,
            0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000];
    maxs = [586671.000000, 100.000000, 5621218, 1.000000, 0.991000, 1.000000, 5.376000,
            0.971000, 0.996000, 1.000000, 1.000000, 1.000000, 246.381000];
  } else if ($selectedDataset.name === "mountain_peaks") {
    mins = [2.480150e+05, -179.880663, -85.347589, 1.000000];
    maxs = [7.838285e+09, 179.987292, 83.571472, 52.000000];
  } else if ($selectedDataset.name === "taxis") {
    mins = [73.0, 1.0, 1.041384e+18, 1.041384e+18, 0.0, 0.01, 1.0, 1.0, 1.0, 1.0, 0.01, -0.49, 0.0,
            0.0, 0.0, 0.0, 0.31, -74.197663, 40.543353, -74.254741, 40.504555, -2.928987, -2.738654,
            0.0, 0.0];
    maxs = [76955200.0, 4.0, 1.607632e+18, 1.607634e+18, 9.0, 63.30, 99.0, 263.0, 263.0, 4.0,
            398.00, 17.50, 0.5, 300.0, 950.7, 0.3, 1003.50, -73.702319, 40.912294, -73.701511,
            40.914637, 60.361013, 26.416724, 1.0, 1.0];
  }

  _dimensionExtents.mins = mins;
  _dimensionExtents.maxs = maxs;
});

export function getExtent(dimension: string): [number, number] {
  return [_dimensionExtents.mins[+dimension], _dimensionExtents.maxs[+dimension]];
};

export function scaleChunk(chunk: number[][]): number[][] {
  const scales = _dimensionsInData.map(dim => scaleLinear(getExtent(dim), [0, 1]));

  const scaledChunk = chunk.map(row => {
    const scaledRow: number[] = [];
    scales.forEach((scale, dim) => {
      scaledRow.push(scale(row[dim]));
    });
    return scaledRow;
  });

  return scaledChunk;
}