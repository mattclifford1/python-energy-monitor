'''
utility helper functions
'''
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
