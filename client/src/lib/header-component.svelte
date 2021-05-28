<script lang="typescript">
	import Alternatives from './widgets/alternatives.svelte';
	import { progressionState } from './state/progression-state';
	import { samplingRate } from './state/sampling-rate';
	import Toggle from './widgets/toggle.svelte';
	import NumberInput from './widgets/number-input.svelte';
	import { selectedDataset } from './state/selected-dataset';
	import { leftView, rightView } from './state/view-config';
	import { primarySample, secondarySample } from './state/sampled-data';
	import { reset } from './util/requests';
	import { createPipelines } from './state/pipelines';

	let isProgressionRunning = false;

	$: progressionState.set(isProgressionRunning ? "running" : "paused");

	function resetProgression() {
		isProgressionRunning = false;
		$primarySample = [];
		$secondarySample = [];
		reset();
		createPipelines();
	}
</script>

<header>
	<h1 class="title">Sampling Pipeline</h1>
	<div class="pick-dataset config-component">
		<h2>Pick Dataset</h2>
		<Alternatives
			name="datasets"
			alternatives={ ["mountain_peaks", "random", "fastfood_places"] }
			bind:activeAlternative={ $selectedDataset }
		/>
	</div>

	<div class="sampling-rate config-component">
		<h2>Sample every</h2>
		<!-- <NumberInput id="sampling-amount" bind:disabled={ isProgressionRunning } bind:value={ $samplingAmount } />
		<h2>points every</h2> -->
		<NumberInput id="sampling-rate" bind:disabled={ isProgressionRunning } bind:value={ $samplingRate } />
		<h2>milliseconds</h2>
		<Toggle
			id="progression-running-indicator"
			bind:active={ isProgressionRunning }
			disabled={ !($leftView.initialized && $rightView.initialized) }
			disabledTitle="pipelines not ready"
			disabledText="wait ..."
			activeText="Pause."
			passiveText="Go!"
			style="width:75px;margin-left:20px"
			theme="dark"
		/>
		<button
			id="reset-progression"
			class={$leftView.initialized && $rightView.initialized ? "" : "disabled"}
			disabled={ !($leftView.initialized && $rightView.initialized) }
			on:click={ resetProgression }>

			Reset
		</button>
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

	header button#reset-progression {
		width: 75px;
		line-height: 25px;
		font-size: 14px;
		font-weight: bold;
		margin: 0;
		padding: 0;
		color: white;
		background: rgb(180, 34, 34);
		border: 2px solid black;
		cursor: pointer;
		margin-left: 15px;
	}
	header button#reset-progression:hover {
		background: rgb(222, 84, 84);
	}
	header button#reset-progression.disabled {
		opacity: 0.4;
	}
</style>