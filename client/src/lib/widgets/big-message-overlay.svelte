<script lang="typescript">
  export let message: string;

  let width: number;
  let height: number;
</script>

<div class="big-message-overlay" style="width:{width}px;height:{height}px">
  <div class="message-container">
    <div class="message">{ message }</div>
  </div>
</div>

<svelte:window bind:innerWidth={ width } bind:innerHeight={ height } />

<style>
  div.big-message-overlay {
    box-sizing: border-box;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: space-around;
    flex-direction: row;
    align-items: center;
    background: rgba(0, 0, 0, 0.3);
  }

  div.message-container {
    min-width: 300px;
    min-height: 120px;
    background: white;
    border: 2px solid black;
    transform: translateY(-50px);
    font-size: 25px;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 7px 45px 8px;
    border-radius: 4px;
    box-shadow: 0 2px 14px #888;
  }
</style>