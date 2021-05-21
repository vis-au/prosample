<script lang="typescript">
  import type { HexbinBin } from "d3-hexbin";
  import { scaleDiverging, scaleSequential } from "d3-scale";
  import { interpolatePiYG, interpolateViridis } from "d3-scale-chromatic";

  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import LegendViewer from "./legend-viewer.svelte";
  import ScatterplotGlView from "./scatterplot-gl-view.svelte";
  import { leftPipeline, rightPipeline } from "./state/pipelines";
  import { generator, primaryBins, secondaryBins } from "./util/bin-generator";
  import Alternatives from "./widgets/alternatives.svelte";
  import ZoomOverlay from "./zoom-overlay.svelte";


  export let id = "left";
  export let orientation: "left" | "right" | "center";
  export let width = 250;
  export let height = 100;
  export let dataset: number[][];
  export let zoomable: boolean = false;

  const pipeline = orientation === "left"
    ? leftPipeline
    : orientation === "right" ? rightPipeline : null;

  $: renderer = $pipeline?.viewType;
  $: color = renderer === "bins (delta)"
    ? scaleDiverging(interpolatePiYG)
    : scaleSequential(interpolateViridis);

  let bins: HexbinBin<[number, number]>[] = [];

  primaryBins.subscribe(value => {
    if (renderer === "scatterplot") {
      return;
    } else if (renderer === "bins (delta)") {
      bins = generator.getDifferenceBins();
    } else {
      if (orientation === "left") {
        bins = value;
      }
    }
  });
  secondaryBins.subscribe(value => {
    if (renderer === "scatterplot") {
      return;
    } else if (renderer === "bins (delta)") {
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
  { #if pipeline !== null }
    <Alternatives
      name="{orientation}-renderer"
      alternatives={ ["bins (absolute)", "scatterplot"] }
      bind:activeAlternative={ $pipeline.viewType }
    />
  { /if }
</div>

<style>
  div.data-view {
    position: relative;
  }
  :global(div.data-view .alternatives) {
    position: absolute;
    right: 10px;
    top: 10px;
  }
  :global(div.data-view .alternatives .alternative) {
    width: 10px;
    height: 10px;
    background: white;
    overflow: hidden;
    margin: 0 5px;
    border: 2px solid black;
    border-radius: 10px;
    cursor: pointer;
  }
  :global(div.data-view .alternatives .alternative.active) {
    background: black;
  }
  :global(div.data-view .alternatives .alternative > *) {
    display: none;
  }
</style>