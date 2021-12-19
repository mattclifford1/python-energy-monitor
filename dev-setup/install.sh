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
pip install -r requirements-dev.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html

# install current dir in editable mode
pip install -e ..
