#!/bin/bash
# run tests on server (CI)

# make sure conda is accessable
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

# activate virtual env
VENV=energy_monitor
conda activate $VENV

# run tests
pytest energy_monitor/tests/misc
