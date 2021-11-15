# Python tests

Run all tests with `$ pytest` from the base dir.

# Docker tests

To run all tests that don't depend on hardware energy monitoring run `$ pytest energy_monitor/tests/misc`. (Containerised code cannot access hardware energy monitoring)
