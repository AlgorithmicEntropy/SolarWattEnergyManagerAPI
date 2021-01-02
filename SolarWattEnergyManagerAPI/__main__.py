import SolarWattEnergyManagerAPI as energyManagerApi

if __name__ == "__main__":
    # create a new api object
    api = energyManagerApi.EnergyManagerAPI()
    # set host or ip of energy manager device
    api.set_host('hostname or ip')
    # optional, change log level
    api.set_log_level('WARNING')
    # test the connection (returns bool)
    result = api.test_connection()
    # pull data from the device (dictionary)
    data = api.pull_data()
