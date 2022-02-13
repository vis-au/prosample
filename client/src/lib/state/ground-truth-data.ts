import { getAllData, isRemoteBusy } from "$lib/util/requests";
import { derived, writable } from "svelte/store";
import { leftView, rightView } from "./view-config";


export const groundTruthData = writable([] as number[][]);

export const hasGroundTruthBeenLoaded = writable(false);


async function preloadGroundTruthDataset(): Promise<void> {
  const response = await getAllData("left");
  const groundTruth = await response.json();

  console.log(groundTruth);

  groundTruthData.set(groundTruth);
  hasGroundTruthBeenLoaded.set(true);
}

const viewsReady = derived(
  [leftView, rightView, hasGroundTruthBeenLoaded, isRemoteBusy],
  ([$leftView, $rightView, $hasGroundTruthBeenLoaded, $isRemoteBusy]) => {

  return $leftView.initialized
    && $rightView.initialized
    && !$hasGroundTruthBeenLoaded
    && !$isRemoteBusy;
});

// FIXME: enable this snippet to load the ground truth data from the frontend, which will allow the
// comparisons with the "real" data to assess the sampling quality.
// viewsReady.subscribe(async value => {
//   if (value) {
//     await preloadGroundTruthDataset();
//     console.log("done loading ground truth")
//   }
// });