<script lang="typescript">
  import { range } from 'd3-array';
  import { scaleSequential } from 'd3-scale';
  import { interpolateViridis } from 'd3-scale-chromatic';
  import ConfigWidget from './config-widget.svelte';
  import DataView from './data-view.svelte';

  let innerWidth = 500;
  let innerHeight = 350;
  let margin = 1;

  $: plotWidth = innerWidth / 2;
  $: plotHeight = innerHeight - 125;
  $: color = scaleSequential(interpolateViridis);

  // [random x, random y, random attribute]
  const randomData = range(0, 1000000).map(() => [Math.random()**2, Math.random(), Math.random()]);
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="split-view">
  <div class="left">
    <ConfigWidget id="A" />
    <DataView
      id={ "left" }
      width={ plotWidth - margin }
      height={ plotHeight }
      orientation={ "left" }
      color={ color }
      data={ randomData }
      renderer={ "binned-scatterplot" }
    />
  </div>
  <div class="right">
    <ConfigWidget id="B" />
    <DataView
      id={ "right" }
      width={ plotWidth - margin }
      height={ plotHeight }
      orientation={ "right" }
      color={ color }
      data={ randomData }
      renderer={ "gl-scatterplot" }
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
