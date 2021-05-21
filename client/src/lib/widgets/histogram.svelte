<script lang="typescript">
  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let width = 100;
  export let height = 100;
  export let data: Array<any>;
  export let dimension: string;

  $: histogram = {
    $schema: "https://vega.github.io/schema/vega-lite/v5.json",
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
        aggregate: "count"
      }
    }
  }
</script>

<VegaLitePlot id="dimension-histogram" spec={ histogram } />