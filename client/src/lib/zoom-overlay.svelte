<script lang="typescript">
  import { select } from "d3-selection";
  import type { D3ZoomEvent } from "d3-zoom";
  import { zoom } from "d3-zoom";
  import { onMount } from "svelte";

  export let id = "left";
  export let orientation = "left";
  export let width = 250;
  export let height = 100;

  const zoomBehavior = zoom()
    .scaleExtent([0.75, 10])
    .on("zoom", onZoom);

  function onZoom(event: D3ZoomEvent<Element, void>) {
    console.log(event.transform);
  }

  onMount(() => {
    const svg = select(`#${id}-zoom-overlay`);
    svg.call(zoomBehavior);
  });

</script>

<svg id="{id}-zoom-overlay" class="zoom-overlay { orientation }" width={ width } height={ height }></svg>

<style>
  .zoom-overlay {
    position: absolute;
    top: 0;
  }
  .zoom-overlay.left {
    left: 0;
  }
  .zoom-overlay.right {
    right: 0;
  }
</style>