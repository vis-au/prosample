<script lang="typescript">
  export let name: string;
  export let alternatives: string[];
  export let activeAlternative: string;
</script>

<div id="{ name }-alternatives" class="alternatives">
  { #each alternatives as alternative }
    <label for="{alternative.split(" ").join("_")}-{name}-alternative" class="alternative {alternative === activeAlternative ? "active" : ""}">
      <div class="alternative-text {alternative === activeAlternative ? "active" : ""}">{ alternative }</div>
      <input
        id="{alternative.split(" ").join("_")}-{name}-alternative"
        type="radio"
        name={name}
        value={alternative}
        bind:group={activeAlternative} />
    </label>
  { /each }
</div>

<style>
  div.alternatives {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
  }

	div.alternatives div.alternative-text {
		font-family: sans-serif;
		background: #333;
		color: white;
		font-weight: bold;
		padding: 2px 15px 1.5px;
		border: 2px solid black;
		border-radius: 20px;
		cursor: pointer;
	}
	div.alternatives div.alternative-text:hover {
    background: #555;
	}
	div.alternatives div.alternative-text.active {
		background: white;
		color: black;
		border-color: black;
		text-decoration: none;
	}
  div.alternatives input[type="radio"] {
    display: none;
  }
</style>