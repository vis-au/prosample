<script lang="typescript">
  import { onMount } from 'svelte';
  import { Deck, OrthographicView } from '@deck.gl/core';
  import { ScatterplotLayer } from '@deck.gl/layers';

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

    window.setTimeout(() => {
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
          controller: true,
          x: 0,
          y: 0,
          width: width,
          height: height,
        })
      ];

      generateDeckComponent();
    }, 0);
  });

  function generateDeckComponent() {
    const style = orientation === "left"
      ? { left: "0" }
      : { right: "0" };

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

<canvas bind:this={ canvasElement } class="scatterplot-gl-view"></canvas>