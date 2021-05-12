<script lang="typescript">
  import type { HexbinBin } from "d3-hexbin";
  import { scaleSequential } from "d3-scale";
  import { interpolatePiYG, interpolateViridis } from "d3-scale-chromatic";

  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import LegendViewer from "./legend-viewer.svelte";
  import ScatterplotGlView from "./scatterplot-gl-view.svelte";
  import { generator, primaryBins, secondaryBins } from "./util/bin-generator";
  import type { ViewType } from "./util/types";
  import ZoomOverlay from "./zoom-overlay.svelte";


  export let renderer: ViewType = "scatterplot";
  export let id = "left";
  export let orientation: "left" | "right" | "center" = "left";
  export let width = 250;
  export let height = 100;
  export let dataset: number[][];
  export let zoomable: boolean = false;

  $: color = renderer !== "bins (delta)"
    ? scaleSequential(interpolateViridis)
    : scaleSequential(interpolatePiYG);

  let bins: HexbinBin<[number, number]>[] = [];

  primaryBins.subscribe(value => {
    if (renderer === "bins (delta)") {
      bins = generator.getDifferenceBins();
    } else {
      if (orientation === "left") {
        bins = value;
      }
    }
  });
  secondaryBins.subscribe(value => {
    if (renderer === "bins (delta)") {
      bins = generator.getDifferenceBins();
    } else {
      if (orientation === "right") {
        bins = value;
      }
    }
  });
</script>

<div class="data-view" style="width: {width}px; height: {height}px">
  { #if renderer === "scatterplot"}
    <ScatterplotGlView
      { id }
      { orientation }
      radius={ 1 }
      { width }
      { height }
      data={ dataset }
    />
  { :else }
    <BinnedScatterplotView
      { id }
      { width }
      { height }
      { color }
      { bins }
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