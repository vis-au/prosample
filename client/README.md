# PVA Sampling Comparison Tool - Client
This directory contains the code for the browser-based user interface to the pva sampling pipeline.
It serves as a visual demonstration tool to visualize the impace of adjusting different steps of the progressive sampling pipeline.
The client allows to configure two sampling pipelines and visualize their output next to each other.
Both sampling pipelines retrieve the next sample of data at the same time, yet under the particular configuration.

The client is web-based, using the visualization libraries [D3](https://d3js.org/) and [deck.gl](https://deck.gl/) under the hood, ontop of a lightweight [svelte](https://svelte.dev/) architecture.


## Installation
To install the client, you need a local installation of [nodeJS](https://nodejs.org/) (version 14.16.1 or higher) with the package manager npm (version 7.11.2 or higher).
Run the following command inside this directory to load the required dependencies (see [package.json](./package.json) for more details).
```sh
npm intall
```

## Getting Started
After installing the dependenices as described above, you may launch the client in your browser by running the following command inside this directory:
```sh
npm run dev
```

This will launch the development application server.
You can now access the client by directing your browser to [http://localhost:3000](http://localhost:3000).