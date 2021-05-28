<script lang="typescript">
  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let id: string;
  export let color: string;
  export let width = 100;
  export let height = 100;
  export let data: Record<string, unknown>[];
  export let dimension: string;
  export let showTitle = false;

  $: histogram = {
    $schema: "https://vega.github.io/schema/vega-lite/v5.1.0.json",
    data: {
      values: data
    },
    width: width,
    height: height,
    margin: "none",
    mark: "bar",
    encoding: {
      x: {
        bin: true,
        field: dimension
      },
      y: {
        aggregate: "count",
        title: null
      },
      color: {
        value: !color ? "#555" : color
      }
    }
  }

  $: showTitle ? "" : histogram.encoding.x["title"] = false;
</script>

<VegaLitePlot {id} spec={ histogram } />