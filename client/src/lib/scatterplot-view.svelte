<script lang="typescript">
  import { rgb } from "d3-color";
  import { scaleSequentialLog } from 'd3-scale';
  import { selectAll } from 'd3-selection';
  import { afterUpdate, onMount } from 'svelte';
  import { Deck, OrthographicView } from '@deck.gl/core';
  import { ScatterplotLayer } from '@deck.gl/layers';

  import ViewInteractionLayer from './widgets/view-interaction-layer.svelte';
  import { scaleX, scaleY } from './state/scales';
  import { globalViewConfig } from "./state/view-config";
  import { sequentialScheme } from "./state/color-schemes";
  import { getExtent } from "./state/data";

  export let id = "deck-gl-scatterplot";
  export let data: number[][] = [];
  export let width = 100;
  export let height = 50;
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

    const {x, y, color} = $globalViewConfig.encoding;
    const scaleColor = scaleSequentialLog($sequentialScheme).domain(getExtent(color));

    layers = [
      new ScatterplotLayer({
        id: `${id}-layer`,
        getPosition: d => [$scaleX(d[x]), $scaleY(d[y])],
        getFillColor: d => {
          const c = rgb(scaleColor(d[color]));
          return [c.r, c.g, c.b]
        },
        getRadius: 2,
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
    const style = orientation === "left"
      ? { left: "0", border: "none", position: "" }
      : { right: "0", border: "none", position: "" };

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
  <canvas
    id="{id}-scatterplot-gl-view-canvas"
    class="scatterplot-gl-view"
    {width}
    {height}
    bind:this={ canvasElement } />

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