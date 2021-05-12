<script>
  export let id = "my-toggle";
  export let active = true;
  export let title = "toggle feature";
  export let style = "";
  export let activeText = "active";
  export let passiveText = "passive";
</script>

<label id={id} class="toggle {active ? "active" : ""}" for="{id}-toggle" title={ title }>
  <div class="toggle-text" style={ style }>{active ? activeText : passiveText}</div>
  <input id="{id}-toggle" type="checkbox" bind:checked={ active } />
</label>

<style>
  label.toggle {
    display: flex;
    flex-direction: row;
  }
  label.toggle .toggle-text {
    border: 2px solid black;
    border-radius: 2px;
    background: white;
    color: black;
    font-weight: bold;
    text-align: center;
    padding: 0;
    margin: 0;
    line-height: 25px;
    cursor: pointer;
    transition: background-color 0.1s ease-in-out;
  }
  label.toggle .toggle-text:hover {
    background: #eee;
  }
  label.toggle input {
    display: none;
  }
</style>