import { writable } from "svelte/store";

export const dimensionsInData = writable(["1", "2", "3"] as string[]);