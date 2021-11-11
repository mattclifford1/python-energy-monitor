#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 17:03:19 2021

@author: ri21540
"""
import pytest
import energy_monitor
import os

def test_log_data():
    dictionary = {'Time': 10.23, 'Energy 1': 100.23, 'Energy 2': 54.92}
    csv_filepath = os.path.join(os.getcwd(), 'energy_monitor', 'tests', 'data', 'test_write.csv')
    energy_monitor.utils.log_data(csv_filepath, dictionary)

    # TODO: test this with a csv_reader
