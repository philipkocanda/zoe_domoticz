from fcache.cache import FileCache
from pyze.api import Gigya, Kamereon, Vehicle
from domoticz import Domoticz
import yaml

class Main:
    def __init__(self):
        with open('config.yml', 'r') as ymlfile:
            self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.cache = FileCache('zoe-domoticz', flag='cs')
        self.domoticz = Domoticz(self.config)

        # PyZE stuff:
        self.gigya = Gigya()
        self.login()
        self.kamereon = Kamereon(gigya=self.gigya, country=self.config['myRenaultCountry'])
        self.vehicle = Vehicle(self.config['myRenaultVIN'], self.kamereon)

    def login(self):
        # Login only needs to be called once and credentials are cached by pyze (?)
        self.gigya.login(self.config['myRenaultEmail'], self.config['myRenaultPassword'])
        self.gigya.account_info() # Retrieves and caches person ID

    def updateDomoticz(self, batt, hvac, mileage):
        print("Updating data in Domoticz...\n")

        dz = self.domoticz
        config = self.config

        if batt['chargeStatus'] == 1:
            dz.setPower(config['dzChargePowerId'], batt['instantaneousPower'])
        else:
            dz.setPower(config['dzChargePowerId'], 0)

        dz.setValue(config['dzBatteryPercentageId'], batt['batteryLevel'])
        dz.setValue(config['dzRangeId'], batt['rangeHvacOff'])
        dz.setValue(config['dzBatteryTempId'], batt['batteryTemperature'])
        dz.setValue(config['dzExternalTempId'], hvac['externalTemperature'])
        dz.setValue(config['dzMileageId'], mileage['totalMileage'])
        dz.setSwitch(config['dzPlugStateId'], batt['plugStatus'] == 1)

        print("Update success!")

    def execute(self):
        cache = self.cache
        batt = self.vehicle.battery_status()
        hvac = self.vehicle.hvac_status()
        mileage = self.vehicle.mileage()

        if self.config['debug'] == True:
            self.printDebugInfo(batt, hvac, mileage)

        if 'lastUpdateTime' in cache:
            lastUpdateTime = cache['lastUpdateTime']
        else:
            lastUpdateTime = 'never'

        if batt['lastUpdateTime'] != lastUpdateTime:
            print("Last update at: %s, updating!" % lastUpdateTime)
            cache['lastUpdateTime'] = batt['lastUpdateTime']
            self.updateDomoticz(batt, hvac, mileage)
        else:
            print("Last update at %s, skipping update." % lastUpdateTime)

    def printDebugInfo(self, batt, hvac, mileage):
        print("Battery Status:")
        print(batt)

        # When plugged in and charging:
        # {'rangeHvacOff': 134, 'plugStatus': 1, 'chargePower': 1, 'lastUpdateTime': '2019-10-20T10:33:48+02:00',
        # 'batteryTemperature': 16, 'chargeStatus': 1, 'batteryLevel': 99, 'instantaneousPower': 1600}

        # When plugged in and not charging:
        # {'plugStatus': 1, 'lastUpdateTime': '2019-10-20T11:07:04+02:00', 'batteryTemperature': 15,
        # 'chargeStatus': -1, 'batteryLevel': 100, 'rangeHvacOff': 137}

        print("\nHVAC Status:")
        print(hvac)
        # {'hvacStatus': 'off', 'externalTemperature': 10.0}

        print("\nMileage:")
        print(mileage)
        # {'totalMileage': 55506}

Main().execute()
