'''
class to access CLI functionality of intel power gadget
TODO:
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
    '''
    monitor energy using IntelPowerGadget
    args:
        - name (str):
        - non_standard_binary_path: use if IntelPowerGadget is installed in a non stand location
        - log_filepath: where to log energy data to (default is inside user's Documents)
    '''
    def __init__(self, name='Monitor Test',
                       non_standard_binary_path=False,
                       log_filepath=os.path.join(os.path.expanduser("~"), 'Documents', 'energy_monitor_log.csv')):
        self.system_os = platform.system()
        self.name = name
        self.non_standard_binary_path = non_standard_binary_path
        self.log_filepath = log_filepath
        self.app_running = False
        self.recording = False
        self.locate_bin()
        # TODO: check log filepath is '.csv' format

    def __enter__(self):
        # for use with 'with' statement enter
        return self

    def locate_bin(self):
        if self.non_standard_binary_path: # user provided alternate binary file location
            if type(self.non_standard_binary_path) not in [str]:  # check valid input format
                raise ValueError('argument: non_standard_binary_path={arg} needs to be type str'.format(arg=repr(self.non_standard_binary_path)))
            else:
                self.bin = self.non_standard_binary_path
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
            while not self.check_PwrData_csv_exists(): # wait for csv to be created
                time.sleep(0.1)
            while not utils.check_written(self.csv_file): # wait for csv to be written
                time.sleep(0.1)
            self.recording = False
        # save what we need from csv
        self.power_gadget_data = utils.read_csv(self.csv_file)
        self.joules = self.power_gadget_data['cumulative_ia']
        # close recording
        self.kill_proc()
        # remove csv log
        os.remove(self.csv_file)
        # log monitor data
        self.power_gadget_data['date'] = utils.get_date_string(self.start_time)
        self.power_gadget_data['name'] = self.name
        utils.log_data(self.log_filepath, self.power_gadget_data)

    def check_PwrData_csv_exists(self):
        for file in utils.get_PwrData_csv(self.start_time):
            if os.path.isfile(file):
                self.csv_file = file
                return True
        return False

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
