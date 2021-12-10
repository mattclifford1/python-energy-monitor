# Monitoring Energy Example
To monitor the energy of python code, wrap it with start and stop:

```
import energy_monitor

monitor.start()
### write your code here
monitor.stop()
joules_used = monitor.joules
```

# Dev
[powergadget_wrapper.py](./powergadget_wrapper.py) contains the functionality to interact with as process data from IntelPowerGadget.
[cpu_percent.py(./cpu_percent.py) contains cpu monitoring and wattage/joules estimation for non intel cpus.
[dash_app.py](./dash_app.py) contains the dashboard application.
[utils.py](./utils.py) contains data managements and other helper functionality.
[train_mnist.py](./train_mnist.py) contains an example script to train a networks (used to quickly stress the CPU).
