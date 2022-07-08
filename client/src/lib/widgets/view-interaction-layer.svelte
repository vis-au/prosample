<script lang="typescript">
  import { brush } from "d3";
  import { select } from "d3-selection";
  import type { Selection } from "d3-selection";
  import { zoom, zoomTransform } from "d3-zoom";
  import type { D3ZoomEvent } from "d3-zoom";
  import { afterUpdate, onMount } from "svelte";

  import { hoveredPosition } from "$lib/state/hovered-position";
  import { interactionMode } from "$lib/state/interaction-mode";
  import { selectedBins } from "$lib/state/selected-bin";
  import { currentTransform, isZooming } from "$lib/state/zoom";
  import { hexbinning } from "$lib/util/bin-generator";
  import { scaleX, scaleY } from "$lib/state/scales";

  export let id: string;
  export let width: number;
  export let height: number;
  export let color = "rgba(255,255,255,1)";
  export let lineWidth = 4;

  let zoomCanvas: HTMLCanvasElement;

  const zoomBehavior = zoom()
    .scaleExtent([0.75, 10])
    .on("start", () => $isZooming = true)
    .on("zoom", onZoom)
    .on("end", () => $isZooming = false);

  const brushBehavior = brush();

  function onZoom(event: D3ZoomEvent<Element, void>) {
    if (event.sourceEvent === null) {
      return;
    }

    $currentTransform = event.transform;
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
    const canvas = select(zoomCanvas);
    canvas.call(zoomBehavior);
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
  <canvas
    class="zoom-canvas"
    width={ width }
    height={ height }
    on:mousemove={ onHover }
    on:click={ onClick }
    bind:this={ zoomCanvas }
    style="display: {$interactionMode === "zoom" ? "block" : "none"}"
  />
  <svg
    class="brush-canvas"
    width={ width }
    height={ height }
    on:mousemove={ onHover }
    on:click={ onClick }
    style="display: {$interactionMode === "brush" ? "block" : "none"}"
  />
</div>

<style>
  div.interaction-canvas {
    position: absolute;
  }
  div.interaction-canvas canvas {
    position: absolute;
  }
</style>