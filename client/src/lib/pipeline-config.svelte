<script lang="typescript">
  import { dimensionsInData } from "./state/dimensions-in-data";
  import { leftPipelineConfig, rightPipelineConfig } from "./state/pipelines";
  import { leftView, rightView } from "./state/view-config";
  import type { LinearizationType, SelectionType, SubdivisionType } from "./util/types";

  export let id = "0";
  export let orientation: "left" | "right";

  $: view = orientation === "left" ? leftView : rightView;
  $: pipelineConfig = orientation === "left" ? leftPipelineConfig : rightPipelineConfig;
  $: isSamplingRunning = $view?.pointsRetrieved > 0;

  const linearizationTypes: LinearizationType[] = ["z-order", "knn", "strip", "random"];
  const subdivisionTypes: SubdivisionType[] = ["standard", "bucket_size"];
  const selectionTypes: SelectionType[] = ["first", "median", "minimum", "maximum", "random"];
</script>

<div class="pipeline-config-view {orientation} {isSamplingRunning ? "disabled" : ""}">
  <div class="title">
    <h1>Pipeline Configuration {id}</h1>
    <div class="status { $view.initialized ? "ready" : "" }" title="{ !$view.initialized ? "not " : "" }ready"></div>
  </div>
  <div class="configuration">
    <div class="pipeline">
      <label for="{id}-linearization" class="linearization">
        <span title="linearization">Lin.</span>
        <select id="{id}-linearization" name="{id}-linearization" bind:value={ $pipelineConfig.linearization } disabled={ isSamplingRunning }>
          { #each linearizationTypes as type }
          <option value={ type }>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-subdivision" class="subdivision">
        <span title="subdivision">Sub.</span>
        <select id="{id}-subdivision" name="{id}-subdivision" bind:value={ $pipelineConfig.subdivision } disabled={ isSamplingRunning }>
          { #each subdivisionTypes as type }
            <option value={ type }>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-selection" class="selection">
        <span title="selection">Sel.</span>
        <select id="{id}-selection" name="{id}-selection" bind:value={ $pipelineConfig.selection }>
          { #each selectionTypes as type }
            <option value={ type }>{ type } </option>
          { /each }
        </select>
      </label>
      { #if ["minimum", "median", "maximum"].indexOf($pipelineConfig.selection) > -1}
        <label for="{id}-selection-dimension" class="selection">
          <span title="selection-dimension">in</span>
          <select id="{id}-selection-dimension" name="{id}-selection-dimension" bind:value={ $pipelineConfig.selectionDimension }>
            { #each $dimensionsInData as dim }
              <option value={ dim }>{ dim } </option>
            { /each }
          </select>
        </label>
      { /if }
    </div>
    <div class="metadata">
      sampled:
      <!-- src: https://stackoverflow.com/a/2901298 -->
      <span class="total">{$view.pointsRetrieved.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</span>
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
  div.pipeline-config-view.disabled .linearization,
  div.pipeline-config-view.disabled .subdivision {
    color: #aaa;
  }
  div.pipeline-config-view .title h1 {
    font-size: 15px;
  }
  div.pipeline-config-view .title .status {
    width: 10px;
    height: 10px;
    background: firebrick;
    border: none;
    border-radius: 10px;
    margin-left: 10px;
  }
  div.pipeline-config-view .title .status.ready {
    background: limegreen;
  }
  div.pipeline-config-view .configuration {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  div.pipeline-config-view .configuration .metadata span.total {
    font-weight: bold;
  }
</style>