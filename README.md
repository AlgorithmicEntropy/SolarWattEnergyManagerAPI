# SolarWattEnergyManagerAPI
A python3 library to access the data of a solar watt energy manager

This library returns the current power data of your solar array via the unofficial local api.

## Installation

```
pip install SolarWattEnergyManagerAPI
```

## Usage
```
from SolarWattEnergyManagerAPI.SolarWatt import EnergyManagerAPI

# create a new api object
api = EnergyManagerAPI()

# set host or ip of energy manager device
api.set_host('hostname or ip')

# optional, change log level
api.set_log_level('WARNING')

# optional, change work units to Wh instead of kWh
from SolarWattEnergyManagerAPI.units import WorkUnit
api.set_unit(WorkUnit.Wh)

# test the connection (returns bool based on success)
result = api.test_connection()

# pull data from the device (retuirn dictionary with power values)
data = api.pull_data()
```

