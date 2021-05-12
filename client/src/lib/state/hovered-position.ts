import { writable } from "svelte/store";

export const hoveredPosition = writable(
  [null, null] as [number, number]
);