<script lang="typescript">
  import { onMount } from 'svelte';
  import { max } from 'd3-array';
  import { scaleLinear } from 'd3-scale';
  import { hexbin } from 'd3-hexbin';
  import { select } from 'd3-selection';

  export let id: string;
  export let data: number[][];
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let binSize: number = 10;

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  const hexbinning = hexbin<[number, number]>()
    .radius(binSize);

  let canvasElement;

  onMount(async () => {
    window.setTimeout(() => {
      hexbinning
        .x(d => scaleX(d[0]))
        .y(d => scaleY(d[1]));

      const bins = hexbinning(data.map(d => [d[0], d[1]]));
      const hexagon = hexbinning.hexagon();
      const hexagonPath = new Path2D(hexagon);

      const ctx = canvasElement.getContext("2d");

      color.domain([0, (max(bins, d => (d as Array<any>).length) || 0) / 2]);

      ctx.clearRect(0, 0, width, height);
      ctx.beginPath();
      bins.forEach(bin => {
        ctx.translate(bin.x, bin.y);
        ctx.fillStyle = color(bin.length);
        ctx.strokeStyle="rgba(255,255,255,1)";
        ctx.lineWidth = 2;
        ctx.stroke(hexagonPath);
        ctx.fill(hexagonPath);
        ctx.translate(-bin.x, -bin.y);
      });
      ctx.closePath();
    }, 0);
  });
</script>

<canvas id="{id}-bins-canvas" class="bins-canvas" bind:this={ canvasElement } width={ width } height={ height }></canvas>

<style>
  canvas.bins-canvas {
    border: 1px solid black;
    box-sizing: border-box;
  }
</style>