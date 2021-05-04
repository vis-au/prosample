<script>
import HeaderComponent from "$lib/header-component.svelte";
</script>

<!-- src/routes/$layout.svelte -->
<HeaderComponent></HeaderComponent>

<slot></slot>

<footer>
	<a href="https://vis-au.github.io/">Visualization Repository</a>
</footer>


<style>
	footer {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items: center;
		background: black;
		color: white;
		font-family: sans-serif;
	}
	footer a {
		color: white;
	}

	footer {
		height: 25px;
	}
</style>
