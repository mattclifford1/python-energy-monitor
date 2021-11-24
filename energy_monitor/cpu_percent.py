'''
cpu % utilisation monitor/logging

usage:
    args:
        - TDP (int):         wattage of CPU (thermal design power)
        - interval (float):  frequency to sample % cpu utilisation (0.5 default)

    methods:
        - start()           starts monitoring (automatically called from __init__)
        - stop():           stops monitoring

    attributes:
        - data (dict):      contains all relevant data collected and estimated
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import threading
from datetime import datetime, timedelta
import psutil

class start_recording:
    def __init__(self, TDP, interval=0.5):
        self.TDP = TDP
        self.interval = interval
        self.monitoring = False
        self.start()

    def start(self):
        self.measurements = []
        self.data = {}
        self.monitoring = True
        self._thread_monitor = threading.Thread(target=self._record, args=())
        self._thread_monitor.daemon = True
        self.start_time = datetime.now()
        self.end_time = datetime.now() # initialisation
        self._thread_monitor.start()

    def _record(self):
        while self.monitoring:
            self.measurements.append(psutil.cpu_percent(interval=self.interval))
            self.end_time = datetime.now()

    def stop(self):
        self._stop_thread()
        self.time_taken = self.end_time - self.start_time
        if len(self.measurements) == 0:
            self.mean_cpu = 0
        else:
            self.mean_cpu = sum(self.measurements)/len(self.measurements)
        self.mean_watts = (self.mean_cpu/100)*self.TDP
        self.duration = self.time_taken.total_seconds()
        self.data = {'cpu utilisation': self.measurements,
                     'mean' :self.mean_cpu,
                     'time': self.duration,
                     'average_ia': self.mean_watts,
                     'cumulative_ia': self.mean_watts*self.duration}
        return self.data

    def _stop_thread(self):
        if self.monitoring:
            self.monitoring = False # send signal to thread to stop job
            # could also kill the thread explictly

    def __str__(self):
        return str(self.data)

    def __enter__(self):
        # for use with 'with' statement enter
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # for use with 'with' statement exit
        self._stop_thread()

    def __del__(self):
        # close app upon garbage collection
        self._stop_thread()

#
# if __name__ == '__main__':
#     # import time
#     # from energy_monitor import utils
#     m = start_recording(TDP=15)
#     utils.dummy_compute(20)
#     m.stop()
#     print(m)
