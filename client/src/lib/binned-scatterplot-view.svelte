<script lang="typescript">
  import { max, min } from 'd3-array';
  import type { HexbinBin } from 'd3-hexbin';
  import { scaleLinear } from 'd3-scale';
  import { afterUpdate } from 'svelte';
  import { hexagon, hexbinning } from './util/bin-generator';
  import ViewInteractionLayer from './widgets/view-interaction-layer.svelte';

  export let id: string;
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let bins: HexbinBin<[number, number]>[];

  let canvasElement;

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);


  function renderBins(ctx: any, hexagonPath: any) {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle="rgba(255,255,255,1)";
    ctx.lineWidth = 2;
    bins.forEach(bin => {
      ctx.translate(bin.x, bin.y);
      ctx.fillStyle = color(bin.length);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function render() {
    if (!canvasElement) {
      return;
    }

    hexbinning
      .x(d => scaleX(d[0]))
      .y(d => scaleY(d[1]));

    const ctx = canvasElement.getContext("2d");
    const hexagonPath = new Path2D(hexagon);

    const minCount = (min(bins, d => (d as Array<any>).length) || 0);
    const maxCount = (max(bins, d => (d as Array<any>).length) || 1);

    if (color.range().length === 3) {
      color.domain([minCount, 0, maxCount]);
    } else {
      color.domain([minCount, maxCount]);
    }

    renderBins(ctx, hexagonPath);
  }

  afterUpdate(render);
</script>

<div id="{id}-binned-scatterplot-view" class="binned-scatterplot-view">
  <canvas
    id="{id}-bins-canvas"
    class="bins-canvas"
    width={ width }
    height={ height }
    bind:this={ canvasElement }
  />
  <ViewInteractionLayer { id } { width } { height } />
</div>

<style>
  div.binned-scatterplot-view {
    position: relative;
  }
  div.binned-scatterplot-view canvas.bins-canvas {
    position: absolute;
  }
</style>
