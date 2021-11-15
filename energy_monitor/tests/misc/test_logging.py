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
    csv_filepath = os.path.join(os.getcwd(), 'energy_monitor', 'tests', 'data_examples', 'test_write.csv')
    if os.path.isfile(csv_filepath):
        os.remove(csv_filepath)
    energy_monitor.utils.log_data(csv_filepath, dictionary)

    result = energy_monitor.utils.read_results(csv_filepath)
    assert result['Time'][-1] == 10.23
    assert result['Energy 1'][-1] == 100.23
    assert result['Energy 2'][-1] == 54.92
    os.remove(csv_filepath)

if __name__ == '__main__':
    test_log_data()
