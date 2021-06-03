<script lang="typescript">
  export let id = "my-toggle";
  export let active = true;
  export let disabled = false;
  export let title = "toggle feature";
  export let disabledTitle = "feature disabled";
  export let style = "";
  export let activeText;
  export let passiveText;
  export let disabledText = "";
  export let theme: "dark" | "light" = "light";

  $: checked = active && !disabled
</script>

<label
  id={id}
  class="toggle {active ? "active" : ""} {disabled ? "disabled" : ""} { theme }"
  for="{id}-toggle"
  title={ disabled ? title : disabledTitle }>

  <div class="toggle-text" style={ style } on:click={ null }>
    { #if $$slots.icon }
      <slot class="icon" name="icon"></slot>
    { /if }
    <span>{ disabled ? disabledText : active ? activeText : passiveText }</span>
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
    background: transparent;
    border-radius: 2px;
    font-weight: bold;
    text-align: center;
    padding: 0;
    margin: 0;
    line-height: 25px;
    cursor: pointer;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    filter: brightness(95%);
    transition: background-color 0.1s ease-in-out;
  }
  label.toggle .toggle-text:hover {
    filter: brightness(100%)
  }
  label.toggle.light .toggle-text {
    font-size: 16px;
    font-family: sans-serif;
    margin: 0;
    background: white;
    color: black;
    border-color: black;
  }
  label.toggle.dark .toggle-text {
    background: #333;
    color: white;
  }
  label.toggle.disabled .toggle-text {
    opacity: 0.4;
  }
  label.toggle.light .toggle-text:hover {
    background: #eee;
  }
  label.toggle.dark .toggle-text:hover {
    background: #555;
  }
  label.toggle.light.disabled .toggle-text:hover {
    background: white;
  }
  :global(label.toggle .toggle-text > i) {
		margin: 0 2px;
		font-size: 18px;
  }
  label.toggle .toggle-text > span {
    margin: 0 2px;
  }
  label.toggle input {
    display: none;
  }
</style>