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
		$leftView.initialized = false;
		$rightView.initialized = false;
		$primarySample = [];
		$secondarySample = [];
		reset();
		createPipelines();
	}
</script>

<header>
	<img class="logo" src="static/logo.svg" alt="ProSampling logo" height="30">
	<div class="pick-dataset config-component">
		<h2><i class="material-icons">folder_open</i>Dataset:</h2>
		<Alternatives
			name="datasets"
			alternatives={ ["mountain_peaks", "random", "fastfood_places"] }
			bind:activeAlternative={ $selectedDataset.name }
		/>
	</div>

	<div class="sampling-rate config-component">
		<h2><i class="material-icons">update</i>Sample interval:</h2>
		<!-- <NumberInput id="sampling-amount" bind:disabled={ isProgressionRunning } bind:value={ $samplingAmount } />
		<h2>points every</h2> -->
		<NumberInput id="sampling-rate" bind:disabled={ isProgressionRunning } bind:value={ $samplingRate } />
		<h2>ms</h2>
		<Toggle
			id="progression-running-indicator"
			bind:active={ isProgressionRunning }
			disabled={ !($leftView.initialized && $rightView.initialized) }
			disabledTitle="pipelines not ready"
			disabledText="wait ..."
			activeText="Pause."
			passiveText="Go!"
			style="width:75px;margin-left:20px;background:#64DD17"
			theme="dark"
		>
			<i slot="icon" class="material-icons">
				{ #if isProgressionRunning }pause{ :else }play_arrow{/if}
			</i>
		</Toggle>
		<button
			id="reset-progression"
			class={$leftView.initialized && $rightView.initialized ? "" : "disabled"}
			disabled={ !($leftView.initialized && $rightView.initialized) }
			on:click={ resetProgression }>

			<i class="material-icons">replay</i>
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

	header img.logo {
		margin-right: 50px;
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
		display: flex;
		align-items: center;
		margin-right: 10px;
	}
	header .config-component h2 i {
		font-size: 18px;
		margin: 0 7px;
	}

	header button#reset-progression {
		display: flex;
		flex-direction: row;
		align-items: center;
		box-sizing: border-box;
		line-height: 25px;
		font-size: 14px;
		font-weight: bold;
		margin: 0;
		padding: 0 10px;
		color: white;
		background: hsl(12, 100%, 43%);
		border: 2px solid black;
		cursor: pointer;
		margin-left: 15px;
	}
	header button#reset-progression i {
		margin-right: 2px;
		font-size: 16px;
	}
	header button#reset-progression:hover {
		background: hsl(12, 100%, 50%);
	}
	header button#reset-progression.disabled {
		opacity: 0.4;
	}
</style>