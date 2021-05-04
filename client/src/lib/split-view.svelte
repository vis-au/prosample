<script lang="typescript">
  import { range } from 'd3-array';
  import { scaleSequential } from 'd3-scale';
  import { interpolateViridis } from 'd3-scale-chromatic';
  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import ScatterplotGlView from "./scatterplot-gl-view.svelte";

  let innerWidth = 500;
  let innerHeight = 350;
  let margin = 1;

  $: plotWidth = innerWidth / 2;
  $: plotHeight = innerHeight - 57;
  $: color = scaleSequential(interpolateViridis);

  // [random x, random y, random attribute]
  const randomData = range(0, 1000000).map(() => [Math.random()**2, Math.random(), Math.random()]);
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="left">
    <BinnedScatterplotView id={ "left" }
      width={ plotWidth - margin }
      height={ plotHeight }
      data={ randomData }
      color={ color }
    />
  </div>
  <div class="right">
    <ScatterplotGlView
      id={ "right" }
      orientation={ "right" }
      radius={ 1 }
      width={ plotWidth - margin }
      height={ plotHeight }
      data={ randomData }
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
