'''
create some example data for dev usage

useage: will save to './example.csv' (pwd)
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from energy_monitor import monitor, utils, train_mnist

logfile = './example.csv'
names = ['Dummy Compute', 'Train Mnist']
funcs = [utils.dummy_compute, train_mnist.main]
for i in range(len(names)):
    for background in [False, True]:
        mon = monitor(name=names[i],
                       remove_background_energy=background,
                       log_filepath=logfile)
        mon.start()
        funcs[i]()
        mon.stop()
