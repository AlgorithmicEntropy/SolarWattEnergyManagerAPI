# LocalSolarWatt
A python3 library to access the data of solar watt devices via local api  
Disclaimer: This library uses an unofficial local api and could therefore break at any point

# Overview
The package wraps both the kiwigrid energy manager api and the myReserve api.  
Data available:
  - energy manager: current power, energy counters, diagnostics
  - my reserve: hex status codes, current power (same as web interface)

As the myReserve api only returns small amount of data and gets polled by the web interface anyway,  
it is the preferred option for realtime data.  
Polling the energy manager to often could lead to reliability issues (untested).

## Installation

```
pip install LocalSolarWatt
```

## Usage
```
from LocalSolarWatt import EnergyManager, MyReserve, WorkUnits

# create a new api objects
energy_api = EnergyManager('hostname or ip')
my_reserve_api = MyReserve('hostname or ip')

# optional, change work units to Wh instead of kWh
from SolarWattEnergyManagerAPI.units import WorkUnit
api = EnergyManager('hostname or ip', work_unit=WorkUnits.Wh)

# below functions work on both energy manager and my reserve
# optional, change log level
api.set_log_level('WARNING')

# test the connection (returns bool based on success)
status, data = api.test_connection()

# pull data from the device (retuirn dictionary with power values)
print(api.pull_data())
```

# Tests:
If you want to run the tests locally make sure to set the following environment variables to correct IPs / hostnames
```
ENERGY_MANAGER_HOST
MY_RESERVE_HOST
```

