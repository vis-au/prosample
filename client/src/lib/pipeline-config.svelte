<script lang="typescript">
  import { dimensionsInData, selectedDataset } from "./state/data";
  import { leftPipelineConfig, rightPipelineConfig } from "./state/pipelines";
  import { globalViewConfig, leftView, rightView } from "./state/view-config";
  import { isRemoteBusy } from "./util/requests";
  import { linearizationTypes, selectionTypes, subdivisionTypes } from "./util/types";
  import ProgressBar from "./widgets/progress-bar.svelte";
  import Selection from "./widgets/selection.svelte";

  export let id = "0";
  export let orientation: "left" | "right";

  $: view = orientation === "left" ? leftView : rightView;
  $: pipelineConfig = orientation === "left" ? leftPipelineConfig : rightPipelineConfig;
  $: otherPipelineConfig = orientation === "left" ? rightPipelineConfig : leftPipelineConfig;
  $: isSamplingRunning = $view?.pointsRetrieved > 0;
  $: isConfigLoading = !$view.initialized || $isRemoteBusy;
</script>

<div class="pipeline-config-view {orientation} {isSamplingRunning ? "disabled" : ""}">
  <div class="title">
    <h1><i class="material-icons">settings</i>Pipeline Configuration {id}</h1>
    <div class="status { isConfigLoading ? "busy" : "ready" }" title="{ isConfigLoading ? "not " : "" }ready"></div>
  </div>
  <div class="configuration">
    <div class="pipeline" title="{$isRemoteBusy ? "wait a bit, server is busy" : ""}">
      <Selection
        id="{id}-linearization"
        title="linearization"
        label={ $globalViewConfig.showCenter ? "Lin." : "Linearization"}
        options={ linearizationTypes }
        isEmphasized={ $pipelineConfig.linearization !== $otherPipelineConfig.linearization }
        isDisabled={ isSamplingRunning || $isRemoteBusy }
        bind:value={ $pipelineConfig.linearization }
      />
      <Selection
        id="{id}-subdivision"
        title="subdivision"
        label={ $globalViewConfig.showCenter ? "Sub." : "Subdivision"}
        options={ subdivisionTypes }
        isEmphasized={ $pipelineConfig.subdivision !== $otherPipelineConfig.subdivision }
        isDisabled={ isSamplingRunning || $isRemoteBusy }
        bind:value={ $pipelineConfig.subdivision }
      />
      <Selection
        id="{id}-selection"
        title="selection"
        label={ $globalViewConfig.showCenter ? "Sel." : "Selection"}
        options={ selectionTypes }
        isEmphasized={ $pipelineConfig.selection !== $otherPipelineConfig.selection }
        isDisabled={ $isRemoteBusy }
        bind:value={ $pipelineConfig.selection }
      />
      { #if ["minimum", "median", "maximum"].indexOf($pipelineConfig.selection) > -1}
        <Selection
          id="{id}-selection-dimension"
          title="selection-dimension"
          label="in"
          options={ $dimensionsInData }
          isDisabled={ $isRemoteBusy }
          bind:value={ $pipelineConfig.selectionDimension }
        />
      { /if }
    </div>
    <div class="metadata">
      <div class="sampled">
        sampled:
        <!-- src: https://stackoverflow.com/a/2901298 -->
        <span class="total">{$view.pointsRetrieved.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }</span>
      </div>
      <ProgressBar id="{id}-sample-progress" height={ 2 } progress={ $view.pointsRetrieved/$selectedDataset.size } />
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
    display: flex;
    align-items: center;
  }
  div.pipeline-config-view .title h1 i {
    font-size: 13px;
    margin-right: 5px;
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
  div.pipeline-config-view .configuration,
  div.pipeline-config-view .configuration .pipeline  {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  div.pipeline-config-view .configuration .metadata {
    font-size: 13px;
  }
  div.pipeline-config-view .configuration .metadata .total {
    font-weight: bold;
  }
</style>