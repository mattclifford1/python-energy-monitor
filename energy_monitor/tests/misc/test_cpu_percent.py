'''
test cpu_util.py functionality is correct
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import time
import energy_monitor
import os

def test_args():
    tdp = 20
    inter = 0.1
    print(os.getcwd())
    print(dir(energy_monitor))
    print(dir(energy_monitor.utils))
    energy_monitor.utils.dummy_compute(2)
    energy_monitor.utils.test_func()
    m = energy_monitor.cpu_percent.start_recording(TDP=tdp, interval=inter)
    assert m.TDP == tdp
    assert m.interval == inter

if __name__ == '__main__':
    test_args()
