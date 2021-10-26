#!/bin/bash
# script to setup python virtual env with conda
VENV=energy_monitor
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate $VENV

conda create -n $VENV python=3.8
conda activate $VENV

pip install --upgrade pip
# install dependancies
pip install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
# install current dir in editable mode
pip install -e .
