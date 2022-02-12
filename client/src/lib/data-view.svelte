<script lang="typescript">
  import { scaleDiverging, scaleSequential, scaleSequentialLog } from "d3-scale";
  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";
  import LegendViewer from "./legend-viewer.svelte";
  import ScatterplotGlView from "./scatterplot-view.svelte";
  import { divergingScheme, sequentialScheme } from "./state/color-schemes";
  import { leftView, rightView, globalViewConfig } from "./state/view-config";
  import { generator, primaryBins, primaryData, secondaryBins, secondaryData, selectedPrimaryIds,
    selectedSecondaryIds } from "./util/bin-generator";
  import Alternatives from "./widgets/alternatives.svelte";
  import Histogram from "./widgets/histogram.svelte";


  export let id = "left";
  export let orientation: "left" | "right" | "center";
  export let width = 250;
  export let height = 100;

  let useRelativeBins = "relative";
  $: $globalViewConfig.useRelativeDifferenceScale = useRelativeBins === "relative";

  const view = orientation === "left"
    ? leftView
    : orientation === "right" ? rightView : null;

  $: dataset = orientation === "center"
    ? null
    : orientation === "left" ? $primaryData : $secondaryData;

  $: bins = orientation === "center"
    ? generator.getDifferenceBins($globalViewConfig.useRelativeDifferenceScale)
    : orientation === "left" ? $primaryBins : $secondaryBins;

  $: renderer = $view?.viewType;
  $: color = orientation === "center"
    ? scaleDiverging($divergingScheme)
    : $view.colorScaleType === "log"
      ? scaleSequentialLog($sequentialScheme)
      : scaleSequential($sequentialScheme);
  let colorScaleType = view !== null ? $view.colorScaleType : null;
  $: view !== null ? $view.colorScaleType = colorScaleType : null;

  $: histogramColors = orientation === "left" ? [$divergingScheme(0.1)]
    : orientation === "right" ? [$divergingScheme(0.9)]
    : [$divergingScheme(0.1), $divergingScheme(0.9)];

  const selectedDimensions = ["3"];

  $: selectedData = orientation === "left"
    ? generator.getPrimaryDataList($selectedPrimaryIds).filter(d => !!d)
    : orientation === "right"
      ? generator.getSecondaryDataList($selectedSecondaryIds).filter(d => !!d)
        : generator.getPrimaryDataList($selectedPrimaryIds).filter(d => !!d)
            .concat(generator.getSecondaryDataList($selectedSecondaryIds).filter(d => !!d));

  $: tabularSelectedData = selectedData.map((d, i) => {
    let datum = {};
    selectedDimensions.forEach(dim => datum[dim] = d[+dim]);
    if (orientation === "center") {
      datum["orientation"] = i < $selectedPrimaryIds.length ? "left" : "right";
    }
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

  { #if renderer !== "scatterplot" }
    <LegendViewer
      id={ orientation }
      { color }
      title={ "Density" }
      left={ width - 210 }
      top={ height - 65 }
      height={ 55 }
      blockSize={ 10 }
      steps={ 11 }
      width={ 200 }
      bind:colorScaleType={ colorScaleType }
    />
  { /if }
  { #if view !== null }
    <Alternatives
      name="{orientation}-renderer"
      alternatives={ ["bins (absolute)", "scatterplot", "bins (ground truth)"] }
      bind:activeAlternative={ $view.viewType }
    />
  { :else }
    <Alternatives
      name="relative-bins"
      alternatives={ [ "relative", "absolute" ] }
      bind:activeAlternative={ useRelativeBins }
    />
  { /if }
  { #if selectedDimensions.length > 0 && tabularSelectedData.length > 0 }
    { #each selectedDimensions as dim }
      <Histogram
        id={ `${orientation}-${dim}-histogram` }
        data={ tabularSelectedData }
        dimension={ dim }
        groupDimension={ orientation === "center" ? "orientation" : null}
        colors={ histogramColors }
        height={30}
        width={100}
        showTitle={ false }
      />
    { /each }
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