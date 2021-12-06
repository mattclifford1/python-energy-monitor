'''
Basic usage of pyJoules to print out energy usage of a function
'''
from pyJoules.energy_meter import measure_energy
import numpy as np
from tqdm import tqdm

@measure_energy
def foo():
    for i in tqdm(range(20)):
        a = np.arange(3*40*5*600).reshape((3,40,5,600))
        b = np.arange(3*40*5*600)[::-1].reshape((5,40,600,3))
        np.dot(a, b)[2,3,2,1,2,2]
    return

foo()
