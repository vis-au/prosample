<script lang="typescript">
  import type { LinearizationType, SelectionType, SubdivisionType, ViewType } from "./types";

  export let id = "0";
  export let orientation: "left" | "right" | "center" = "left";
  export let selectedViewType: ViewType = "scatterplot";
  export let selectedSubdivisionType: SubdivisionType = "equal size";
  export let selectedSelectionType: SelectionType = "first";
  export let selectedLinearizationType: LinearizationType = "knn";

  const linearizationTypes: LinearizationType[] = ["knn", "sort by attribute", "z-order"];
  const subdivisionTypes: SubdivisionType[] = ["equal size", "equal cardinality", "equal density", "equal attribute"];
  const selectionTypes: SelectionType[] = ["first", "median", "min/max", "random"];
  const viewTypes: ViewType[] = ["scatterplot", "bins (absolute)", "bins (delta)"];
</script>

<div class="pipeline-config-view {orientation}">
  <h1>Pipeline Configuration {id}</h1>
  <div class="configuration">
    <div class="pipeline">
      <label for="{id}-linearization">
        <span title="linearization">Lin.</span>
        <select id="{id}-linearization" name="{id}-linearization" bind:value={ selectedLinearizationType }>
          { #each linearizationTypes as type }
          <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-subdivision">
        <span title="subdivision">Sub.</span>
        <select id="{id}-subdivision" name="{id}-subdivision" bind:value={ selectedSubdivisionType }>
          { #each subdivisionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-selection">
        <span title="selection">Sel.</span>
        <select id="{id}-selection" name="{id}-selection" bind:value={ selectedSelectionType }>
          { #each selectionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
    </div>
    <div class="view">
      <label for="{id}-view">
        <span>View</span>
        <select id="{id}-view" name="{id}-view" bind:value={ selectedViewType }>
          { #each viewTypes as type }
            <option>{ type }</option>
          { /each }
        </select>
      </label>
    </div>
  </div>
</div>

<style>
  div.pipeline-config-view {
    padding: 0 5px 10px;
    box-sizing: border-box;
    border: 1px solid black;
    width: 100%;
  }
  div.pipeline-config-view.left {
    border-right: none;
  }
  div.pipeline-config-view.right {
    border-left: none;
  }
  div.pipeline-config-view .configuration {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  div.pipeline-config-view h1 {
    font-size: 15px;
  }
</style>