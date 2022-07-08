import type { Dataset } from "$lib/util/types";
import { writable } from "svelte/store";

export const presetDatasetNames = writable(["mountain_peaks", "spotify"]);

export const selectedDataset = writable<Dataset>({
  name: null,
  size: null
});

export const dimensionsInData = writable(["1", "2", "3"] );