<script lang="typescript">
  export let title = "Info";
  export let message: string;

  let width = 0;
  let height = 0;
</script>

<div class="big-message-overlay" style="width:{width}px;height:{height}px">
  <div class="message-container">
    <h1><i class="material-icons">info</i>{ title }</h1>
    <p class="message">{ message }</p>
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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 4px;
    box-shadow: 0 2px 14px #888;
  }

  div.message-container h1 {
    font-size: 22px;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 0;
    background: black;
    padding: 7px 20px 8px;
    color: white;
  }
  div.message-container h1 i {
    margin-right: 10px;
    font-size: 20px;
  }
  div.message-container p {
    font-size: 16px;
    padding: 15px 20px;
  }
</style>