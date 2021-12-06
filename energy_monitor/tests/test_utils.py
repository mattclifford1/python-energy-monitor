import energy_monitor
from datetime import datetime

def test_date_construction():
    date = datetime(2009, 10, 5, 18, 00)
    assert energy_monitor.utils.get_date_string(date) == '2009-10-5-18-0-0'
