'''
test functions to analyse energy monitoring wrapper to intel power gadget
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os
import platform
import pytest
import energy_monitor

def test_standard_input():
    # standard input args
    monitor = energy_monitor.monitor()
    if platform.system() == 'Windows':
        assert monitor.bin == '"C:\\Program Files\\Intel\\Power Gadget 3.6\\IntelPowerGadget.exe"'

def test_non_standard_input():
    # non standard file location
    monitor = energy_monitor.monitor(non_standard_location='/bin/loc.bin')
    assert monitor.bin == '/bin/loc.bin'

def test_input_error():
    # # test error for non string
    args=[True, 0.1]
    for arg in args:
        with pytest.raises(ValueError) as val_error:
            monitor = energy_monitor.monitor(non_standard_location=arg)
        assert str(val_error.value) == 'argument: non_standard_location={arg} needs to be type str'.format(arg=repr(arg))

def test_joules_value():
    monitor = energy_monitor.monitor()
    monitor.start()
    energy_monitor.utils.dummy_compute(2)
    monitor.stop()
    assert type(monitor.joules) == float

def test_csv_removed():
    monitor = energy_monitor.monitor()
    monitor.start()
    energy_monitor.utils.dummy_compute(2)
    monitor.stop()
    assert os.path.exists(monitor.csv_file) == False
    
def test_read_joules():
    file_names = ['PwrData_2021-10-29-13-4-0.csv,
                  'PwrData_2021-10-29-13-2-26.csv',
                  'PwrData_2021-10-29-13-3-19.csv',
                  'PwrData_2021-10-29-13-2-14.csv']
    list_joules = []
    for idx, file_name in enumerate(file_names):
        list_joules.append(energy_monitor.utils.read_joules(file_name))
    assert list_joules == ['1.511089', '2.934142', '1.778402', '1.605088']
        
        
        
