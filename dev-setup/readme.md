# Workflow
Create a new branch for any new feature updates. Once code is stable and passes all tests, push the branch to github. Create a pull request on github to merge into the main branch.

# Adding dependancies
Put any package required dependancies in [requirements.txt](./requirements.txt) and also put them in [.circleci/requirements-test.txt](.circleci/requirements-test.txt) if they are required for testing using CI.

# Adding tests
Put any tests to be run on CI in the folder [energy_monitor/tests/](energy_monitor/tests/misc). Make sure to write tests for **ALL** new functionality.

# Python Setup
Use either the automatic or manual setup process as described below

### Automatic Setup (Recommended)
Use the [install script](https://github.com/iaitp/2021-A/blob/main/dev-setup/install.sh) to set up automatically:
`$ ./install.sh`

### Manual Setup (Windows)

1. Create conda venv:

`$ conda create --name energy_monitor python=3.8`

2. Activate venv:

`$ conda activate energy_monitor`

3. Install dependancies with pip:

`$ pip install -r requirements-dev.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html`

4. Install current dir in editable mode:

`$ pip install -e .`

# Updating PyPi
### Automatically (Recommended)
Use the [script](https://github.com/iaitp/2021-A/blob/main/scripts/push-to-pypi.sh).

`
$ scripts/push-to-pypi.sh
`

### Manually (Windows)
First clean the repo of _pycache and other unstaged/untracked files by git

`$ git clean -xfd`

Then build the package wheel

`$ python setup.py sdist bdist_wheel`

And finally, upload to PyPi via twine

`$ twine upload dist/*`.
