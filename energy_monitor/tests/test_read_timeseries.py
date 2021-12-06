#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test functionality for reading timeseries data
"""

import pytest
import energy_monitor

def test_read_timeseries():
    filename = 'energy_monitor/tests/data_examples/PwrData_2021-10-29-13-2-26.csv'
    column_names = ['System Time', ' CPU Utilization(%)', 'IA Power_0(Watt)', 'Cumulative GT Energy_0(mWh)', 'GT Frequency(MHz)']
    list_result_0 = energy_monitor.utils.read_timeseries(column_names[0], filename)
    list_result_1 = energy_monitor.utils.read_timeseries(column_names[1], filename)
    list_result_2 = energy_monitor.utils.read_timeseries(column_names[2], filename)
    list_result_3 = energy_monitor.utils.read_timeseries(column_names[3], filename)
    list_result_4 = energy_monitor.utils.read_timeseries(column_names[4], filename)
    assert list_result_0 == ['13:02:29:923', '13:02:30:030', '13:02:31:750', '13:02:32:302', '13:02:33:107', '13:02:34:922', '13:02:37:082', '13:02:38:251', '13:02:40:239', '13:02:41:317', '13:02:42:597', '13:02:44:748', '13:02:44:842', '13:02:45:083', '13:02:45:668', '13:02:47:805', '13:02:49:665', '13:02:51:282', '13:02:53:246', '13:02:55:635', '13:02:55:683', '13:02:55:897', '13:02:57:318', '13:02:59:238', '13:03:01:699']
    assert list_result_1 == [16.0, 37.0, 59.0, 34.0, 29.0, 36.0, 60.0, 19.0, 15.0, 21.0, 17.0, 36.0, 56.0, 16.0, 27.0, 21.0, 26.0, 22.0, 31.0, 28.0, 24.0, 29.0, 15.0, 32.0, 14.0]
    assert list_result_2 == [2.971, 1.843, 6.153, 5.955, 3.293, 3.891, 4.024, 4.856, 1.911, 1.53, 2.149, 1.76, 2.771, 4.966, 1.841, 2.802, 2.259, 2.443, 2.128, 3.014, 1.861, 2.47, 1.966, 1.943, 3.172]
    assert list_result_3 == [0.082, 0.082, 0.13, 0.204, 0.268, 0.32, 0.404, 0.442, 0.498, 0.53, 0.574, 1.042, 1.073, 1.27, 1.478, 1.618, 1.702, 1.762, 1.827, 2.451, 2.484, 2.629, 3.129, 3.262, 3.389]
    assert list_result_4 == [99999999.0, 17.0, 3.0, 134.0, 62.0, 12.0, 20.0, 18.0, 12.0, 12.0, 20.0, 99999999.0, 172.0, 579.0, 155.0, 34.0, 25.0, 24.0, 19.0, 99999999.0, 199.0, 635.0, 106.0, 17.0, 14.0]
