<script lang="typescript">
  import { onMount } from 'svelte';
  import { samplingRate } from './state/sampling-rate';
  import { samplingAmount } from './state/sampling-amount';
  import type { PipelineConfig } from './util/types';
  import { samplingTotal } from './state/sampling-total';
  import { progressionState } from './state/progression-state';
  import { viewConfig } from './state/view-config';
  import { generator } from './util/bin-generator';
  import { hoveredPosition } from './state/hovered-position';
  import ViewConfig from './widgets/view-config.svelte';
  import DataView from './data-view.svelte';
  import Toggle from './widgets/toggle.svelte';
  import { sample, updatePipeline } from './util/requests';
  import { selectedDataset } from './util/selected-dataset';

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
  let currentDataset = "mountain_peaks";

  samplingRate.subscribe(value => samplingRateValue = value);
  samplingAmount.subscribe(value => samplingAmountValue = value);
  viewConfig.subscribe(value => showCenter = value.showCenter);
  selectedDataset.subscribe(value => currentDataset = value);

  $: plotWidth = innerWidth / (showCenter ? 3 : 2) - margin.horizontal;
  $: plotHeight = innerHeight - margin.vertical;
  $: viewConfig.set({ showCenter })

  const leftPipeline: PipelineConfig = {
    id: "left",
    linearization: "knn",
    selection: "first",
    subdivision: "standard",
    viewType: "bins (absolute)"
  };

  const rightPipeline: PipelineConfig = {
    id: "right",
    linearization: "knn",
    selection: "first",
    subdivision: "standard",
    viewType: "bins (absolute)"
  };

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

    updatePipeline(leftPipeline);
    updatePipeline(rightPipeline);
  });

  $: sampleA = rawA.slice(0);
  $: sampleB = rawB.slice(0);

  $: generator.primaryData = sampleA || [];
  $: generator.secondaryData = sampleB || [];

  $: samplingTotal.set(sampleA.length);

  function startSampling() {
    return window.setInterval(async () => {
      const responseA = await sample("left");
      const jsonA = await responseA.json();

      const responseB = await sample("right");
      const jsonB = await responseB.json();

      rawA = rawA.concat(jsonA.sample);
      rawB = rawB.concat(jsonB.sample);
    }, samplingRateValue);
  }

  function hideTooltip() {
    hoveredPosition.set([-1, -1]);
  }
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="config" on:mouseenter={ hideTooltip }>
    <ViewConfig
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
    <ViewConfig
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
      dataset={ sampleA }
      bind:renderer={ leftPipeline.viewType }
    />
    <div class="vertical-line" style="min-height:{plotHeight}px;border-left:1px solid black;border-right:1px solid black">
      { #if showCenter }
        <DataView
          id={ "center" }
          width={ plotWidth }
          height={ plotHeight }
          orientation={ "center" }
          dataset={ sampleA }
          renderer={ "bins (delta)" }
        />
      { /if }
    </div>
    <DataView
      id={ "right" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "right" }
      dataset={ sampleB }
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
