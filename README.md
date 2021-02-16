# Dublin Energy Modelling

A collection of notebooks using EnergyPlus (E+), eppy and docker to automate E+ archetype creation. 
Utilization of a conda environment from within a docker container.

Produces energy, electricity, heat and peak electricity demands at a small-area and postcode level at both commercial and residential sectors for Dublin, Ireland.

## Installation

Install [`docker`](https://www.docker.com/get-started) and run:

```bash
git clone https://github.com/codema-dev/dublin-energy-model
docker build -t dem .
docker run --rm -it -v $(pwd):/DEM/ --workdir /DEM/ dem
poetry install
```

If using `vscode` can use the [`Remote - Containers`](https://github.com/Microsoft/vscode-remote-release) extension to `Attach to a Running Container` and run all code & notebooks from within `vscode` 