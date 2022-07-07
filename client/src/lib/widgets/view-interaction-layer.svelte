<script lang="typescript">
  import { brush } from "d3-brush";
  import type { D3BrushEvent } from "d3-brush";
  import { select } from "d3-selection";
  import type { Selection } from "d3-selection";
  import { zoom, zoomTransform } from "d3-zoom";
  import type { D3ZoomEvent } from "d3-zoom";
  import { afterUpdate, onMount } from "svelte";

  import { interactionMode } from "$lib/state/interaction-mode";
  import { selectedBins } from "$lib/state/selected-bin";
  import { currentTransform } from "$lib/state/zoom";
  import { hexbinning } from "$lib/util/bin-generator";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { cancelSteering, steer } from "$lib/util/requests";
  import { steeringFilters } from "$lib/state/steering-filters";
  import { hoveredPosition } from "$lib/state/hovered-position";

  export let id: string;
  export let width: number;
  export let height: number;
  export let color = "rgba(255,255,255,1)";
  export let lineWidth = 4;

  let zoomCanvas: HTMLCanvasElement;
  let brushCanvas: SVGElement;

  let isBrushing = false;
  let isZooming = false;

  const zoomBehavior = zoom()
    .scaleExtent([0.75, 10])
    .on("start", () => isZooming = true)
    .on("zoom", onZoom)
    .on("end", () => isZooming = false);

  const brushBehavior = brush()
    .on("start", () => isBrushing = true)
    .on("end", onBrushEnd);

  function onZoom(event: D3ZoomEvent<Element, void>) {
    if (event.sourceEvent === null) {
      return true;
    }

    $currentTransform = event.transform;
  }

  function onBrushEnd(event: D3BrushEvent<Element>) {
    const selection = event.selection;

    if (selection === null) {
      $steeringFilters.x = null;
      $steeringFilters.y = null;
      cancelSteering();
    } else {
      const [[minX, minY], [maxX, maxY]] = selection as [[number, number], [number, number]];

      $steeringFilters.x = {
        dimension: "1",
        min: $scaleX.invert($currentTransform.invertX(minX)),
        max: $scaleX.invert($currentTransform.invertX(maxX))
      };
      $steeringFilters.y = {
        dimension: "2",
        min: $scaleY.invert($currentTransform.invertY(minY)),
        max: $scaleY.invert($currentTransform.invertY(maxY))
      };

      steer($steeringFilters.x);
      steer($steeringFilters.y);
    }

    isBrushing = false;
  }

  function onHover(event) {
    const rect = event.target.getBoundingClientRect();
    const x = $scaleX.invert($currentTransform.invertX(event.clientX - rect.left));
    const y = $scaleY.invert($currentTransform.invertY(event.clientY - rect.top));

    hoveredPosition.set([ x, y ]);
  }

  function onClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = $scaleX.invert($currentTransform.invertX(event.clientX - rect.left));
    const y = $scaleY.invert($currentTransform.invertY(event.clientY - rect.top));

    const clickedBin = hexbinning([[x,y,-1]])[0];
    const selectedBin = $selectedBins.find(bin => bin.x === clickedBin.x && bin.y === clickedBin.y);
    const selectedIndex = $selectedBins.indexOf(selectedBin);

    selectedBins.update(currentlySelectedBins => {
      if (selectedIndex > 0) {
        currentlySelectedBins.splice(selectedIndex, 1);
        return currentlySelectedBins;
      } else {
        return currentlySelectedBins = currentlySelectedBins.concat([clickedBin]);
      }
    });
  }

  function renderHoveredBin(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    const hoveredBin = hexbinning([[ ...$hoveredPosition, -1]])[0];

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

  function renderSelectedBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    $selectedBins.forEach(bin => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function render() {
    if (!zoomCanvas) {
      return;
    }

    const hexagonPath = new Path2D(hexbinning.hexagon());
    const ctx = zoomCanvas.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    renderHoveredBin(ctx, hexagonPath);
    renderSelectedBins(ctx, hexagonPath);
  }

  onMount(() => {
    window.setTimeout(() => {
      const zoom = select(zoomCanvas);
      zoom.call(zoomBehavior);
      const brushSvg = select(brushCanvas);
      brushSvg.call(brushBehavior);
    }, 100);
  });

  afterUpdate(() => {
    const canvas = select(zoomCanvas) as Selection<Element, unknown, any, any>;
    const myZoom = zoomTransform(zoomCanvas);
    if (JSON.stringify(myZoom) !== JSON.stringify($currentTransform)) {
      zoomBehavior.transform(canvas, $currentTransform);
    }

    render();
  });
</script>

<div id="{id}-interaction-canvas" class="interaction-canvas">
  <svg class="active-brush" width={ width } height={ height }>
    {#if $steeringFilters.x && $steeringFilters.y}
      <rect
        class="steering-filter"
        x={ $currentTransform.applyX($scaleX($steeringFilters.x.min))}
        y={ $currentTransform.applyY($scaleY($steeringFilters.y.min))}
        width={
          $currentTransform.applyX($scaleX($steeringFilters.x.max))
          -
          $currentTransform.applyX($scaleX($steeringFilters.x.min))
        }
        height={
          $currentTransform.applyY($scaleY($steeringFilters.y.max))
          -
          $currentTransform.applyY($scaleY($steeringFilters.y.min))
        }
      />
    {/if}
  </svg>
  <svg
    class="brush-canvas {isBrushing ? "brushing" : ""}"
    width={ width }
    height={ height }
    on:mousemove={ onHover }
    on:click={ onClick }
    bind:this={ brushCanvas }
    style="display: {$interactionMode === "brush" ? "block" : "none"}">
  </svg>
  <canvas
    id="{id}-interaction-canvas"
    class="interaction-canvas {isZooming ? "zooming" : ""}"
    width={ width }
    height={ height }
    on:mousemove={ onHover }
    on:click={ onClick }
    bind:this={ zoomCanvas }
  />
</div>

<style>
  div.interaction-canvas {
    position: absolute;
  }
  div.interaction-canvas canvas,
  div.interaction-canvas svg {
    position: absolute;
  }
  .zooming {
    cursor: move;
  }
  svg.active-brush .steering-filter {
    fill: transparent;
    stroke: black;
    stroke-width: 2px;
  }
  :global(svg.brush-canvas .selection,
  svg.brush-canvas .handle) {
    display: none;
  }
  :global(svg.brush-canvas.brushing .selection,
  svg.brush-canvas.brushing .handle) {
    display: block;
  }
</style>