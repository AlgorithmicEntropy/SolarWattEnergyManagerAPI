# LocalSolarWatt
A python3 library to access the data of a solar watt energy manager

This library returns the current power data of your solar array via the unofficial local api.

## Installation

```
pip install LocalSolarWatt
```

## Usage
```
from LocalSolarWatt import EnergyManager, WorkUnits

# create a new api object
api = EnergyManager('hostname or ip')

# optional, change work units to Wh instead of kWh
from SolarWattEnergyManagerAPI.units import WorkUnit
api = EnergyManager('hostname or ip', work_unit=WorkUnits.Wh)

# optional, change log level
api.set_log_level('WARNING')

# test the connection (returns bool based on success)
status, data = api.test_connection()

# pull data from the device (retuirn dictionary with power values)
print(api.pull_data())
```

