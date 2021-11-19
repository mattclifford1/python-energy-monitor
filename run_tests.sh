#!/bin/bash
# script to setup python virtual env with conda

# make sure conda is accessable
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

# create virtual env
VENV=energy_monitor
conda activate $VENV

# run tests
pytest energy_monitor/tests/misc
