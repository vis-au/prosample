import { selectedDataset } from "../state/selected-dataset";
import type { PipelineConfig, Orientation, SelectionType } from "./types";

const BASE_URL = "http://127.0.0.1:5000";

let currentDataset = null;
selectedDataset.subscribe(value => currentDataset = value);

function pipelineConfigToURLParams(configuration: PipelineConfig) {
  const lin = `linearization=${configuration.linearization}`;
  const sub = `subdivision=${configuration.subdivision}`;
  const sel = `selection=${configuration.selection}`;
  const dim = `dimension=${configuration.selectionDimension}`;

  return `${lin}&${sub}&${sel}&${dim}`;
}

export async function createPipeline(pipeline: PipelineConfig): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(pipeline);

  return fetch(`${BASE_URL}/create_pipeline/${pipeline.id}?${config}&${dat}`);
}

export async function updatePipeline(pipeline: PipelineConfig): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(pipeline);

  return fetch(`${BASE_URL}/update_pipeline/${pipeline.id}?${config}&${dat}`);
}

export async function setSelection(id: Orientation, selection: SelectionType): Promise<Response> {
  return fetch(`${BASE_URL}/set_selection/${id}?selection=${selection}`);
}

export async function sample(id: Orientation): Promise<Response> {
  return fetch(`${BASE_URL}/sample/${id}`);
}

export function reset(): Promise<void> {
  return fetch(`${BASE_URL}/reset`).then(() => console.log("pipelines were reset."));
}