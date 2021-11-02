'''
class to access CLI functionality of intel power gadget
TODO:
    - update to get more info that just joules?
    - test for mac - application default binary
    - find better way than sleep.wait(1) to wait for IntelPowerGadget app to open
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import subprocess
import platform
from datetime import datetime, timedelta
import time
from energy_monitor import utils

class monitor:
    def __init__(self, non_standard_location=False):
        self.system_os = platform.system()
        self.non_standard_location = non_standard_location
        self.app_running = False
        self.recording = False
        self.locate_bin()

    def __enter__(self):
        # for use with 'with' statement enter
        return self

    def locate_bin(self):
        if self.non_standard_location: # user provided alternate binary file location
            if type(self.non_standard_location) not in [str]:  # check valid input format
                raise ValueError('argument: non_standard_location={arg} needs to be type str'.format(arg=repr(self.non_standard_location)))
            else:
                self.bin = self.non_standard_location
        else: # use standard application binary location
            if self.system_os == 'Windows':
                self.bin = '"C:\\Program Files\\Intel\\Power Gadget 3.6\\IntelPowerGadget.exe"'
            elif self.system_os == 'Darwin':
                self.bin = '/Applications/Intel/IntelPowerGadget.bin'

    def start(self):
        self.open_app() # make sure IntelPowerGadget is running
        time.sleep(0.1)  # quick calls to 'start' sometimes fail
        os.system(self.bin + ' -start')
        self.start_time = datetime.now() # log start time to know file name
        self.recording = True

    def open_app(self):
        # open in a subprocess so we dont have to wait for a return which causes code to hang
        self.proc = subprocess.Popen(self.bin)
        time.sleep(1) # TODO: find better way to know when program has opened (it doesn't return and codes from CLI)
        self.app_running = True

    def stop(self):
        if self.recording:
            os.system(self.bin + ' -stop')  # CLI stop recording
            while not self.csv_exists(): # wait for csv to be created
                time.sleep(0.1)
            while not utils.check_written(self.csv_file): # wait for csv to be written
                time.sleep(0.1)
            self.recording = False
        # save what we need from csv
        self.joules = utils.read_joules(self.csv_file)
        # close recording
        self.kill_proc()
        # remove csv log
        os.remove(self.csv_file)

    def csv_exists(self):
        for file in self.get_csv_list():
            if os.path.isfile(file):
                self.csv_file = file
                return True
        return False

    def get_csv_list(self):
        '''
        get start time +-1 second incase of discrepancies
        '''
        csv_list = []
        start_datetime = self.start_time
        for sec in [-1, 0, 1]:
            adjusted_datetime = start_datetime + timedelta(seconds=sec)
            csv_list.append(self._csv_name(adjusted_datetime))
        return csv_list

    def _csv_name(self, datetime_obj):
        name = 'PwrData_'
        name += str(datetime_obj.year) + '-'
        name += str(datetime_obj.month) + '-'
        name += str(datetime_obj.day) + '-'
        name += str(datetime_obj.hour) + '-'
        name += str(datetime_obj.minute) + '-'
        name += str(datetime_obj.second)
        name += '.csv'
        return os.path.join(os.path.expanduser("~"), 'Documents', name)

    def kill_proc(self):
        if self.app_running:
            self.proc.kill()
            self.app_running = False

    def __exit__(self, exc_type, exc_value, traceback):
        # for use with 'with' statement exit
        self.kill_proc()

    def __del__(self):
        # close app upon garbage collection
        self.kill_proc()

if __name__ == '__main__':
    # with monitor() as mon1:
    mon1 = monitor()
    mon1.start()
    utils.dummy_compute(20)
    mon1.stop()
    print('Joules used: ', mon1.joules)
