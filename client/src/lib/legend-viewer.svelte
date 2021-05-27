<script lang="typescript">
  import { range } from "d3-array";
  import type { ScaleDiverging, ScaleSequential } from "d3-scale";
  import { scaleLinear } from "d3-scale";
  import type { BinColorScaleType } from "./util/types";

  export let id = "id";
  export let color: ScaleSequential<string, never> | ScaleDiverging<string, never>;
  export let title: string;
  export let left = 0;
  export let top = 0;
  export let width = 200;
  export let height = 25;
  export let margin = 3;
  export let blockSize: number;
  export let steps = 10;
  export let isVertical = false;
  export let colorScaleType: BinColorScaleType = null;

  const colorScaleTypes = ["log", "linear"] as BinColorScaleType[];

  const segmentWidth = width / (steps + 1);
  $: scaleX = scaleLinear()
    .domain([0, steps])
    .range([margin, width - margin]);

  $: scaleY = scaleLinear()
    .domain([0, steps])
    .range([margin, height - margin]);

  $: domain = color.domain();
  $: values = range(domain[0], domain[domain.length - 1], Math.abs(domain[0] - domain[domain.length - 1]) / steps);
</script>

<svg
  id="{id}-legend-canvas"
  class="legend"
  width={ width }
  height={ height }
  style="left: {left}px; top: {top}px"
  >
  <g class="color">
    <text class="legend-title" x={ margin } y={ margin }>{ title }</text>
    <g class="values" transform="translate(0,{22})">
      { #each values as value, i }
        <rect
          class="value"
          width={ segmentWidth }
          height={ blockSize }
          x={ isVertical ? 0 : scaleX(i) }
          y={ isVertical ? scaleY(i) : 0 }
          fill={ color(value) }
        />
      { /each }
    </g>
    <text class="low" x={ margin } y={ height - 17 - margin }>low</text>
    <text class="high" x={ width-margin } y={ height - 17 - margin }>high</text>
  </g>
  { #if colorScaleType !== null }
    <g class="scale-type" transform="translate({ width - colorScaleTypes.length * 15 + margin }, 15)">
      { #each colorScaleTypes as type, index }
        <circle
          class="scale-type-toggle"
          cx={index * 15}
          cy=0
          r=5
          fill={ colorScaleType === type ? "black" : "white" }
          stroke="black"
          on:click={ () => colorScaleType = type }>
          <title>{ type }</title>
        </circle>
      { /each }
    </g>
  { /if }
</svg>

<style>
  svg.legend {
    position: absolute;
    background: rgba(255, 255, 255, 0.73);
    shape-rendering: crispEdges;
  }

  svg.legend rect.value {
    stroke: white;
    stroke-width: 0.25px;
  }

  svg.legend text {
    fill: black;
    font-size: 15px;
    transform: translateY(15px);
  }
  svg.legend text.legend-title {
    font-weight: bold;
  }
  svg.legend text.high {
    text-anchor: end;
  }

  svg.legend .scale-type circle.scale-type-toggle {
    cursor: pointer;
  }
</style>