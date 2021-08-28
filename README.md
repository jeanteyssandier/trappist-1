# trappist-1

This repository contains a python script to run a REBOUND(x) simulation of migrating planets. 
In this particular example, the setup corresponds to the 7 planets of the Trappist-1 system. 
As in [Tamayo et al. (2017)](https://ui.adsabs.harvard.edu/abs/2017ApJ...840L..19T/abstract),  only the outer planet migrates. Eccentricity damping is applied to all planets.

## Requirements

You'll need REBOUND ((https://github.com/hannorein/rebound) and REBOUNDx (https://github.com/dtamayo/reboundx):
```shell
pip install rebound
pip install reboundx
pip install numpy
```

## Execution

Usage:

```shell
python trappist1.py  [-n, RUN_NUMBER] [-v,]
```

Optional arguments:

* `-n RUN_NUMBER, --njob RUN_NUMBER` Run number, create a binary output file 'run*n*.bin'
* `-v, --verbose` Verbose mode, displays information every output step

## Output

Each job creates a REBOUND binary output file **run*n*.bin**.
See https://rebound.readthedocs.io/en/latest/simulationarchive/ for information on the REBOUND archive.
