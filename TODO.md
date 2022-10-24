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



# Existing implementations
Code Carbon monitors gpu usage already
### GPU initialisation
finding all devices and make handle [here](https://github.com/mlco2/codecarbon/blob/master/codecarbon/core/gpu.py#L173-L198)
### GPU power
many useful GPU functions [here](https://github.com/mlco2/codecarbon/blob/954cb8cec0197a63761206ccced4a0b223efb92f/codecarbon/core/gpu.py#L64)
