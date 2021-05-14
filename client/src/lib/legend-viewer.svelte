<script lang="typescript">
  import { range } from "d3-array";
  import type { ScaleSequential } from "d3-scale";
  import { scaleSequential, scaleLinear } from "d3-scale";
  import { interpolateViridis } from "d3-scale-chromatic";
  import { afterUpdate } from "svelte";

  export let id: string = "id";
  export let color: ScaleSequential<string, never> = scaleSequential(interpolateViridis);
  export let title: string;
  export let left: number = 0;
  export let top: number = 0;
  export let width: number = 200;
  export let height: number = 25;
  export let margin: number = 3;
  export let blockSize: number;
  export let steps: number = 10;
  export let isVertical: boolean = false;

  const segmentWidth = width / (steps + 1);
  $: scaleX = scaleLinear()
    .domain([0, steps])
    .range([margin, width - margin]);

  $: scaleY = scaleLinear()
    .domain([0, steps])
    .range([margin, height - margin]);

  let domain = [0, 1];

  $: values = range(domain[0], domain[1], Math.abs(domain[0] - domain[1]) / steps);

  afterUpdate(() => {
    domain = color.domain();
  });

</script>

<svg
  id="{id}-legend-canvas"
  class="legend"
  width={ width }
  height={ height }
  style="left: {left}px; top: {top}px"
  >
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
</style>