<script lang="typescript">
  import type { HexbinBin } from "d3-hexbin";
  import { scaleLinear } from "d3-scale";
  import { hoveredPosition } from "$lib/state/hovered-position";
  import { selectedBins } from "$lib/state/selected-bin";
  import { hexagon, hexbinning } from "$lib/util/bin-generator";
  import { afterUpdate } from "svelte";

  export let id: string;
  export let width: number;
  export let height: number;
  export let color: string = "rgba(255,255,255,1)";
  export let lineWidth: number = 4;

  let canvasElement;

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  let hovered: [number, number] = [-1, -1];
  let selected: HexbinBin<[number, number]>[] = [];

  hoveredPosition.subscribe(value => {
    hovered = value;
    render();
  });

  selectedBins.subscribe(value => {
    selected = value;
    render();
  });

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

  function renderHoveredBin(ctx: any, hexagonPath: any) {
    const hoveredBin = hexbinning([ hovered ])[0];

    if (!hoveredBin) {
      return;
    }

    ctx.beginPath();
    ctx.translate(hoveredBin.x, hoveredBin.y);
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-hoveredBin.x, -hoveredBin.y);
    ctx.closePath();
  }

  function renderSelectedBins(ctx: any, hexagonPath: any) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    selected.forEach(bin => {
      ctx.translate(bin.x, bin.y);
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

    const hexagonPath = new Path2D(hexagon);
    const ctx = canvasElement.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    renderHoveredBin(ctx, hexagonPath);
    renderSelectedBins(ctx, hexagonPath);
    console.log("ooph");
  }

  afterUpdate(render);
</script>

<canvas
  id="{id}-interaction-canvas"
  class="interaction-canvas"
  width={ width }
  height={ height }
  on:mousemove={ onHover }
  on:click={ onClick }
  bind:this={ canvasElement }
/>

<style>
  canvas.interaction-canvas {
    position: absolute;
  }
</style>