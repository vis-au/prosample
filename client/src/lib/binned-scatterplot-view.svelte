<script lang="typescript">
  import { afterUpdate, onMount } from 'svelte';
  import { max, min } from 'd3-array';
  import { scaleLinear } from 'd3-scale';
  import { hexbin } from 'd3-hexbin';
  import { getDifferenceBins } from './difference-bins';

  export let id: string;
  export let data: number[][];
  export let differenceData: number[][];
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let binSize: number = 10;

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  const hexbinning = hexbin<[number, number]>()
    .radius(binSize);

  let canvasElement;

  afterUpdate(async () => {
    window.setTimeout(() => {
      hexbinning
        .x(d => scaleX(d[0]))
        .y(d => scaleY(d[1]));

      const bins = getBins();
      const hexagon = hexbinning.hexagon();
      const hexagonPath = new Path2D(hexagon);

      const ctx = canvasElement.getContext("2d");

      const minCount = (min(bins, d => (d as Array<any>).length) || 0);
      const maxCount = (max(bins, d => (d as Array<any>).length) || 0);
      color.domain([minCount, maxCount]);

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

  function getBins() {
    if (differenceData === undefined) {
      return hexbinning(data.map(d => [d[0], d[1]]));
    }

    const primaryBins = hexbinning(data.map(d => [d[0], d[1]]));
    const secondaryBins = hexbinning(differenceData.map(d => [d[0], d[1]]));

    return getDifferenceBins(primaryBins, secondaryBins);
  }
</script>

<canvas id="{id}-bins-canvas" class="bins-canvas" bind:this={ canvasElement } width={ width } height={ height }></canvas>

<style>
  canvas.bins-canvas {
    /* border: none;
    box-sizing: border-box; */
  }
</style>
