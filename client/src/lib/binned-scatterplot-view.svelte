<script lang="typescript">
  import { max, min } from 'd3-array';
  import type { HexbinBin } from 'd3-hexbin';
  import { scaleLinear } from 'd3-scale';
  import { afterUpdate } from 'svelte';
import { update_await_block_branch } from 'svelte/internal';
  import { hoveredPosition } from './state/hovered-position';
import { selectedBins } from './state/selected-bin';
  import { hexagon, hexbinning } from './util/bin-generator';

  export let id: string;
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let bins: HexbinBin<[number, number]>[];

  let canvasElement;
  let overlayCanvasElement;
  let hovered: [number, number] = [-1, -1];
  let selected: HexbinBin<[number, number]>[] = [];

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  hoveredPosition.subscribe(value => {
    hovered = value;
    renderOverlay();
  });

  selectedBins.subscribe(value => {
    selected = value;
    renderOverlay();
  });


  function renderDataBins(ctx: any, hexagonPath: any) {
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

  function renderSelectedBins(ctx: any, hexagonPath: any) {
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255,255,255,1)";
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = 4;
    selected.forEach(bin => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function onHover(event) {
    const rect = event.target.getBoundingClientRect();
    const x = (event.clientX - rect.left) / width;
    const y = (event.clientY - rect.top) / height;

    hoveredPosition.set([ x, y ]);
  }

  function onClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = (event.clientX - rect.left) / width;
    const y = (event.clientY - rect.top) / height;

    const clickedBin = hexbinning([[x,y]])[0];
    const selectedBin = selected.find(bin => bin.x === clickedBin.x && bin.y === clickedBin.y);
    const selectedIndex = selected.indexOf(selectedBin);

    selectedBins.update(currentlySelectedBins => {
      if (selectedIndex > 0) {
        currentlySelectedBins.splice(selectedIndex, 1);
        return currentlySelectedBins;
      } else {
        return currentlySelectedBins = currentlySelectedBins.concat([clickedBin]);
      }
    });
  }

  function renderOverlay() {
    if (!overlayCanvasElement) {
      return;
    }

    hexbinning
      .x(d => scaleX(d[0]))
      .y(d => scaleY(d[1]));

    const ctx = overlayCanvasElement.getContext("2d");
    const hexagonPath = new Path2D(hexagon);
    ctx.clearRect(0, 0, width, height);

    renderHoveredBin(ctx, hexagonPath);
    renderSelectedBins(ctx, hexagonPath);
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
    const maxCount = (max(bins, d => (d as Array<any>).length) || 0);
    color.domain([minCount, maxCount]);

    ctx.clearRect(0, 0, width, height);

    renderDataBins(ctx, hexagonPath);
    renderOverlay();
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
  <canvas
    id="{id}-interaction-canvas"
    class="interaction-canvas"
    width={ width }
    height={ height }
    on:mousemove={ onHover }
    on:click={ onClick }
    bind:this={ overlayCanvasElement }
  />
</div>

<style>
  div.binned-scatterplot-view {
    position: relative;
  }
  div.binned-scatterplot-view canvas {
    position: absolute;
  }
</style>
