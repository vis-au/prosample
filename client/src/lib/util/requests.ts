import { selectedDataset } from "../state/selected-dataset";
import type { PipelineConfig, PipelineId, SelectionType } from "./types";

const BASE_URL = "http://127.0.0.1:5000";

let currentDataset = null;
selectedDataset.subscribe(value => currentDataset = value);

function pipelineConfigToURLParams(configuration: PipelineConfig) {
  const lin = `linearization=${configuration.linearization}`;
  const sub = `subdivision=${configuration.subdivision}`;
  const sel = `selection=${configuration.selection}`;

  return `${lin}&${sub}&${sel}`;
}

export async function createPipeline(configuration: PipelineConfig): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const id = configuration.id;
  const dat = `data=${currentDataset}`;
  const config = pipelineConfigToURLParams(configuration);

  return fetch(`${BASE_URL}/create_pipeline/${id}?${config}&${dat}`);
}

export async function updatePipeline(configuration: PipelineConfig): Promise<Response> {
  if (currentDataset === null) {
    return;
  }
  const id = configuration.id;
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