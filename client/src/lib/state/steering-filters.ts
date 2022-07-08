import type { Filter } from "$lib/util/types";
import { writable } from "svelte/store";

export const steeringFilters = writable({
  x: null as Filter,
  y: null as Filter
});