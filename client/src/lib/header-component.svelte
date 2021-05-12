<script lang="typescript">
	import { progressionState } from './progression-state';
	import { samplingAmount } from './sampling-amount';
	import { samplingRate } from './sampling-rate';
	import { samplingTotal } from './sampling-total';
	import Toggle from './toggle.svelte';

	let isProgressionRunning = false;
	let samplingRateValue = 1000;
	let samplingAmountValue = 1000;
	let samplingTotalValue = 0;

	samplingTotal.subscribe(value => samplingTotalValue = value);

	$: progressionState.set(isProgressionRunning ? "running" : "paused");
	$: samplingRate.set(samplingRateValue);
	$: samplingAmount.set(samplingAmountValue);
</script>

<header>
	<h1 class="title">Sampling Pipeline</h1>
	<div class="pick-dataset config-component">
		<h2>Pick Dataset</h2>
		<div class="datasets">
			<button class="dataset selected">Random</button>
			<button class="dataset">Burger places</button>
			<button class="dataset">Dataset ABC</button>
			<button class="dataset">Mountain peaks</button>
		</div>
	</div>

	<div class="sampling-rate config-component">
		<h2>Sample</h2>
		<input type="number" bind:value={ samplingAmountValue } />
		<h2>points every</h2>
		<input type="number" bind:value={ samplingRateValue } />
		<!-- src: https://stackoverflow.com/a/2901298 -->
		<h2>milliseconds ({samplingTotalValue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} so far).</h2>
		<Toggle
			id="progression-running-indicator"
			bind:active={ isProgressionRunning }
			activeText="Pause."
			passiveText="Go!"
			style="width:75px;margin-left:20px"
		/>
	</div>
</header>

<style>
	header {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items: center;
		background: black;
		color: white;
		font-family: sans-serif;
		box-sizing: border-box;
		padding: 5px;
	}
	header {
		height: 30px;
	}
	header h1.title {
		min-width: 200px;
		font-size: 20px;
		margin-right: 75px;
	}

	header .config-component {
		display: flex;
		flex-direction: row;
		width: 100%;
		align-items: center;
		font-size: 14px
	}
	header .config-component h2 {
		font-size: 16px;
	}

	header .pick-dataset h2 {
		min-width: 120px;
	}
	header .pick-dataset .datasets {
		display: flex;
		flex-direction: row;
		width: 100%;
		align-items: center;
	}

	header .pick-dataset .datasets .dataset {
		font-family: sans-serif;
		background: black;
		color: white;
		font-weight: bold;
		text-decoration: underline;
		padding: 2px 15px 1.5px;
		border: 2px solid transparent;
		border-radius: 20px;
		cursor: pointer;
	}
	header .pick-dataset .datasets .dataset:hover {
		border-color: white;
		text-decoration: none;
	}
	header .pick-dataset .datasets .dataset.selected {
		background: white;
		color: black;
		border-color: black;
		text-decoration: none;
	}

	header .sampling-rate input[type="number"] {
		width: 50px;
		margin: 0 10px;
	}
</style>