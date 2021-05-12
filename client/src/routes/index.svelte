<script>
  import SplitView from '$lib/split-view.svelte';
  import { hoveredPosition } from '$lib/state/hovered-position';
  import { generator } from '$lib/util/bin-generator';

  let innerWidth = 0;
  let innerHeight = 0;

  const margin = 30;
  const tooltip = {
    width: 150,
    height: 80,
    x: 0,
    y: 0,
    data: {
      primary: [],
      secondary: []
    }
  };

  hoveredPosition.subscribe(value => {
    tooltip.data.primary = generator.getPrimaryBin(value[0], value[1]);
    tooltip.data.secondary = generator.getSecondaryBin(value[0], value[1]);
  });

  function onMouseMove(event) {
    tooltip.x = Math.min(event.clientX + margin, innerWidth - tooltip.width - margin);
    tooltip.y = Math.min(event.clientY, innerHeight - tooltip.height - margin);
  }

  $: left = tooltip.data.primary?.length || 0;
  $: right = tooltip.data.secondary?.length || 0;
  $: diff = Math.abs(left - right);
  $: percentage = Math.floor((diff / Math.max(left, right)) * 100000) / 1000;
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<main class="split-view" on:mousemove={ onMouseMove }>
  <SplitView></SplitView>
  { #if tooltip.data }
  <div class="tooltip" style="left:{tooltip.x}px;top:{tooltip.y}px;width:{tooltip.width}px;height:{tooltip.height}px;">
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
</main>

<style>
  main.split-view {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  main div.tooltip {
    position: absolute;
    background: white;
    padding: 5px 10px;
    border: 1px solid black;
    overflow: auto;
  }
  main div.tooltip div {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  main div.tooltip div.diff {
    font-weight: bold;
  }
</style>