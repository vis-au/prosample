import { scaleLinear } from "d3-scale";
import type { ScaleLinear } from "d3-scale";
import { writable } from "svelte/store";

export const scaleX = writable(getPlotScale());
export const scaleY = writable(getPlotScale());

export function getPlotScale(range?: [number, number]): ScaleLinear<number, number> {
  return scaleLinear([0, 1], range || [0, 1]);
}