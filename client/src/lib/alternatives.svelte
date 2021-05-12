<script lang="typescript">
  export let name: string;
  export let alternatives: string[] = ["option a", "option b", "option c"];
  export let activeAlternative: string = "option a";
</script>

<div id={ name } class="alternatives">
  { #each alternatives as alternative }
    <label for={alternative.split(" ").join("_")} class="alternative">
      <div class="alternative-text {alternative === activeAlternative ? "active" : ""}">{ alternative }</div>
      <input
        id={alternative.split(" ").join("_")}
        type="radio"
        name={name}
        value={alternative}
        checked={ alternative === activeAlternative }
        on:click={ () => { activeAlternative=alternative }} />
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
		background: black;
		color: white;
		font-weight: bold;
		text-decoration: underline;
		padding: 2px 15px 1.5px;
		border: 2px solid black;
		border-radius: 20px;
		cursor: pointer;
	}
	div.alternatives div.alternative-text:hover {
		border-color: white;
		text-decoration: none;
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