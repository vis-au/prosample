import { scaleLinear } from "d3";
import { writable } from "svelte/store";
import { getExtent, selectedDataset } from "../state/data";
import type { PipelineConfig, Orientation, SelectionType, LinearizationType, SubdivisionType, Filter } from "./types";

const BASE_URL = "http://127.0.0.1:5000";

let currentDataset = null;
selectedDataset.subscribe(value => currentDataset = value.name);

export const isRemoteBusy = writable(false);

function pipelineConfigToURLParams(configuration: PipelineConfig) {
  const lin = `linearization=${configuration.linearization}`;
  const sub = `subdivision=${configuration.subdivision}`;
  const sel = `selection=${configuration.selection}`;
  const dim = `dimension=${configuration.selectionDimension}`;

  return `${lin}&${sub}&${sel}&${dim}`;
}

export async function createPipeline(pipeline: PipelineConfig): Promise<void> {
  if (currentDataset === null) {
    return;
  }
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(pipeline);

  isRemoteBusy.set(true);
  return fetch(`${BASE_URL}/create_pipeline/${pipeline.id}?${config}&${dat}`)
    .then(() => isRemoteBusy.set(false));
}

export function updateLinearization(id: Orientation, linearization: LinearizationType): Promise<void> {
  isRemoteBusy.set(true);
  return fetch(`${BASE_URL}/update_linearization/${id}?linearization=${linearization}`)
    .then(() => isRemoteBusy.set(false));
}

export function updateSubdivision(id: Orientation, subdivision: SubdivisionType): Promise<void> {
  isRemoteBusy.set(true);
  return fetch(`${BASE_URL}/update_subdivision/${id}?subdivision=${subdivision}`)
  .then(() => isRemoteBusy.set(false));
}

export function updateSelection(id: Orientation, selection: SelectionType): Promise<void> {
  isRemoteBusy.set(true);
  return fetch(`${BASE_URL}/update_selection/${id}?selection=${selection}`)
  .then(() => isRemoteBusy.set(false));
}

export function updateSelectionDimension(id: Orientation, dimension: string): Promise<void> {
  isRemoteBusy.set(true);
  return fetch(`${BASE_URL}/update_dimension/${id}?dimension=${dimension}`)
   .then(() => isRemoteBusy.set(false));
}

export async function sample(id: Orientation): Promise<Response> {
  return fetch(`${BASE_URL}/sample/${id}`);
}

export async function getAllData(id: Orientation): Promise<Response> {
  return fetch(`${BASE_URL}/all_data/${id}`)
}

export async function steer(filter: Filter): Promise<Response> {
  const { dimension, min, max } = filter;
  const extent = getExtent(dimension);
  const scale = scaleLinear([0, 1], extent);
  return fetch(`${BASE_URL}/steer?dimension=${dimension}&min=${scale(min)}&max=${scale(max)}`);
}

export async function cancelSteering(): Promise<Response> {
  return fetch(`${BASE_URL}/steer/cancel`);
}

export function getDatasetSize(id: Orientation): Promise<void> {
  return fetch(`${BASE_URL}/data_size/${id}`)
    .then((res) => res.json())
    .then(size => {
      selectedDataset.set({
        name: currentDataset,
        size
      })
    });
}

export function reset(): Promise<void> {
  return fetch(`${BASE_URL}/reset`).then(() => console.log("pipelines were reset."));
}