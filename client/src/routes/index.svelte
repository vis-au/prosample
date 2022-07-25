<script lang="typescript">
  import { onMount } from 'svelte';
  import SplitView from '$lib/split-view.svelte';
  import Tooltip from '$lib/widgets/tooltip.svelte';
  import BigMessageOverlay from '$lib/widgets/big-message-overlay.svelte'
  import { getDatasetSize, reset, sample } from '$lib/util/requests';
  import { samplingRate } from '$lib/state/sampling-rate';
  import { primarySample, secondarySample } from '$lib/state/sampled-data';
  import { leftView, rightView } from '$lib/state/view-config';
  import { scaleChunk, selectedDataset } from '$lib/state/data';
  import { createPipelines, leftPipelineConfig } from '$lib/state/pipelines';
  import { isProgressionRunning } from '$lib/state/progression-state';

  let innerWidth = 0;
  let innerHeight = 0;

  const margin = 30;
  const tooltip = {
    width: 150,
    height: 60,
    x: 0,
    y: 0,
    data: {
      primary: [],
      secondary: []
    }
  };

  let samplingInterval = -1;
  let datasetName = null;

  onMount(async () => {
    await reset();

    samplingRate.subscribe(() => {
      window.clearInterval(samplingInterval);
      samplingInterval = startSampling();
    });

    isProgressionRunning.subscribe(value => {
      if (value) {
        samplingInterval = startSampling();
      } else {
        window.clearInterval(samplingInterval);
      }
    });

    selectedDataset.subscribe(async value => {
      if (value.name === datasetName) {
        return;
      }

      $isProgressionRunning = false;
      $leftView.initialized = false;
      $rightView.initialized = false;
      datasetName = value.name;

      await createPipelines();
      await getDatasetSize($leftPipelineConfig.id);

      primarySample.set([]);
      secondarySample.set([]);
    });

    selectedDataset.update(value => {
      value.name = "taxis";
      return value;
    });
  });

  function startSampling() {
    return window.setInterval(async () => {
      const responseA = await sample("left");
      const jsonA = await responseA.json();

      const responseB = await sample("right");
      const jsonB = await responseB.json();

      $primarySample = $primarySample.concat(scaleChunk(jsonA.sample));
      $secondarySample = $secondarySample.concat(scaleChunk(jsonB.sample));
    }, $samplingRate);
  }

  function onMouseMove(event) {
    tooltip.x = Math.min(event.clientX + margin, innerWidth - tooltip.width - margin);
    tooltip.y = event.clientY + margin > innerHeight - tooltip.height - margin
    ? event.clientY - margin - tooltip.height
    : event.clientY + margin;
  }
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<main class="split-view" on:mousemove={ onMouseMove }>
  <SplitView></SplitView>
  { #if !($leftView.initialized && $rightView.initialized) }
    <BigMessageOverlay
      message="Please wait, while we initialize the two pipelines ..."
    />
  { /if }
  <Tooltip
    x={ tooltip.x }
    y={ tooltip.y }
    width={ tooltip.width }
    height={ tooltip.height }
    data={ tooltip.data }
  />
</main>

<style>
  main.split-view {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
  }
</style>