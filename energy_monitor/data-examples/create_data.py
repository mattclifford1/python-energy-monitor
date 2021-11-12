'''
create some example data for dev usage
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import energy_monitor

mon1 = monitor(remove_background_energy=True)
mon1.start()
utils.dummy_compute(20)
mon1.stop()
