<script lang="typescript">
  import { afterUpdate, onMount } from 'svelte';
  import { Deck, OrthographicView } from '@deck.gl/core';
  import { ScatterplotLayer } from '@deck.gl/layers';
  import { selectAll } from 'd3-selection';
import ViewInteractionLayer from './widgets/view-interaction-layer.svelte';

  export let id = "deck-gl-scatterplot";
  export let data: number[][] = [];
  export let width = 100;
  export let height = 50;
  export let radius = 5; // size of points
  export let orientation = "right"; // left or right side of the screen?

  const INITIAL_VIEW_STATE = {
    zoom: 0,
    minZoom: -1,
    maxZoom: 40,
    orthographic: true
  };

  let canvasElement;

  $: layers = [];
  $: views = [];

  onMount(() => {
    window.setInterval(() => {
      selectAll("div.deck-tooltip").remove()
    }, 1000);
  });

  afterUpdate(render);

  function render() {
    INITIAL_VIEW_STATE["target"] = [width / 2, height / 2, 0];

    layers = [
      new ScatterplotLayer({
        id: `${id}-layer`,
        getPosition: d => [d[0] * width, d[1] * height],
        getRadius: radius,
        getLineWidth: 0,
        opacity: 0.3,
        lineWidthUnits: "pixels",
        stroked: false,
        data: data,
      })
    ];

    views = [
      new OrthographicView({
        id: `${id}-view`,
        flipY: true,
        controller: false,
        x: 0,
        y: 0,
        width: width,
        height: height,
      })
    ];

    generateDeckComponent();
  }

  function generateDeckComponent() {
    const style: any = orientation === "left"
      ? { left: "0", border: "none" }
      : { right: "0", border: "none" };

    style.position = "relative";

    new Deck({
      id: id,
      canvas: canvasElement,
      width,
      height,
      views,
      layers,
      style,
      initialViewState: INITIAL_VIEW_STATE,
    });
  }
</script>

<div id="{id}-scatterplot-gl-view" class="scatterplot-gl-view">
  <canvas id="{id}-scatterplot-gl-view-canvas" class="scatterplot-gl-view" {width} {height} bind:this={ canvasElement }></canvas>

  <ViewInteractionLayer { id } { width } { height } color="black" lineWidth={1} />
</div>

<style>
  div.scatterplot-gl-view {
    position: relative;
  }
  div.scatterplot-gl-view canvas.scatterplot-gl-view {
    position: absolute;
  }
</style>