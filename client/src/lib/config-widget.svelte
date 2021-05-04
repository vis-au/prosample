<script lang="typescript">
  export let id = "0";

  const linearizationTypes = ["knn", "sort by attribute", "z-order"];
  const subdivisionTypes = ["equal size", "equal cardinality", "equal density", "equal attribute"];
  const selectionTypes = ["first", "median", "min/max", "random"];
  const viewTypes = ["scatterplot", "hexagonal bins", "square bins"];
</script>

<div class="pipeline-config-view">
  <h1>Pipeline Configuration {id}</h1>
  <div class="configuration">
    <div class="pipeline">
      <label for="{id}-linearization">
        <span>Linearization</span>
        <select id="{id}-linearization" name="{id}-linearization">
          { #each linearizationTypes as type }
          <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-linearization">
        <span>Subdivision</span>
        <select id="{id}-linearization" name="{id}-linearization">
          { #each subdivisionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
      <label for="{id}-linearization">
        <span>Selection</span>
        <select id="{id}-linearization" name="{id}-linearization">
          { #each selectionTypes as type }
            <option>{ type } </option>
          { /each }
        </select>
      </label>
    </div>
    <div class="view">
      <label for="{id}-view">
        <span>View</span>
        <select id="{id}-view">
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