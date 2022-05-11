<script lang="typescript">
  import { dimensionsInData, selectedDataset } from './state/data';
	import { isProgressionRunning } from './state/progression-state';
  import { interactionMode } from '$lib/state/interaction-mode';
	import { createPipelines } from './state/pipelines';
	import { primarySample, secondarySample } from './state/sampled-data';
	import { globalViewConfig, leftView, rightView } from './state/view-config';
	import { reset } from './util/requests';
	import Alternatives from './widgets/alternatives.svelte';
	import NumberInput from './widgets/number-input.svelte';
	import { samplingRate } from './state/sampling-rate';
	import Toggle from './widgets/toggle.svelte';
  import Selection from './widgets/selection.svelte';

  let steeringConfig = {
    dimension: "",
    min: 0,
    max: 0
  };

	function resetProgression() {
		$isProgressionRunning = false;
		$leftView.initialized = false;
		$rightView.initialized = false;
		$primarySample = [];
		$secondarySample = [];
		reset();
		createPipelines();
	}
</script>

<header>
	<div class="left side">
		<img class="logo" src="static/logo.svg" alt="ProSampling logo" height="30">
		<div class="pick-dataset config-component">
			<h2><i class="material-icons">folder_open</i>Dataset:</h2>
			<Alternatives
				name="datasets"
				alternatives={ ["mountain_peaks", "spotify"] }
				bind:activeAlternative={ $selectedDataset.name }
			/>
		</div>

		<div class="sampling-rate config-component">
			<h2><i class="material-icons">update</i>Sample interval:</h2>
			<!-- <NumberInput id="sampling-amount" bind:disabled={ isProgressionRunning } bind:value={ $samplingAmount } />
			<h2>points every</h2> -->
			<NumberInput id="sampling-rate" bind:disabled={ $isProgressionRunning } bind:value={ $samplingRate } />
			<h2>ms</h2>
		</div>

    <div class="bin-size config-component">
      <h2>Bin size:</h2>
      <NumberInput id="bins-ize" bind:value={ $globalViewConfig.binSize } />
    </div>

    <div class="steering config-component">
      <h2>x:</h2>
      <Selection
        id="steering-dimension"
        title="set steering dimension"
        label=""
        options={ $dimensionsInData }
        bind:value={ steeringConfig.dimension }
      />
      <h2>y:</h2>
      <Selection
        id="steering-dimension"
        title="set steering dimension"
        label=""
        options={ $dimensionsInData }
        bind:value={ steeringConfig.dimension }
      />
      <h2>View interaction:</h2>
      <Alternatives
				name="view-interaction-mode"
				alternatives={ ["zoom", "brush"] }
				bind:activeAlternative={ $interactionMode }
			/>
    </div>
	</div>
	<div class="right side">
		<Toggle
			id="progression-running-indicator"
			bind:active={ $isProgressionRunning }
			disabled={ !($leftView.initialized && $rightView.initialized) }
			title="start sampling the dataset"
			disabledTitle="pipelines not ready"
			disabledText="wait ..."
			activeText="Pause"
			passiveText="Sample"
			style="width:85px;margin-left:20px;color:lime;border:1px solid lime"
			theme="dark"
		>
			<i slot="icon" class="material-icons">
				{ #if $isProgressionRunning }pause{ :else }play_arrow{/if}
			</i>
		</Toggle>
		<button
			id="reset-progression"
			class={$leftView.initialized && $rightView.initialized ? "" : "disabled"}
			disabled={ !($leftView.initialized && $rightView.initialized) }
			title="reset the pipelines to 0 samples drawn."
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
		justify-content: space-between;
		align-items: center;
		background: #222;
		color: white;
		font-family: sans-serif;
		box-sizing: border-box;
		padding: 5px;
	}
	header {
		height: 30px;
	}

	header div.side {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items:center;
	}

	header img.logo {
		margin-right: 50px;
	}

	header .config-component {
		display: flex;
		flex-direction: row;
		width: 100%;
		align-items: center;
		font-size: 14px;
		margin-right: 50px;
	}
	header .config-component h2 {
		font-size: 16px;
		display: flex;
		align-items: center;
		margin-right: 10px;
		white-space: nowrap;
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
		background: #333;
		color: yellow;
		border: 1px solid yellow;
		cursor: pointer;
		margin-left: 15px;
	}
	header button#reset-progression i {
		margin-right: 2px;
		font-size: 16px;
	}
	header button#reset-progression:hover {
		background: #555;
	}
	header button#reset-progression.disabled {
		opacity: 0.4;
	}
</style>