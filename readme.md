[![CircleCI](https://circleci.com/gh/iaitp/2021-A/tree/main.svg?style=svg)](https://circleci.com/gh/iaitp/2021-A/tree/main)

# Energy Monitor Python Package
[energy_monitor](./energy_monitor) is a python package that automatically records, logs and visualises the energy comsuption of developing and testing python programs.

# Adding dependancies
Put any package required dependancies in [requirements.txt](./requirements.txt) and also put them in [.circleci/requirements-test.txt](.circleci/requirements-test.txt) if they are required for testing using CI.

# Adding tests
Put any tests to be run on CI in the folder [energy_monitor/tests/misc](energy_monitor/tests/misc). Make sure to write tests for *ALL* new functionality.

# Python Setup
Use either the automatic or manual setup process as described below

### Automatic Setup (Linux)
Use the install script to set up automatically:
`$ ./install.sh`

### Manual Setup

1. Create conda venv:

`$ conda create --name energy_monitor python=3.8`

2. Activate venv:

`$ conda activate energy_monitor`

3. Install dependancies with pip:

`$ pip install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html`

4. Install current dir in editable mode:

`$ pip install -e .`

# External Dependancies

We use [IntelPowerGadget](https://www.intel.com/content/www/us/en/developer/articles/tool/power-gadget.html) to monitor energy usage on Windows/MacOS. 
