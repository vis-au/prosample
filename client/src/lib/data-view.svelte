<script lang="typescript">
import { precisionPrefix } from "d3-format";

  import { scaleDiverging, scaleSequential, scaleSequentialLog } from "d3-scale";
  import { interpolatePiYG, interpolateViridis } from "d3-scale-chromatic";

  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import LegendViewer from "./legend-viewer.svelte";
  import ScatterplotGlView from "./scatterplot-view.svelte";
  import { leftPipeline, rightPipeline } from "./state/pipelines";
  import { selectedBins } from "./state/selected-bin";
  import { viewConfig } from "./state/view-config";
  import { generator, primaryBins, primaryData, secondaryBins, secondaryData } from "./util/bin-generator";
  import Alternatives from "./widgets/alternatives.svelte";
  import Histogram from "./widgets/histogram.svelte";
  import ZoomOverlay from "./zoom-overlay.svelte";


  export let id = "left";
  export let orientation: "left" | "right" | "center";
  export let width = 250;
  export let height = 100;
  export let zoomable = false;

  let useRelativeBins = "relative";
  $: $viewConfig.useRelativeDifferenceScale = useRelativeBins === "relative";

  const pipeline = orientation === "left"
    ? leftPipeline
    : orientation === "right" ? rightPipeline : null;

  $: dataset = orientation === "center"
    ? null
    : orientation === "left" ? $primaryData : $secondaryData;

  $: bins = orientation === "center"
    ? generator.getDifferenceBins($viewConfig.useRelativeDifferenceScale)
    : orientation === "left" ? $primaryBins : $secondaryBins;

  $: renderer = $pipeline?.viewType;
  $: color = orientation === "center"
    ? scaleDiverging(interpolatePiYG)
    : $pipeline.colorScaleType === "log"
      ? scaleSequentialLog(interpolateViridis)
      : scaleSequential(interpolateViridis);
  $: colorScaleType = pipeline !== null ? $pipeline.colorScaleType : null;

  const selectedDimensions = ["1", "2", "3"];

  $: selectedIds = orientation === "left"
    ? $selectedBins.map(bin => generator.getPrimaryBin([bin.x, bin.y, -1])?.map(item => item[2])).flat()
    : orientation === "right"
      ? $selectedBins.map(bin => generator.getSecondaryBin([bin.x, bin.y, -1])?.map(item => item[2])).flat()
      : [];

  $: selectedData = orientation === "left"
    ? generator.getPrimaryDataList(selectedIds).filter(d => !!d)
    : orientation === "right"
      ? generator.getSecondaryDataList(selectedIds).filter(d => !!d)
      : [];

  $: tabularSelectedData = selectedData.map(d => {
    let datum = {};
    selectedDimensions.forEach(dim => datum[dim] = d[+dim]);
    return datum;
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
      bind:colorScaleType={ colorScaleType }
    />
  { /if }
  { #if pipeline !== null }
    <Alternatives
      name="{orientation}-renderer"
      alternatives={ ["bins (absolute)", "scatterplot"] }
      bind:activeAlternative={ $pipeline.viewType }
    />
  { #if selectedDimensions.length > 0 && tabularSelectedData.length > 0 }
    { #each selectedDimensions as dim }
      <Histogram
        id={ `${orientation}-${dim}-histogram` }
        data={ tabularSelectedData }
        dimension={ dim }
        height={30}
        width={100}
        showTitle={ false }
      />
    { /each }
  { /if }
  { :else }
    <Alternatives
      name="relative-bins"
      alternatives={ [ "relative", "absolute" ] }
      bind:activeAlternative={ useRelativeBins }
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