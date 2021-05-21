<script>
  import { onMount } from 'svelte';
  import SplitView from '$lib/split-view.svelte';
  import { reset, sample, updatePipeline } from '$lib/util/requests';
  import Tooltip from '$lib/widgets/tooltip.svelte';
  import { leftPipeline, rightPipeline } from '$lib/state/pipelines';
  import { samplingRate } from '$lib/state/sampling-rate';
  import { progressionState } from '$lib/state/progression-state';
  import { generator } from '$lib/util/bin-generator';

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

  // [random x, random y, random attribute]
  let rawA = [];
  let rawB = [];

  $: sampleA = rawA.slice(0);
  $: sampleB = rawB.slice(0);

  $: generator.primaryData = sampleA || [];
  $: generator.secondaryData = sampleB || [];

  onMount(async () => {
    await reset();

    updatePipeline($leftPipeline).then(() => {
      leftPipeline.update(config => {
        config.ready = true;
        return config;
      });
    });
    updatePipeline($rightPipeline).then(() => {
      rightPipeline.update(config => {
        config.ready = true;
        return config;
      });
    });

    samplingRate.subscribe(() => {
      window.clearInterval(samplingInterval);
      samplingInterval = startSampling();
    });

    progressionState.subscribe(value => {
      if (value === "running") {
        samplingInterval = startSampling();
      } else {
        window.clearInterval(samplingInterval);
      }
    });
  });

  function startSampling() {
    return window.setInterval(async () => {
      const responseA = await sample("left");
      const jsonA = await responseA.json();

      const responseB = await sample("right");
      const jsonB = await responseB.json();

      rawA = rawA.concat(jsonA.sample);
      rawB = rawB.concat(jsonB.sample);

      $leftPipeline.pointsRetrieved = rawA.length;
      $rightPipeline.pointsRetrieved = rawB.length;
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
    justify-content: space-between;
  }
</style>