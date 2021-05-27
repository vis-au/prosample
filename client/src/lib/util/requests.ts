import { selectedDataset } from "../state/selected-dataset";
import type { Pipeline, PipelineConfig, PipelineId, SelectionType } from "./types";

const BASE_URL = "http://127.0.0.1:5000";

let currentDataset = null;
selectedDataset.subscribe(value => currentDataset = value);

function pipelineConfigToURLParams(configuration: PipelineConfig) {
  const lin = `linearization=${configuration.linearization}`;
  const sub = `subdivision=${configuration.subdivision}`;
  const sel = `selection=${configuration.selection}`;
  const dim = `dimension=${configuration.selection}`;

  return `${lin}&${sub}&${sel}${dim}`;
}

export async function createPipeline(pipeline: Pipeline): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const id = pipeline.id;
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(pipeline.config);

  return fetch(`${BASE_URL}/create_pipeline/${id}?${config}&${dat}`);
}

export async function updatePipeline(id: PipelineId, configuration: PipelineConfig): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(configuration);

  return fetch(`${BASE_URL}/update_pipeline/${id}?${config}&${dat}`);
}

export async function setSelection(id: PipelineId, selection: SelectionType): Promise<Response> {
  return fetch(`${BASE_URL}/set_selection/${id}?selection=${selection}`);
}

export async function sample(id: PipelineId): Promise<Response> {
  return fetch(`${BASE_URL}/sample/${id}`);
}

export function reset(): Promise<void> {
  return fetch(`${BASE_URL}/reset`).then(() => console.log("pipelines were reset."));
}