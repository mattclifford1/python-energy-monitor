#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:08:34 2021

@author: ri21540
"""

import pytest
import energy_monitor

def test_read():
    filename = 'energy_monitor/tests/data/test1.csv'
    dict_result = energy_monitor.utils.read_results(filename)
    assert list(dict_result.keys()) == ['Time', 'Energy 1', 'Energy 2']
    assert dict_result['Time'] == [10.23, 10.23]
    assert dict_result['Energy 1'] == [100.23, 100.23]
    assert dict_result['Energy 2'] == [54.92, 54.92]
