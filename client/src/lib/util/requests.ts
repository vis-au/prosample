import { isProgressionRunning } from "$lib/state/progression-state";
import { scaleLinear } from "d3";
import { writable } from "svelte/store";
import { getExtent, selectedDataset } from "../state/data";
import type { PipelineConfig, Orientation, SelectionType, LinearizationType, SubdivisionType, Filter, SubdivisionParamType } from "./types";

const BASE_URL = "http://127.0.0.1:5000";

let currentDataset = null;
selectedDataset.subscribe(value => currentDataset = value.name);

export const isRemoteBusy = writable(false);
let _isProgressionRunning = false;
isProgressionRunning.subscribe(value => {
  _isProgressionRunning = value;
});

function pipelineConfigToURLParams(configuration: PipelineConfig) {
  const lin = `linearization=${configuration.linearization}`;
  const sub = `subdivision=${configuration.subdivision}`;
  const sel = `selection=${configuration.selection}`;
  const dim = `dimension=${configuration.selectionDimension}`;

  const params = getParamsForSubdivision(
    configuration.subdivision, configuration.subdivisionParams
  );

  return `${lin}&${sub}&${sel}&${dim}&${params}`;
}

function getParamsForSubdivision(subdivision: SubdivisionType, params: SubdivisionParamType) {
  let url = "";

  if (subdivision === "density") {
    const eps = params.eps;
    const min_samples = params.min_samples;
    const subspace = params.subspace.join(":");;
    url = `params=eps+min_samples+subspace&eps=${eps}&min_samples=${min_samples}&subspace=${subspace}`;
  } else if (subdivision === "representative") {
    const k = params.k;
    const subspace = params.subspace.join(":");
    url = `params=k+subspace&k=${k}&subspace=${subspace}`;
  } else {
    url = `params=-1`;
  }

  return url;
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

export function updateSubdivision(id: Orientation, subdivision: SubdivisionType, subdivisionParams?: SubdivisionParamType): Promise<void> {
  const wasProgressionRunning = _isProgressionRunning;
  isProgressionRunning.set(false);
  isRemoteBusy.set(true);
  const params = getParamsForSubdivision(subdivision, subdivisionParams);

  // this basic url sets the subdivision type
  const url = `${BASE_URL}/update_subdivision/${id}?subdivision=${subdivision}&${params}`;

  return fetch(url).then(() => {
    isRemoteBusy.set(false);
    isProgressionRunning.set(wasProgressionRunning);
  });
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