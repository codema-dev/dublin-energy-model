# Dublin Energy Modelling

A collection of notebooks using EnergyPlus (E+), eppy and docker to automate E+ archetype creation. 
Utilization of a conda environment from within a docker container.

Produces energy, electricity, heat and peak electricity demands at a small-area and postcode level at both commercial and residential sectors for Dublin, Ireland.

## Installation

- Install [`docker`](https://www.docker.com/get-started)

- Clone this repository

```bash
git clone https://github.com/codema-dev/dublin-energy-model
```

### a. VSCode (recommended)
 
- Install [VSCode](https://code.visualstudio.com/Download)

- Install the [`Remote - Containers`](https://github.com/Microsoft/vscode-remote-release) extension.

- Run `Remote-Containers: Open Workspace in Container...`

### b. Command Line

> If you are on Windows; download [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to run the commands in a *nix shell 

- Run:

```bash
cd dublin-energy-model
docker build -t dem -f=./Dockerfile .
docker run --rm -it -v=$(pwd):/DEM/ --workdir=/DEM/ dem
```



