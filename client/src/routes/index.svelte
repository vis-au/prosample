<script>
  import SplitView from '$lib/split-view.svelte';
</script>


<main class="split-view">
  <SplitView></SplitView>
</main>

<style>
  main.split-view {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
</style>