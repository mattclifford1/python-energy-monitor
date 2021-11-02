'''
utility helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import numpy as np
from tqdm import tqdm


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
read joules from csv file (mauro update this)
'''
def read_joules(csv_file):
    with open(csv_file, 'r') as file:
        joules = file.readlines()[-3]
    return float(joules[34:-1])

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
