<script lang="typescript">
  import { hoveredPosition } from "$lib/state/hovered-position";
  import { generator } from "$lib/util/bin-generator";

  export let active: boolean = false;
  export let x: number;
  export let y: number;
  export let width: number;
  export let height: number;
  export let data: {
    primary: [number, number][],
    secondary: [number, number][]
  };

  $: left = data.primary?.length || 0;
  $: right = data.secondary?.length || 0;
  $: diff = Math.abs(left - right);
  $: percentage = Math.floor((diff / Math.max(left, right)) * 100000) / 1000;

  hoveredPosition.subscribe(value => {
    if (value[1] < 0) {
      active = false;
      return;
    }

    active = true;
    data.primary = generator.getPrimaryBin(value[0], value[1]);
    data.secondary = generator.getSecondaryBin(value[0], value[1]);
  });
</script>

{ #if active }
<div class="tooltip" style="left:{x}px;top:{y}px;width:{width}px;height:{height}px;">
  <div class="left">
    <span>left:</span>
    <span>{ left }</span>
  </div>
  <div class="right">
    <span>right:</span>
    <span>{ right }</span>
  </div>
  <hr/>
  <div class="diff">
    <span>diff:</span>
    <span>{ percentage }%</span>
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
  div.tooltip div {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  div.tooltip div.diff {
    font-weight: bold;
  }
</style>