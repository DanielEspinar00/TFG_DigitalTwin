import sys
import Ice
import random
import digitaltwin
import asyncio
import sys

import unittest

from configparser import ConfigParser

# Config file
config = ConfigParser()

FILE_NAME = 'gw_sim.config'

PROXY = ''
FACILITY_ID = 'Testing_'
DEVICE_ID = 'Testing_'

try:
    config.read(FILE_NAME)

    PROXY = config.get('zeroc_ice','dt.Server')
    FACILITY_ID = FACILITY_ID + config.get('zeroc_ice','FacilityID')
    DEVICE_ID = DEVICE_ID + config.get('zeroc_ice','DeviceID')

except:
    print("\nERROR trying to read configuration file '"+FILE_NAME+"'\nExpected:\n" +
          "Section -> zeroc_ice\n\tkey -> 'dt.Server'\n\tkey -> 'FacilityID'\n\tkey -> 'DeviceID'\n")
    exit(-1)

dt = None
num = round(random.random(), 2)

class PruebaUnitaria(unittest.TestCase):

    def test_putSingleData(self):
        dt.putSingleDataReading(FACILITY_ID, DEVICE_ID, digitaltwin.TypeSingleData.Temperature, num)

    def test_putDataSet(self):
        dt.putDataSetReading(FACILITY_ID, DEVICE_ID, digitaltwin.TypeDataSet.Accelerometer, digitaltwin.DataSet(num, num, num))

    def test_getSingleData(self):
        a = dt.getSingleDataReading(FACILITY_ID, DEVICE_ID, digitaltwin.TypeSingleData.Temperature)
        self.assertEqual(round(a, 2), num)

    def test_getDataSet(self):
        b = dt.getDataSetReading(FACILITY_ID, DEVICE_ID, digitaltwin.TypeDataSet.Accelerometer)
        self.assertEqual(round(b.x, 2), num)
    
    def test_updateSingleDataLimits(self):
        lim = digitaltwin.SingleDataLimits(num + 1, num -1)
        dt.updateSingleDataLimits(FACILITY_ID, DEVICE_ID, digitaltwin.TypeSingleData.Temperature, lim)
    
    def test_updateDataSetLimits(self):
        lim = digitaltwin.DataSetLimits(num + 1, num -1, num + 1, num -1, num + 1, num -1)
        dt.updateDataSetLimits(FACILITY_ID, DEVICE_ID, digitaltwin.TypeDataSet.Accelerometer, lim)

    def test_getSingleDataLimits(self):
        a = dt.getSingleDataLimits(FACILITY_ID, DEVICE_ID, digitaltwin.TypeSingleData.Temperature)
        self.assertEqual(round(a.maxLimit, 2), num+1)

    def test_getDataSetLimits(self):
        b = dt.getDataSetLimits(FACILITY_ID, DEVICE_ID, digitaltwin.TypeDataSet.Accelerometer)
        self.assertEqual(round(b.xMinLimit, 2), num-1)
        
    
class gw(Ice.Application):

    def run(self, argv):
        global dt
        proxy = self.communicator().stringToProxy(PROXY)

        dt = digitaltwin.dataSinkPrx.checkedCast(proxy)
        if not dt:
            raise RuntimeError("Invalid proxy")

        unittest.main()


async def main():
    sys.exit(gw().main(sys.argv))

asyncio.run(main())
