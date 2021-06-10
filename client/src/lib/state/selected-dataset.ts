import type { Dataset } from "$lib/util/types";
import { writable } from "svelte/store";

export const selectedDataset = writable<Dataset>({
  name: null,
  size: null
});