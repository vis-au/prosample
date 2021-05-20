<script lang="typescript">
  import { leftPipeline, rightPipeline } from "$lib/state/pipelines";
  import type { LinearizationType, PipelineConfig, SelectionType, SubdivisionType, ViewType } from "../util/types";

  export let id = "0";
  export let orientation: "left" | "right" | "center" = "left";

  let configuration: PipelineConfig = null;

  $: pipeline = orientation === "left" ? leftPipeline : rightPipeline;
  $: pipeline.set(configuration);
  $: pipeline.subscribe(value => configuration = value);

  const linearizationTypes: LinearizationType[] = ["z-order", "knn", "strip", "random"];
  const subdivisionTypes: SubdivisionType[] = ["standard", "bucket_size"];
  const selectionTypes: SelectionType[] = ["first", "median", "minimum", "maximum", "random"];
  const viewTypes: ViewType[] = ["scatterplot", "bins (absolute)", "bins (delta)"];
</script>

<div class="pipeline-config-view {orientation}">
  <div class="title">
    <h1>Pipeline Configuration {id}</h1>
    <div class="status { configuration.ready ? "ready" : "" }" title="{ !configuration.ready ? "not " : "" }ready"></div>
  </div>
  <div class="configuration">
    <div class="pipeline">
      <label for="{id}-linearization">
        <span title="linearization">Lin.</span>
        <select id="{id}-linearization" name="{id}-linearization" bind:value={ configuration.linearization }>
          { #each linearizationTypes as type }
          <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-subdivision">
        <span title="subdivision">Sub.</span>
        <select id="{id}-subdivision" name="{id}-subdivision" bind:value={ configuration.subdivision }>
          { #each subdivisionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-selection">
        <span title="selection">Sel.</span>
        <select id="{id}-selection" name="{id}-selection" bind:value={ configuration.selection }>
          { #each selectionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
    </div>
    <div class="view">
      <label for="{id}-view">
        <span>View</span>
        <select id="{id}-view" name="{id}-view" bind:value={ configuration.viewType }>
          { #each viewTypes as type }
            <option>{ type }</option>
          { /each }
        </select>
      </label>
    </div>
  </div>
</div>

<style>
  div.pipeline-config-view {
    padding: 0 5px 10px;
    box-sizing: border-box;
    border: 1px solid black;
    width: 100%;
  }
  div.pipeline-config-view.left {
    border-right: none;
  }
  div.pipeline-config-view.right {
    border-left: none;
  }
  div.pipeline-config-view .title {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
  div.pipeline-config-view .title h1 {
    font-size: 15px;
  }
  div.pipeline-config-view .title .status {
    width: 10px;
    height: 10px;
    background: white;
    border: 2px solid black;
    margin-left: 5px;
  }
  div.pipeline-config-view .title .status.ready {
    background: black;
  }
  div.pipeline-config-view .configuration {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
</style>