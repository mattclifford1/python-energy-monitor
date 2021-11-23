# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

from setuptools import setup, find_packages

import energy_monitor

# TODO: make more like https://github.com/fat-forensics/fat-forensics/blob/master/setup.py

setup(name='energy_monitor',
      version='0.3', 
      packages=find_packages(),
      install_requires=['numpy', 'tqdm', 'pandas'])
