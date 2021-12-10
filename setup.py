# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

from setuptools import setup, find_packages

import energy_monitor

# TODO: make more like https://github.com/fat-forensics/fat-forensics/blob/master/setup.py

setup(name='energy_monitor',
      version='0.7.5',
      packages=find_packages(),
      install_requires=['numpy', 'tqdm', 'pandas', 'dash', 'plotly', 'psutil', 'dash-bootstrap-components'],
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="CPU energy monitoring and displaying'",
      scripts=['scripts/display-energy'])
