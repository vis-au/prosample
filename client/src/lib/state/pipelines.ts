import { writable } from "svelte/store";
import { createPipeline, updateSelectionDimension, updateLinearization, updateSelection, updateSubdivision } from "$lib/util/requests";
import type { PipelineConfig } from "$lib/util/types";
import { leftView, rightView } from "./view-config";


let leftPipeline: PipelineConfig = null;
let rightPipeline: PipelineConfig = null;

function updateRemotePipeline(oldPipeline: PipelineConfig, newPipeline: PipelineConfig) {
  console.log(oldPipeline.subdivision, newPipeline.subdivision)
  if (oldPipeline.linearization !== newPipeline.linearization) {
    updateLinearization(newPipeline.id, newPipeline.linearization);
  }
  if (oldPipeline.subdivision !== newPipeline.subdivision) {
    updateSubdivision(newPipeline.id, newPipeline.subdivision, newPipeline.subdivisionParams);
  }
  if (oldPipeline.selection !== newPipeline.selection) {
    updateSelection(newPipeline.id, newPipeline.selection);
  }
  if (oldPipeline.selectionDimension !== newPipeline.selectionDimension) {
    updateSelectionDimension(newPipeline.id, newPipeline.selectionDimension);
  }

  oldPipeline = JSON.parse(JSON.stringify(newPipeline));
}

export const leftPipelineConfig = writable<PipelineConfig>({
  id: "left",
  linearization: "z-order",
  subdivision: "standard",
  subdivisionParams: {
    subspace: [17, 18],  // pickup location x, y
    k: 1000,
    eps: 3,
    min_samples: 100
  },
  selection: "minimum",
  selectionDimension: "5"
});

export const rightPipelineConfig = writable<PipelineConfig>({
  id: "right",
  linearization: "z-order",
  subdivision: "standard",
  subdivisionParams: {
    subspace: [17, 18],  // pickup location x, y
    k: 1000,
    eps: 3,
    min_samples: 100
  },
  selection: "random",
  selectionDimension: "5"
});


leftPipelineConfig.subscribe(value => {
  if (leftPipeline === null) {
    leftPipeline = JSON.parse(JSON.stringify(value));
    return value;
  }

  updateRemotePipeline(leftPipeline, value);
  return value;
});

rightPipelineConfig.subscribe(value => {
  if (rightPipeline === null) {
    rightPipeline = JSON.parse(JSON.stringify(value));
    return value;
  }

  updateRemotePipeline(rightPipeline, value);
  return value;
});

export async function createPipelines(): Promise<void> {
  await createPipeline(leftPipeline)
    .then(() => leftView.update(v => {
      v.initialized = true;
      return v;
    }));

  await createPipeline(rightPipeline)
    .then(() => rightView.update(v => {
      v.initialized = true;
      return v;
    }));
}
