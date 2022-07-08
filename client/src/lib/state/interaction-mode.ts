import type { InteractionMode } from "$lib/util/types";
import { writable } from "svelte/store";

export const interactionMode = writable("brush" as InteractionMode);