'''
utility helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import numpy as np
from tqdm import tqdm
import re
from csv import reader 

'''
dummy function for testing with
'''
def dummy_compute(iters=20):
    for i in tqdm(range(iters)):
        a = np.arange(3*40*5*600).reshape((3,40,5,600))
        b = np.arange(3*40*5*600)[::-1].reshape((5,40,600,3))
        np.dot(a, b)[2,3,2,1,2,2]
    return

'''
read joules from csv file
'''
def read_joules(csv_file):
    dict_results = dict()
    with open(csv_file, 'r') as file:
        line = reader(file)
        for row in line:
            if len(row) > 0 and bool(re.match(r"Average IA Power", row[0])):
                dict_results['average_ia'] = float(re.findall(r"\d+\.\d+", row[0])[0])
            elif len(row) > 0 and bool(re.match(r"Total Elapsed Time", row[0])):
                dict_results['time'] = float(re.findall(r"\d+\.\d+", row[0])[0])
            elif len(row) > 0 and bool(re.match(r"Cumulative IA Energy_\d+ \(Joules\)", row[0])):
                dict_results['cumulative_ia'] = float(re.findall(r"\d+\.\d+", row[0])[0])
    return dict_results

def check_written(file):
    '''
    check if a file has done being written todo
    '''
    try:
        f = open(file, 'r')
        f.close()
        return True
    except PermissionError:
        return False
