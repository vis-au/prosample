<script lang="typescript">
	import Alternatives from './widgets/alternatives.svelte';
	import { progressionState } from './state/progression-state';
	import { samplingAmount } from './state/sampling-amount';
	import { samplingRate } from './state/sampling-rate';
	import { leftPipeline, rightPipeline } from './state/pipelines';
	import Toggle from './widgets/toggle.svelte';
	import NumberInput from './widgets/number-input.svelte';
	import { selectedDataset } from './state/selected-dataset';

	let isProgressionRunning = false;

	$: progressionState.set(isProgressionRunning ? "running" : "paused");
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
		<h2>Sample</h2>
		<NumberInput id="sampling-amount" bind:disabled={ isProgressionRunning } bind:value={ $samplingAmount } />
		<h2>points every</h2>
		<NumberInput id="sampling-rate" bind:disabled={ isProgressionRunning } bind:value={ $samplingRate } />
		<h2>milliseconds</h2>
		<Toggle
			id="progression-running-indicator"
			bind:active={ isProgressionRunning }
			disabled={ !($leftPipeline.ready && $rightPipeline.ready) }
			disabledTitle="pipelines not ready"
			disabledText="wait ..."
			activeText="Pause."
			passiveText="Go!"
			style="width:75px;margin-left:20px"
			theme="dark"
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
</style>