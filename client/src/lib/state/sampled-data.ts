import { writable } from "svelte/store";

// [random x, random y, random attribute]
export const primarySample = writable([] as number[][]);
export const secondarySample = writable([] as number[][]);
