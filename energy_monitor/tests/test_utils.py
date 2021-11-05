import energy_monitor
from datetime import datetime

def test_date_construction():
    date = datetime(2009, 10, 5, 18, 00)
    # TODO: change to utils not wrappper
    assert energy_monitor.powergadget_wrapper.get_date_string(date) == '2009-10-5-18-0-0'
