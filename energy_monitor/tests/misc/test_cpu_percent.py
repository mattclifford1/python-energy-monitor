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
    m = energy_monitor.cpu_percent.start_recording(TDP=tdp, interval=inter)
    assert m.TDP == tdp
    assert m.interval == inter
    m.stop()

def test_values():
    m = energy_monitor.cpu_percent.start_recording(TDP=15, interval=0.1)
    energy_monitor.utils.dummy_compute(10)
    data = m.stop()
    assert type(data['timeseries']) == list
    assert type(data['mean']) == float
    assert type(data['duration']) == float
    assert type(data['Watts']) == float
    assert type(data['Joules']) == float

def test_recorded1():
    m = energy_monitor.cpu_percent.start_recording(TDP=15, interval=0.1)
    time.sleep(0.15) # slightly more than interval to make sure recorded
    data = m.stop()
    assert len(data['timeseries']) == 1

def test_recorded2():
    m = energy_monitor.cpu_percent.start_recording(TDP=15, interval=0.1)
    time.sleep(0.25) # slightly more than interval to make sure recorded
    data = m.stop()
    assert len(data['timeseries']) == 2
