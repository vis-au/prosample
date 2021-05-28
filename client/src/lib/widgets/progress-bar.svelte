<script lang="typescript">
  export let id: string;
  export let progress: number;
  export let width: number;
  export let height: number;
</script>

<div id="{id}-progress-bar" class="progress-bar" style="width:{width}px" title="{progress*100}%;min-height:{height}px">
  <div class="progress" style="width:{progress*width}px;height:{height}px"></div>
</div>

<style>
  .progress-bar {
    border: 1px solid black;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    margin-top: 1px;
  }
  .progress-bar .progress {
    background: black;
  }
</style>