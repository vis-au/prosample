<script lang="typescript">
  import { scaleDiverging } from "d3-scale";
  import { hoveredPosition } from "$lib/state/hovered-position";
  import type { BinType } from '$lib/util/bin-generator';
  import { generator } from "$lib/util/bin-generator";
  import { divergingScheme } from "$lib/state/color-schemes";
  import { globalViewConfig } from "$lib/state/view-config";

  export let active = false;
  export let x: number;
  export let y: number;
  export let width: number;
  export let height: number;
  export let data: {
    primary: BinType[],
    secondary: BinType[]
  };

  $: color = scaleDiverging($divergingScheme).domain([-1, 0, 1]);

  $: left = data.primary?.length || 0;
  $: right = data.secondary?.length || 0;
  $: diff = left - right || 0;
  $: percentage = left === 0 && right === 0 ? 0 : diff / -Math.max(left, right);

  // src: https://stackoverflow.com/a/2901298
  $: labelText = $globalViewConfig.useRelativeDifferenceScale
    ? `${ Math.abs(Math.round(percentage*100)) }%`
    : `${ Math.abs(diff).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }`;

  let diffLabel: SVGTextElement;
  $: diffLabelWidth = diffLabel?.getBoundingClientRect().width;
  let labelMargin = 50;
  let plotHeight = 25;
  $: plotWidth = width - labelMargin;

  hoveredPosition.subscribe(value => {
    if (value[1] < 0) {
      active = false;
      return;
    }

    active = true;
    data.primary = generator.getPrimaryBinForScreenPosition(value[0], value[1]);
    data.secondary = generator.getSecondaryBinForScreenPosition(value[0], value[1]);
  });
</script>

{ #if active }
<div class="tooltip" style="left:{x}px;top:{y}px;width:{width}px;height:{height}px;">
  <h1>Sampling Difference</h1>
  <div class="top">
    <span class="left {left>right?"greater":""}">{ left }</span>
    <svg class="difference-bar-canvas" width={ plotWidth } height={ plotHeight }>
      <line x1={ plotWidth/2 } x2={plotWidth/2} y1={ 0 } y2={ plotHeight } stroke="black" stroke-dasharray="2px" />
      <rect
      class="difference-bar"
      width={ Math.abs(percentage * (plotWidth / 2)) }
      height={ plotHeight }
      x={ percentage > 0 ? plotWidth / 2 : ((1+percentage) * plotWidth/2) }
      fill={ color(percentage) }
      />
      <rect
        class="background"
        x={ plotWidth / 2 - diffLabelWidth * 0.625 }
        width={ diffLabelWidth * 1.25 }
        height={ plotHeight * 0.6}
        y={ plotHeight * 0.2 }
        fill="rgba(255,255,255,0.7)"
      />
      <text class="diff" x={ plotWidth / 2 } y={ plotHeight / 2+5 } style="text-anchor:middle" bind:this={ diffLabel }>{ labelText }</text>
    </svg>
    <span class="right {right>left?"greater":""}">{ right }</span>
  </div>
</div>
{ /if }

<style>
  div.tooltip {
    position: absolute;
    background: white;
    padding: 5px 10px;
    border: 1px solid black;
    overflow: auto;
  }
  div.tooltip h1 {
    font-size: 11pt;
    margin: 5px 0;
  }
  div.tooltip div.top {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
  }
  div.tooltip div.top .greater {
    font-weight: bold;
  }
  div.tooltip div.top .right {
    text-anchor: end;
  }
  div.tooltip svg.difference-bar-canvas {
    border: 1px solid black;
  }
  div.tooltip svg.difference-bar-canvas rect.difference-bar {
    fill-opacity: 0.73;
  }
</style>