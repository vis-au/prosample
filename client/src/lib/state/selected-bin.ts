import type { BinType } from "$lib/util/bin-generator";
import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";

export const selectedBins = writable([] as HexbinBin<BinType>[]);