[![CircleCI](https://circleci.com/gh/iaitp/2021-A/tree/main.svg?style=svg)](https://circleci.com/gh/iaitp/2021-A/tree/main)
[![PyPI version](https://badge.fury.io/py/energy-monitor.svg)](https://badge.fury.io/py/energy-monitor)

# Energy Monitor Python Package
[energy_monitor](./energy_monitor) is a python package that automatically records, logs and visualises the energy comsuption of developing and testing python programs.

# How to Use
## Installation
(Recommended) Get the latest stable version of the package, use the [PyPi download](https://pypi.org/project/energy-monitor):

`
$ pip install energy-monitor
`

To get the newest beta version (unstable), download via github

`
$ pip install git+https://github.com/iaitp/2021-A.git
`

## Logging CPU usage to database

```
import energy_monitor

monitor = energy_monitor.monitor()
monitor.start()
# call code to monitor here
monitor.stop()
```
### [energy_monitor::monitor](https://github.com/iaitp/2021-A/blob/main/energy_monitor/powergadget_wrapper.py#L15)
Args:
 - name (str): Human readable name to group the logging as
 - remove_background_energy (bool): whether to estimate and remove background energy usage from results. Default: False
 - log_filepath (str): Filepath to database to log results. Default: '~/Documents/energy_monitor.csv'
 - TDP (int): CPU wattage used to estimate power when IntelPowerGadget is unavailable. Default: 15

## Viewing results
Results are displayed in an interactive dash web browser application. To run the dashboard from linux or mac use the CLI

`
$ display-energy
`
display-energy take a single command line argument of the location of the database location (only needs to be specified if it is in a non-standard location).

Alternatevely you can launch the dashboard using the python API using

```
from energy_monitor import dash_app

dash_app.run()
```
### [energy_monitor::dash_app::run](https://github.com/iaitp/2021-A/blob/main/energy_monitor/dash_app.py#L24)
Args:
  - csv_file (str): file location of database. Default: '~/Documents/energy_monitor.csv'

### Using the Dashboard
Mauro write something here :) - include pictures of the dashboard along with what each graph shows/ the options avaible in the dropdowns and timeseries.

# How to Contribute
Follow the dev install and practices outlined in [dev-setup](./dev-setup).

# External Dependancies

We use [IntelPowerGadget](https://www.intel.com/content/www/us/en/developer/articles/tool/power-gadget.html) to monitor energy usage on Windows.
