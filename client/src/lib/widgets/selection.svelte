<script lang="typescript">
  export let id: string;
  export let title: string;
  export let label: string;
  export let value: string;
  export let options: string[];
  export let isEmphasized = false;
  export let isDisabled = false;
</script>

<label for="{id}-selection" class="selection {isEmphasized ? "emph" : ""} {isDisabled ? "disabled" : ""}">
  <span title={title}>{label}</span>
  <select id="{id}-selection" name="{id}-selection" bind:value={ value } disabled={ isDisabled }>
    { #each options as option }
      <option value={ option }>{ option }</option>
    { /each }
  </select>
  <svg>
    <use xlink:href="#select-arrow-down"></use>
  </svg>
</label>

<style>
  label.selection {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    margin: 0 2px 0 0px;
    transition: all 0.25s ease-in-out;
  }
  label.selection.disabled select {
    color: #aaa;
    opacity: 0.4;
  }
  label.selection span {
    margin-right: 5px;
  }

  label.selection select {
    -webkit-appearance: none;
    padding: 2px 25px 2px 8px;
    margin-right: 3px;
    border: 1px solid #ccc;
    border-radius: 2px;
    background: white;
    color: black;
    cursor: pointer;
    font-size: 12px;
    font-family: sans-serif;
    transition: all 150ms ease;
  }
  label.selection select:focus {
    outline: none;
  }
  label.selection.emph select {
    border-color: black;
    font-weight: bold;
  }

  :global(label.selection svg) {
    position: absolute;
    right: 10px;
    top: calc(50% - 3px);
    width: 10px;
    height: 6px;
    stroke-width: 2px;
    stroke: #aaa;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    pointer-events: none;
  }
  :global(label.selection.emph svg) {
    stroke: #333;
  }
</style>