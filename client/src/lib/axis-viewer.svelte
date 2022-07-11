<script lang="typescript">
  import { axisRight, axisTop, format, select } from "d3";
  import type { ZoomTransform } from "d3";
  import { getExtent } from "./state/data";
  import { globalViewConfig } from "./state/view-config";
  import { dimensionNames } from "./state/data";
  import { scaleX, scaleY } from "./state/scales";
  import { currentTransform } from "./state/zoom";
  import { onMount } from "svelte";

  export let id: string;
  export let width: number;
  export let height: number;

  let xAxisContainer: SVGGElement;
  let yAxisContainer: SVGGElement;

  function drawAxes(t: ZoomTransform) {
    const scaleX1 = $scaleX.copy().domain(getExtent($globalViewConfig.encoding.x));
    const scaleY1 = $scaleY.copy().domain(getExtent($globalViewConfig.encoding.y))

    const xAxis = axisTop(t.rescaleX(scaleX1)).tickFormat(format(",.0f"));
    const yAxis = axisRight(t.rescaleY(scaleY1)).tickFormat(format(",.0f"));
    select(xAxisContainer).call(xAxis);
    select(yAxisContainer).call(yAxis);
  }

  currentTransform.subscribe(drawAxes);
  onMount(() => {
    window.setTimeout(() => drawAxes($currentTransform), 200);
  });
</script>

<svg {id} {width} {height}>
  <g class="axis x" bind:this={xAxisContainer} style="transform:translate(0,{height-1}px)">
    <text x={width/2}>{$dimensionNames[$globalViewConfig.encoding.x]}</text>
  </g>
  <g class="axis y" bind:this={yAxisContainer}>
    <text style="transform:translate(5px,{height/2}px)rotate(90deg);">{$dimensionNames[$globalViewConfig.encoding.y]}</text>
  </g>
</svg>

<style>
  svg {
    position: absolute;
  }
  svg g.axis text {
    fill: black;
    text-anchor: middle;
    font-weight: bold;
    font-size: 14px;
  }
</style>