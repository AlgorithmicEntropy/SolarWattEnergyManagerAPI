import SolarWattEnergyManagerAPI.EnergyManagerAPI as energyManagerApi

if __name__ == "__main__":
    api = energyManagerApi.EnergyManagerAPI('hostname or ip')
    api.test_connection()
    data = api.pull_data()
    print(data)