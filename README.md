# trappist-1

This repository contains a python script to run Rebound(x) simulation. 
In this particular example, the setup corresponds to the 7 planets of the Trappist-1 system. 
As in Tamayo et al. (2017, https://ui.adsabs.harvard.edu/abs/2017ApJ...840L..19T/abstract), only the outer planet migrates. Eccentricity damping is applied to all planets.

## Requirements

You'll need Rebound and Reboundx:
```shell
pip install rebound
pip install reboundx
pip install numpy
```

## Execution

Usage:

```shell
usage: trappist1.py  [-n, RUN_NUMBER] [-v,]
```

Optional arguments:

* `-n RUN_NUMBER, --njob JOB_NUMBER` Run number, create a binary output file 'runN.bin'
* `-v, --verbose` Verbose mode, displays information every output step

## Output

Each job creates a Rebound binary output file **runN.bin**.
See https://rebound.readthedocs.io/en/latest/simulationarchive/ for information on the Rebound archive.
