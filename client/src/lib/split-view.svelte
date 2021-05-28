<script lang="typescript">
  import DataView from './data-view.svelte';
  import { globalViewConfig } from './state/view-config';
  import { hoveredPosition } from './state/hovered-position';
  import PipelineConfig from './pipeline-config.svelte';
  import Toggle from './widgets/toggle.svelte';
  import ViewConfig from './view-config.svelte';

  let innerWidth = 500;
  let innerHeight = 350;
  let margin = {
    horizontal: 2,
    vertical: 125
  };

  $: plotWidth = innerWidth / ($globalViewConfig.showCenter ? 3 : 2) - margin.horizontal;
  $: plotHeight = innerHeight - margin.vertical;

  function hideTooltip() {
    hoveredPosition.set([-1, -1]);
  }
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="pipeline-configs" on:mouseenter={ hideTooltip }>
    <PipelineConfig id="A" orientation="left" />
    <div class="center-config" style="min-width:{$globalViewConfig.showCenter?plotWidth+margin.horizontal:50}px">
      <Toggle
        id="center-view-toggle"
        bind:active={ $globalViewConfig.showCenter }
        activeText="-"
        passiveText="+"
        style="width:25px; height:25px; line-height:25px;"
      />
    </div>
    <PipelineConfig id="B" orientation="right" />
  </div>
  <div class="data">
    <DataView
      id={ "left" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "left" }
    />
    <div class="vertical-line" style="min-height:{plotHeight}px;border-left:1px solid black;border-right:1px solid black">
      { #if $globalViewConfig.showCenter }
        <DataView
          id={ "center" }
          width={ plotWidth }
          height={ plotHeight }
          orientation={ "center" }
        />
      { /if }
    </div>
    <DataView
      id={ "right" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "right" }
    />
  </div>
  <div class="view-configs">
    <ViewConfig id="left" />
    <ViewConfig id="center" />
    <ViewConfig id="right" />
  </div>
</div>

<style>
  div.split-view {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  div.split-view div.pipeline-configs,
  div.split-view div.data,
  div.split-view div.view-configs {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
  }
  div.split-view div.pipeline-configs {
    border-bottom: 1px solid black;
  }
  div.split-view div.pipeline-configs div.center-config {
    width: 50px;
    border: 1px solid black;
    box-sizing: border-box;
    padding: 5px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
</style>
