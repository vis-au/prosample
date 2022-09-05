# ProSample

This repository contains the code for a visual demonstration tool for the dynamic sampling pipeline for Progressive Visual Analytics (PVA), and the code for recreating the figures in our paper.
The tool allows to visually compare two pipeline configurations in a side-by-side view, for example to decide on the best sampling configuration for a task at hand or to explore the design space of the sampling pipeline.

The repository contains two main directories: [client/](./client), which contains the web-based frontend, [server/](./server), which contains the pipeline implementation and the server backend.

## Installation
Client and server need to be installed separately.
Follow the instructions in the respective directories for more details.


## Recreating figures from our paper
The computational notebook for recreating the figures in our paper can be found in [server/pipeline/figures.ipynb](server/pipeline/figures.ipynb).
Please note that you need to download this entire repository, before running any notebook cells.
