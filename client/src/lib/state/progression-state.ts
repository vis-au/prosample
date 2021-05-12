import { writable } from "svelte/store";
import type { ProgressionState } from "../util/types";

export const progressionState = writable("paused" as ProgressionState);