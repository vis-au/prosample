<script lang="typescript">
  import { range } from "d3-array";
  import type { ScaleDiverging, ScaleSequential } from "d3-scale";
  import { scaleLinear } from "d3-scale";
  import { divergingScheme, divergingSchemes, sequentialScheme, sequentialSchemes } from "./state/color-schemes";
  import type { BinColorScaleType, Orientation } from "./util/types";

  export let id: Orientation;
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
    <g class="label left" transform="translate({margin},{blockSize + margin + 5})">
      <rect width=30 height=14 />
      <text class="low">{id === "center" ? "> left" : "low"}</text>
    </g>
    <g class="label right" transform="translate({width-margin},{blockSize + margin + 5})">
      <rect x={ -30 } width=30 height=14 />
      <text class="high">{id === "center" ? "> right" : "high"}</text>
    </g>
  </g>
  { #if colorScaleType !== null }
    <g class="scale-type" transform="translate({ width - colorScaleTypes.length * 15 + margin },{ height - 5 - margin})">
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
  <g class="color-scheme" transform="translate({margin},{ height - 12 - margin})">
    { #if id === "center" }
      { #each divergingSchemes as scheme, index }
        <rect
          x={ index * 12 }
          y={0}
          width={8}
          height={8}
          fill={ $divergingScheme === scheme ? "black" : "white"}
          stroke="black"
          on:click={ () => $divergingScheme = scheme }
        />
      { /each }
    { :else }
      { #each sequentialSchemes as scheme, index }
        <rect
          x={ index * 12 }
          y={0}
          width={8}
          height={8}
          fill={ $sequentialScheme === scheme ? "black" : "white"}
          stroke="black"
          on:click={ () => $sequentialScheme = scheme }
        />
      { /each }
    { /if }
  </g>
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

  svg.legend g.color g.label rect {
    fill: rgba(255,255,255,0.7);
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

  svg.legend g.color-scheme rect {
    cursor: pointer;
  }
</style>