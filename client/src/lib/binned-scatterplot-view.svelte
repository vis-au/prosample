<script lang="typescript">
  import { afterUpdate } from 'svelte';
  import { max, min } from 'd3-array';
  import { scaleLinear } from 'd3-scale';
  import { hexbin } from 'd3-hexbin';
  import { getDifferenceBins } from './util/difference-bins';

  export let id: string;
  export let data: number[][];
  export let differenceData: number[][];
  export let width: number = 100;
  export let height: number = 100;
  export let color: any;
  export let binSize: number = 10;
  export let hoveredPosition: [number, number] = [-1, -1];

  $: scaleX = scaleLinear().domain([0, 1]).range([0, width]);
  $: scaleY = scaleLinear().domain([0, 1]).range([0, height]);

  const hexbinning = hexbin<[number, number]>()
    .radius(binSize);

  const hexagon = hexbinning.hexagon();

  let canvasElement;

  function getBins() {
    if (differenceData === undefined) {
      return hexbinning(data.map(d => [d[0], d[1]]));
    }

    const primaryBins = hexbinning(data.map(d => [d[0], d[1]]));
    const secondaryBins = hexbinning(differenceData.map(d => [d[0], d[1]]));

    return getDifferenceBins(primaryBins, secondaryBins);
  }

  function renderDataBins(ctx: any, bins: any[], hexagonPath: any) {
    ctx.beginPath();
    bins.forEach(bin => {
      ctx.translate(bin.x, bin.y);
      ctx.fillStyle = color(bin.length);
      ctx.strokeStyle="rgba(255,255,255,1)";
      ctx.lineWidth = 2;
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function renderHoveredBin(ctx: any, bins: any[], hexagonPath: any) {
    const hoveredBin = hexbinning([ hoveredPosition ])[0];
    ctx.beginPath();
    ctx.translate(hoveredBin.x, hoveredBin.y);
    ctx.fillStyle= "rgba(255, 255, 255, 1)";
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-hoveredBin.x, -hoveredBin.y);
    ctx.closePath();
  }

  function onHover(event) {
    const rect = event.target.getBoundingClientRect();
    const x = (event.clientX - rect.left) / width;
    const y = (event.clientY - rect.top) / height;

    hoveredPosition = [ x, y ];
  }

  afterUpdate(async () => {
    window.setTimeout(() => {
      hexbinning
      .x(d => scaleX(d[0]))
      .y(d => scaleY(d[1]));

      const bins = getBins();
      const ctx = canvasElement.getContext("2d");
      const hexagonPath = new Path2D(hexagon);

      const minCount = (min(bins, d => (d as Array<any>).length) || 0);
      const maxCount = (max(bins, d => (d as Array<any>).length) || 0);
      color.domain([minCount, maxCount]);

      ctx.clearRect(0, 0, width, height);

      renderDataBins(ctx, bins, hexagonPath);
      renderHoveredBin(ctx, bins, hexagonPath);
    }, 0);
  });

</script>

<canvas
  id="{id}-bins-canvas"
  class="bins-canvas"
  width={ width }
  height={ height }
  bind:this={ canvasElement }
  on:mousemove={ onHover }
/>
