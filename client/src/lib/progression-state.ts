import { writable } from "svelte/store";
import type { ProgressionState } from "./types";

export const progressionState = writable("paused" as ProgressionState);