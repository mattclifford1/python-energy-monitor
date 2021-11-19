#!/bin/bash
# script to setup python virtual env with conda

# make sure conda is accessable
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

# create virtual env
VENV=energy_monitor
conda create -n $VENV python=3.8
conda activate $VENV

# install dependancies
pip install --upgrade pip
#pip install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
pip install -r requirements-test.txt

# install current dir in editable mode
pip install -e .

# run tests
pytest energy_monitor/tests/misc
