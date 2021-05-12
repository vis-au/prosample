<script lang="typescript">
  import { range } from 'd3-array';
  import { onMount } from 'svelte';
  import { samplingRate } from './state/sampling-rate';
  import { samplingAmount } from './state/sampling-amount';
  import ConfigWidget from './config-widget.svelte';
  import DataView from './data-view.svelte';
  import type { PipelineConfig } from './util/types';
  import { samplingTotal } from './state/sampling-total';
  import { progressionState } from './state/progression-state';
  import { viewConfig } from './state/view-config';
  import Toggle from './widgets/toggle.svelte';

  let innerWidth = 500;
  let innerHeight = 350;
  let showCenter = true;
  let margin = {
    horizontal: showCenter ? 2 : 0,
    vertical: 125
  };
  let samplingInterval = -1;
  let samplingRateValue = -1;
  let samplingAmountValue = -1;
  let hoveredPosition: [number, number] = [-1, -1];

  samplingRate.subscribe(value => samplingRateValue = value);
  samplingAmount.subscribe(value => samplingAmountValue = value);
  viewConfig.subscribe(value => showCenter = value.showCenter);

  $: plotWidth = innerWidth / (showCenter ? 3 : 2) - margin.horizontal;
  $: plotHeight = innerHeight - margin.vertical;
  $: viewConfig.set({ showCenter })

  const leftPipeline: PipelineConfig = {
    linearization: "knn",
    selection: "first",
    subdivision: "equal attribute",
    viewType: "bins (absolute)"
  };

  const rightPipeline: PipelineConfig = {
    linearization: "knn",
    selection: "first",
    subdivision: "equal attribute",
    viewType: "bins (absolute)"
  };

  $: console.log(leftPipeline);
  $: console.log(rightPipeline);

  // [random x, random y, random attribute]
  let rawA = [];
  let rawB = [];

  onMount(() => {
    samplingRate.subscribe(value => {
      samplingRateValue = value;
      window.clearInterval(samplingInterval);
      samplingInterval = startSampling();
    });

    progressionState.subscribe(value => {
      if (value === "running") {
        samplingInterval = startSampling();
      } else {
        window.clearInterval(samplingInterval);
      }
    });
  });

  $: randomDataA = rawA.slice(0);
  $: randomDataB = rawB.slice(0);
  $: samplingTotal.set(randomDataA.length);

  function startSampling() {
    return window.setInterval(() => {
      rawA = rawA.concat(range(0, samplingAmountValue).map(() => [Math.random()**2, Math.random(), Math.random()]))
      rawB = rawB.concat(range(0, samplingAmountValue).map(() => [Math.random(), Math.random()**2, Math.random()]))
    }, samplingRateValue);
  }
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="config">
    <ConfigWidget
      id="A"
      orientation="left"
      bind:selectedViewType={ leftPipeline.viewType }
      bind:selectedSubdivisionType={ leftPipeline.subdivision }
      bind:selectedLinearizationType={ leftPipeline.linearization }
      bind:selectedSelectionType={ leftPipeline.selection }
    />
    <div class="center-config" style="min-width:{showCenter?plotWidth+margin.horizontal:50}px">
      <Toggle
        id="center-view-toggle"
        bind:active={ showCenter }
        activeText="-"
        passiveText="+"
        style="width:25px; height:25px; line-height:25px;"
      />
    </div>
    <ConfigWidget
      id="B"
      orientation="right"
      bind:selectedViewType={ rightPipeline.viewType }
      bind:selectedSubdivisionType={ rightPipeline.subdivision }
      bind:selectedLinearizationType={ rightPipeline.linearization }
      bind:selectedSelectionType={ rightPipeline.selection }
    />
  </div>
  <div class="data">
    <DataView
      id={ "left" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "left" }
      primaryDataset={ randomDataA }
      secondaryDataset={ randomDataB }
      bind:hoveredPosition={ hoveredPosition }
      bind:renderer={ leftPipeline.viewType }
    />
    <div class="vertical-line" style="min-height:{plotHeight}px;border-left:1px solid black;border-right:1px solid black">
      { #if showCenter }
        <DataView
          id={ "center" }
          width={ plotWidth }
          height={ plotHeight }
          orientation={ "center" }
          primaryDataset={ randomDataA }
          secondaryDataset={ randomDataB }
          bind:hoveredPosition={ hoveredPosition }
          renderer={ "bins (delta)" }
        />
      { /if }
    </div>
    <DataView
      id={ "right" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "right" }
      primaryDataset={ randomDataB }
      secondaryDataset={ randomDataA }
      bind:hoveredPosition={ hoveredPosition }
      bind:renderer={ rightPipeline.viewType }
    />
  </div>
</div>

<style>
  div.split-view {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  div.split-view div.config,
  div.split-view div.data {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
  }
  div.split-view div.config {
    border-bottom: 1px solid black;
  }
  div.split-view div.config div.center-config {
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
