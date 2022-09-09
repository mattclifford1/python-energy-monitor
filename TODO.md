# TODO: include nvidia GPU wattage
plan: use [nvidia-ml-py](https://pypi.org/project/nvidia-ml-py/)
```
$ pip install nvidia-ml-py
```
## How to get wattage
```
import pynvml

pynvml.nvmlInit()
h = pynvml.nvmlDeviceGetHandleByIndex(0)  # or input index
power = pynvml.nvmlDeviceGetPowerUsage(h)

nvmlShutdown()
```

(might also be able to monitor utilization and memory usage) -- look into their [github](https://github.com/jonsafari/nvidia-ml-py))
