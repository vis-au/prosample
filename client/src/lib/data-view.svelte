<script lang="typescript">
  import { scaleSequential } from "d3-scale";
  import { interpolateViridis } from "d3-scale-chromatic";
  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import ScatterplotGlView from "./scatterplot-gl-view.svelte";
import type { ViewType } from "./types";
  import ZoomOverlay from "./zoom-overlay.svelte";

  export let renderer: ViewType = "scatterplot";
  export let id = "left";
  export let orientation: "left" | "right" = "left";
  export let width = 250;
  export let height = 100;
  export let data: number[][] = [];
  export let color = scaleSequential(interpolateViridis);
</script>

<div class="data-view">
  { #if renderer === "scatterplot"}
    <ScatterplotGlView
      { id }
      { orientation }
      radius={ 5 }
      { width }
      { height }
      { data }
    />
  { :else if renderer === "hexagonal bins" }
    <BinnedScatterplotView
      { id }
      { width }
      { height }
      { data }
      { color }
    />
  { /if }

  <ZoomOverlay
    id={ id }
    orientation={ orientation }
    width={ width }
    height={ height }
  />
</div>

<style>
  div.data-view {
    box-sizing: border-box;
    border: 1px solid black;
  }
</style>