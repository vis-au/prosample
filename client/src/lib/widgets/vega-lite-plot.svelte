<script>
  import { afterUpdate } from "svelte";

  export let id;
  export let spec;

  let window;
  let vegaEmbed;

  afterUpdate(() => {
    vegaEmbed = window.vegaEmbed;
    if (vegaEmbed === undefined) {
      return;
    }
    vegaEmbed.embed(`#${id}-vega-container`, spec);
  });

</script>

<div id="{id}-vega-container"></div>

<svelte:head>
	<script src="https://cdn.jsdelivr.net/npm/vega"></script>
	<script src="https://cdn.jsdelivr.net/npm/vega-lite"></script>
	<script src="https://cdn.jsdelivr.net/npm/vega-embed"></script>
</svelte:head>