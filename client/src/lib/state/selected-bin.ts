import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";

export const selectedBins = writable([] as HexbinBin<[number, number]>[]);