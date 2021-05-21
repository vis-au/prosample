<script lang="typescript">
	import Alternatives from './widgets/alternatives.svelte';
	import { progressionState } from './state/progression-state';
	import { samplingAmount } from './state/sampling-amount';
	import { samplingRate } from './state/sampling-rate';
	import Toggle from './widgets/toggle.svelte';
	import { leftPipeline, rightPipeline } from './state/pipelines';

	let isProgressionRunning = false;

	$: progressionState.set(isProgressionRunning ? "running" : "paused");
</script>

<header>
	<h1 class="title">Sampling Pipeline</h1>
	<div class="pick-dataset config-component">
		<h2>Pick Dataset</h2>
		<Alternatives
			name="datasets"
			alternatives={ ["Random", "Burger places", "Dataset ABC", "Mountain peaks"] }
			activeAlternative={ "Random" }
		/>
	</div>

	<div class="sampling-rate config-component">
		<h2>Sample</h2>
		<input type="number" bind:value={ $samplingAmount } />
		<h2>points every</h2>
		<input type="number" bind:value={ $samplingRate } />
		<!-- src: https://stackoverflow.com/a/2901298 -->
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

	header .sampling-rate input[type="number"] {
		width: 50px;
		margin: 0 10px;
	}
</style>