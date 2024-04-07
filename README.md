# LocalSolarWatt
A python3 library to access the data of solar watt devices via local api  
Disclaimer: This library uses an unofficial local api and could therefore break at any point

# Overview
The package uses the kiwigrid api provided by your solar watt energy manager device.  
Data available:
  - Real time power values from inverter, AC sensor and battery (if exists)
  - Long term energy statistics

This library does some preprocessing by extracting relevant fields and grouping them by device class.  
For now this mostly includes data I deem usefully for the integration with home assistant.

Note: Polling the energy manager with a very high interval often could lead to reliability issues (untested).

# Supported devices
As I only have access to one installation and the api is as far as I'm aware not documented by SolarWatt, I can not guarantee that this library works with your setup.  
If you encounter issues with your concrete setup, feel free to open a new issue.  
The raw json data is available via `http://YOUR_DEVICE_IP/rest/kiwigrid/wizard/devices`  
If you can provide the raw json dump, I can try to add support for your device.  
**Important Note**: This data does contain some sensitive information (especially for the "Location" device), so make sure to remove any sensitive data before sharing.

## Installation

```
pip install LocalSolarWatt
```

## Usage
```
from local_solar_watt import Api, WorkUnits, DeviceClass

# create a new api objects
energy_api = Api('hostname or ip')

# optional, change work units to Wh instead of kWh
api = Api('hostname or ip', work_unit=WorkUnits.Wh)

# optional, change log level
api.set_log_level('WARNING')

# test the connection (returns bool based on success)
status, data = api.test_connection()

# pull data from the device (returns only selected power values, grouped by device class)
print(api.pull_data())

# You can also pull the raw json data for your own parsing needs
print(api.pull_raw())
```

# Tests:
If you want to run the tests locally make sure to set the following environment variables to correct IPs / hostnames
```
ENERGY_MANAGER_HOST
```

