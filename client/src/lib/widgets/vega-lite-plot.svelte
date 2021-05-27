<script lang="typescript">
  import { afterUpdate } from "svelte";

  export let id: string;
  export let spec: Record<string, unknown>;

  let vegaEmbed;

  afterUpdate(() => {
    vegaEmbed = (window as any).vegaEmbed;
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