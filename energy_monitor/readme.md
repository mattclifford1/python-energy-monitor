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
