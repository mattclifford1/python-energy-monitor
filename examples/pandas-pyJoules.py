'''
parse pyJoules data to pandas dataframe
'''
import pyJoules
from pyJoules.handler.pandas_handler import PandasHandler
from pyJoules.energy_meter import EnergyContext
from pyJoules.device.rapl_device import RaplPackageDomain
from energy_monitor import utils, train_mnist

def record_energy(func, cpu_socket=0):
    pandas_handler = PandasHandler()
    # remove the domains arg to monitor all parts
    with EnergyContext(handler=pandas_handler,
                       domains=[RaplPackageDomain(cpu_socket)], # cpu socket
                       start_tag='record_pandas') as ctx:
        func()
        # ctx.record(tag='10iters')
        # utils.dummy_compute(10)
    df = pandas_handler.get_dataframe()

    # Print results
    print(f'Full DataBase:\n {df} \n')
    uJoules = df['package_0'][0]
    time = df['duration'][0]
    Joules = uJoules/1000000
    return Joules, time

if __name__ == '__main__':
    # numpy test
    Joules, time = record_energy(utils.dummy_compute)
    print(f'{Joules:.2f} Joules used in {time:.2f} seconds' )
    print(f'Average power: {Joules/time:.2f} Watts' )
    # pytorch test
    Joules, time = record_energy(train_mnist.main)
    print(f'{Joules:.2f} Joules used in {time:.2f} seconds' )
    print(f'Average power: {Joules/time:.2f} Watts' )
