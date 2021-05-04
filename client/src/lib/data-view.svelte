<script lang="typescript">
  import { scaleSequential } from "d3-scale";
  import { interpolateViridis } from "d3-scale-chromatic";
  import BinnedScatterplotView from "./binned-scatterplot-view.svelte";

  import ScatterplotGlView from "./scatterplot-gl-view.svelte";

  export let renderer: "gl-scatterplot" | "binned-scatterplot" = "gl-scatterplot";
  export let id = "left";
  export let orientation: "left" | "right" = "left";
  export let width = 250;
  export let height = 100;
  export let data: number[][] = [];
  export let color = scaleSequential(interpolateViridis);
</script>

<div class="data-view">
  { #if renderer === "gl-scatterplot"}
    <ScatterplotGlView
      id={ id }
      orientation={ orientation }
      radius={ 1 }
      width={ width }
      height={ height }
      data={ data }
    />
  { :else if renderer === "binned-scatterplot" }
    <BinnedScatterplotView
      id={ id }
      width={ width }
      height={ height }
      data={ data }
      color={ color }
    />
  { /if }
</div>