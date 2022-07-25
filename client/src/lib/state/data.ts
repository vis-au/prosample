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
    _dimensionsInData = range(0, 23).map(d => d + "");
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
            "passenger_count", "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID",
            "DOLocationID", "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",
            "tolls_amount", "improvement_surcharge", "total_amount", "PUZone", "PURepresentativeX",
            "PURepresentativeY", "DOZone", "DORepresentativeX", "DORepresentativeY"];
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
    mins = [0.0, 1.0, 0.0, 0.01, 1.0, 1.0, 1.0, 1.0, 0.01, 0.49, 0.0, 0.0, 0.0, 0.0, 0.31,
            74.189938, 40.548830, 74.229526, 40.527316];
    maxs = [985364.0, 4.0, 9.0, 103.30, 99.0, 263.0, 265.0, 4.0, 850.00, 17.50, 0.5, 300.0, 950.7,
            0.3, 1003.50, 73.709073, 40.899852, 73.709073, 40.899852];
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