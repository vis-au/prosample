<script lang="typescript">
  import { max, min } from 'd3-array';
  import type { HexbinBin } from 'd3-hexbin';
  import { scaleLinear } from 'd3-scale';
  import { afterUpdate } from 'svelte';
  import { hoveredPosition } from './state/hovered-position';
  import { hexagon, hexbinning } from './util/bin-generator';

  export let id: string;
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let bins: HexbinBin<[number, number]>[];

  let canvasElement;
  let hovered: [number, number] = [-1, -1];

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  hoveredPosition.subscribe(value => {
    hovered = value;
    render();
  });


  function renderDataBins(ctx: any, bins: any[], hexagonPath: any) {
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
  }

  function renderHoveredBin(ctx: any, hexagonPath: any) {
    const hoveredBin = hexbinning([ hovered ])[0];

    if (!hoveredBin) {
      return;
    }

    ctx.beginPath();
    ctx.translate(hoveredBin.x, hoveredBin.y);
    ctx.strokeStyle = "rgba(255,255,255,1)";
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = 4;
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-hoveredBin.x, -hoveredBin.y);
    ctx.closePath();
  }

  function onHover(event) {
    const rect = event.target.getBoundingClientRect();
    const x = (event.clientX - rect.left) / width;
    const y = (event.clientY - rect.top) / height;

    hoveredPosition.set([ x, y ]);
  }

  function render() {
    if (canvasElement === undefined) {
      return;
    }

    hexbinning
      .x(d => scaleX(d[0]))
      .y(d => scaleY(d[1]));

    const ctx = canvasElement.getContext("2d");
    const hexagonPath = new Path2D(hexagon);

    const minCount = (min(bins, d => (d as Array<any>).length) || 0);
    const maxCount = (max(bins, d => (d as Array<any>).length) || 0);
    color.domain([minCount, maxCount]);

    ctx.clearRect(0, 0, width, height);

    renderDataBins(ctx, bins, hexagonPath);
    renderHoveredBin(ctx, hexagonPath);
  }

  afterUpdate(render);

</script>

<canvas
  id="{id}-bins-canvas"
  class="bins-canvas"
  width={ width }
  height={ height }
  bind:this={ canvasElement }
  on:mousemove={ onHover }
/>
