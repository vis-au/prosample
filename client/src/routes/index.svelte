<script>
  import SplitView from '$lib/split-view.svelte';
  import Tooltip from '$lib/widgets/tooltip.svelte';

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

  function onMouseMove(event) {
    tooltip.x = Math.min(event.clientX + margin, innerWidth - tooltip.width - margin);
    tooltip.y = event.clientY + margin > innerHeight - tooltip.height - margin
    ? event.clientY - margin - tooltip.height
    : event.clientY + margin;
  }
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<main class="split-view" on:mousemove={ onMouseMove }>
  <SplitView></SplitView>
  <Tooltip
    x={ tooltip.x }
    y={ tooltip.y }
    width={ tooltip.width }
    height={ tooltip.height }
    data={ tooltip.data }
  />
</main>

<style>
  main.split-view {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
</style>