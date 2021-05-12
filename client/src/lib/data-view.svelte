<script lang="typescript">
  import { scaleSequential } from "d3-scale";
  import { interpolatePiYG, interpolateViridis } from "d3-scale-chromatic";
  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import LegendViewer from "./legend-viewer.svelte";
  import ScatterplotGlView from "./scatterplot-gl-view.svelte";
  import type { ViewType } from "./util/types";
  import ZoomOverlay from "./zoom-overlay.svelte";

  export let renderer: ViewType = "scatterplot";
  export let id = "left";
  export let orientation: "left" | "right" | "center" = "left";
  export let width = 250;
  export let height = 100;
  export let primaryDataset: number[][] = [];
  export let secondaryDataset: number[][] = [];
  export let zoomable: boolean = false;

  $: color = renderer !== "bins (delta)"
    ? scaleSequential(interpolateViridis)
    : scaleSequential(interpolatePiYG);
</script>

<div class="data-view" style="width: {width}px; height: {height}px">
  { #if renderer === "scatterplot"}
    <ScatterplotGlView
      { id }
      { orientation }
      radius={ 1 }
      { width }
      { height }
      data={ primaryDataset }
    />
  { :else if renderer === "bins (absolute)" }
    <BinnedScatterplotView
      { id }
      { width }
      { height }
      { color }
      data={ primaryDataset }
    />
  { :else if renderer === "bins (delta)" }
    <BinnedScatterplotView
      { id }
      { width }
      { height }
      { color }
      data={ primaryDataset }
      differenceData={ secondaryDataset }
    />
  { /if }

  { #if zoomable }
    <ZoomOverlay
      id={ id }
      orientation={ orientation }
      width={ width }
      height={ height }
    />
  { /if }

  { #if renderer !== "scatterplot" }
    <LegendViewer
      { id }
      { color }
      title={ "Density" }
      left={ width - 210 }
      top={ height - 60 }
      height={ 50 }
      blockSize={ 10 }
      steps={ 11 }
      width={ 200 }
    />
  { /if }
</div>

<style>
  div.data-view {
    position: relative;
  }
</style>