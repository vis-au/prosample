<script lang="typescript">
  import { onMount } from 'svelte';
  import DataView from './data-view.svelte';
  import { samplingRate } from './state/sampling-rate';
  import { samplingAmount } from './state/sampling-amount';
  import { samplingTotal } from './state/sampling-total';
  import { progressionState } from './state/progression-state';
  import { leftPipeline, rightPipeline } from './state/pipelines';
  import { viewConfig } from './state/view-config';
  import { hoveredPosition } from './state/hovered-position';
  import { generator } from './util/bin-generator';
  import { sample, updatePipeline } from './util/requests';
  import { selectedDataset } from './util/selected-dataset';
  import type { PipelineConfig } from './util/types';
  import ViewConfig from './widgets/view-config.svelte';
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
  let currentDataset = "mountain_peaks";
  let leftConfiguration: PipelineConfig = null;
  let rightConfiguration: PipelineConfig = null;

  samplingRate.subscribe(value => samplingRateValue = value);
  samplingAmount.subscribe(value => samplingAmountValue = value);
  viewConfig.subscribe(value => showCenter = value.showCenter);
  selectedDataset.subscribe(value => currentDataset = value);
  leftPipeline.subscribe(value => leftConfiguration = value);
  rightPipeline.subscribe(value => rightConfiguration = value);

  $: plotWidth = innerWidth / (showCenter ? 3 : 2) - margin.horizontal;
  $: plotHeight = innerHeight - margin.vertical;
  $: viewConfig.set({ showCenter })

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

    updatePipeline(leftConfiguration).then(() => {
      leftPipeline.update(config => {
        config.ready = true;
        return config;
      });
    });
    updatePipeline(rightConfiguration).then(() => {
      rightPipeline.update(config => {
        config.ready = true;
        return config;
      });
    });
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
    <ViewConfig id="A" orientation="left" />
    <div class="center-config" style="min-width:{showCenter?plotWidth+margin.horizontal:50}px">
      <Toggle
        id="center-view-toggle"
        bind:active={ showCenter }
        activeText="-"
        passiveText="+"
        style="width:25px; height:25px; line-height:25px;"
      />
    </div>
    <ViewConfig id="B" orientation="right" />
  </div>
  <div class="data">
    <DataView
      id={ "left" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "left" }
      dataset={ sampleA }
    />
    <div class="vertical-line" style="min-height:{plotHeight}px;border-left:1px solid black;border-right:1px solid black">
      { #if showCenter }
        <DataView
          id={ "center" }
          width={ plotWidth }
          height={ plotHeight }
          orientation={ "center" }
          dataset={ sampleA }
        />
      { /if }
    </div>
    <DataView
      id={ "right" }
      width={ plotWidth }
      height={ plotHeight }
      orientation={ "right" }
      dataset={ sampleB }
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
