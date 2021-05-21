<script lang="typescript">
  export let id: string;
  export let value: number;
</script>

<input id="{id}-number-input" class="number-input" type="number" bind:value={ value } />

<style>
	.number-input {
		width: 50px;
		margin: 0 7px;
		padding: 0 5px;
		height: 18px;
		font-size: 14px;
		font-family: sans-serif;
		border: 1px solid transparent;
		border-radius: 3px;
    -moz-appearance: textfield;
		text-align: center;
		background: #555;
		color: white;
		font-weight: bold;
	}
	.number-input::-webkit-outer-spin-button,
	.number-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
	}
	.number-input:hover {
		background: #888;
	}
	.number-input:focus {
		background: white;
		color: black;
	}
</style>