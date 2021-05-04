<!-- src/routes/$layout.svelte -->
<header>
	<nav>
		<a href=".">Home</a>
		<a href="about">About</a>
		<a href="settings">Settings</a>
	</nav>
</header>

<slot></slot>

<footer>
	<a href="https://vis-au.github.io/">Visualization Repository</a>
</footer>


<style>
	header, footer {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		background: black;
		color: white;
		font-family: sans-serif;
	}
	header a, footer a {
		color: white;
	}

	header {
		height: 30px;
	}

	footer {
		height: 25px;
	}
</style>
