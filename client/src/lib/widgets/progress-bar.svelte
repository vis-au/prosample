<script lang="typescript">
  export let id: string;
  export let progress: number;
  export let width: number = null;
  export let height: number;
</script>

<div id="{id}-progress-bar" class="progress-bar" style="width:{width}px;min-height:{height}px" title="{Math.floor(progress*10000)/100}%">
  <div class="progress" style="width:{progress*100}%;height:{height}px"></div>
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