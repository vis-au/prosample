<script lang="typescript">
  import { scaleLinear } from 'd3-scale';

  export let id: string;
  export let width: number = 100;
  export let height: number = 100;
  export let data: number[][] = [];
  export let radius: number = 5;
  export let color: (number: number) => string = () => "black";

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);
</script>

<svg id="{id}-canvas" class="canvas" width={ width } height={ height }>
  <g class="points">
    { #each data as point }
      <circle
        class="point"
        r={ radius }
        cx={ scaleX(point[0]) }
        cy={ scaleY(point[1]) }
        fill={ color(point[2] )}
      />
    { /each }
  </g>
</svg>

<style>
  svg.canvas {
    box-sizing: border-box;
  }

  svg.canvas circle.point {
    fill-opacity: 0.3;
  }
</style>


