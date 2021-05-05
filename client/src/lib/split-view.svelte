<script lang="typescript">
  import { range } from 'd3-array';
  import ConfigWidget from './config-widget.svelte';
  import DataView from './data-view.svelte';
  import type { PipelineConfig } from './types';

  let innerWidth = 500;
  let innerHeight = 350;
  let margin = 1;

  $: plotWidth = innerWidth / 2 - 1;
  $: plotHeight = innerHeight - 130;

  const leftPipeline: PipelineConfig = {
    linearization: "knn",
    selection: "first",
    subdivision: "equal attribute",
    viewType: "bins (delta)"
  };

  const rightPipeline: PipelineConfig = {
    linearization: "knn",
    selection: "first",
    subdivision: "equal attribute",
    viewType: "scatterplot"
  };

  $: console.log(leftPipeline);
  $: console.log(rightPipeline);

  // [random x, random y, random attribute]
  const randomDataA = range(0, 100000).map(() => [Math.random()**2, Math.random(), Math.random()]);
  const randomDataB = range(0, 100000).map(() => [Math.random(), Math.random()**2, Math.random()]);
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="left">
    <ConfigWidget
      id="A"
      bind:selectedViewType={ leftPipeline.viewType }
      bind:selectedSubdivisionType={ leftPipeline.subdivision }
      bind:selectedLinearizationType={ leftPipeline.linearization }
      bind:selectedSelectionType={ leftPipeline.selection }
    />
    <DataView
      id={ "left" }
      width={ plotWidth - margin }
      height={ plotHeight }
      orientation={ "left" }
      primaryDataset={ randomDataA }
      secondaryDataset={ randomDataB }
      bind:renderer={ leftPipeline.viewType }
    />
  </div>
  <div class="right">
    <ConfigWidget
      id="B"
      bind:selectedViewType={ rightPipeline.viewType }
      bind:selectedSubdivisionType={ rightPipeline.subdivision }
      bind:selectedLinearizationType={ rightPipeline.linearization }
      bind:selectedSelectionType={ rightPipeline.selection }
    />
    <DataView
      id={ "right" }
      width={ plotWidth - margin }
      height={ plotHeight }
      orientation={ "right" }
      primaryDataset={ randomDataB }
      secondaryDataset={ randomDataA }
      bind:renderer={ rightPipeline.viewType }
    />
  </div>
</div>

<style>
  div.split-view {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
  div.split-view div {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
</style>
