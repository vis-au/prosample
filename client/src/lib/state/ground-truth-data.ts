import { getAllData } from "$lib/util/requests";
import { writable } from "svelte/store";


export const groundTruthData = writable([] as number[][]);

export const hasGroundTruthBeenLoaded = writable(false);


export async function preloadGroundTruthDataset(): Promise<void> {
  const response = await getAllData("left");
  const groundTruth = await response.json();

  console.log(groundTruth);

  groundTruthData.set(groundTruth);
  hasGroundTruthBeenLoaded.set(true);
}
