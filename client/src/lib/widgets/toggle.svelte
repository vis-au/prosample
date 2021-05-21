<script>
  export let id = "my-toggle";
  export let active = true;
  export let disabled = false;
  export let title = "toggle feature";
  export let disabledTitle = "feature disabled";
  export let style = "";
  export let activeText;
  export let passiveText;
  export let disabledText = "";

  $: checked = active && !disabled
</script>

<label
  id={id}
  class="toggle {active ? "active" : ""} {disabled ? "disabled" : ""}"
  for="{id}-toggle"
  title={ disabled ? title : disabledTitle }>

  <div class="toggle-text" style={ style }>
    {disabled ? disabledText : active ? activeText : passiveText}
  </div>

  <input
    id="{id}-toggle"
    type="checkbox"
    checked={ checked }
    disabled={ disabled }
    on:click={ () => active = !active}
  />
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
  label.toggle.disabled .toggle-text {
    color: grey;
  }
  label.toggle .toggle-text:hover {
    background: #eee;
  }
  label.toggle.disabled .toggle-text:hover {
    background: white;
  }
  label.toggle input {
    display: none;
  }
</style>