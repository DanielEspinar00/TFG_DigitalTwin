import sys
import Ice

import digitaltwin
import sys
import asyncio

from configparser import ConfigParser


# Config file
config = ConfigParser()

FILE_NAME = 'limits.config'

PROXY = ''
FACILITY_ID = ''
DEVICE_ID = ''

acc_limits = []
gy_limits = []
mg_limits = []
temp_limits = []
prs_limits = []
hum_limits = []
lgt_limits = []

try:
    config.read(FILE_NAME)

    PROXY = config.get('zeroc_ice','dt.Server')
    FACILITY_ID = config.get('zeroc_ice','FacilityID')
    DEVICE_ID = config.get('zeroc_ice','DeviceID')

    UPDATE_ACC = config.getboolean('datatypes', 'Accelerometer')
    UPDATE_GY = config.getboolean('datatypes', 'Gyroscope')
    UPDATE_MG = config.getboolean('datatypes', 'Magnetometer')
    UPDATE_TEMP = config.getboolean('datatypes', 'Temperature')
    UPDATE_PRS = config.getboolean('datatypes', 'Pressure')
    UPDATE_HUM = config.getboolean('datatypes', 'Humidity')
    UPDATE_LGT = config.getboolean('datatypes', 'Light')

    if(UPDATE_ACC):
        acc_limits.append(config.getfloat('limits_acc', 'x_max'))
        acc_limits.append(config.getfloat('limits_acc', 'x_min'))
        acc_limits.append(config.getfloat('limits_acc', 'y_max'))
        acc_limits.append(config.getfloat('limits_acc', 'y_min'))
        acc_limits.append(config.getfloat('limits_acc', 'z_max'))
        acc_limits.append(config.getfloat('limits_acc', 'z_min'))

    if(UPDATE_GY):
        gy_limits.append(config.getfloat('limits_gy', 'x_max'))
        gy_limits.append(config.getfloat('limits_gy', 'x_min'))
        gy_limits.append(config.getfloat('limits_gy', 'y_max'))
        gy_limits.append(config.getfloat('limits_gy', 'y_min'))
        gy_limits.append(config.getfloat('limits_gy', 'z_max'))
        gy_limits.append(config.getfloat('limits_gy', 'z_min'))

    if(UPDATE_MG):
        mg_limits.append(config.getfloat('limits_mg', 'x_max'))
        mg_limits.append(config.getfloat('limits_mg', 'x_min'))
        mg_limits.append(config.getfloat('limits_mg', 'y_max'))
        mg_limits.append(config.getfloat('limits_mg', 'y_min'))
        mg_limits.append(config.getfloat('limits_mg', 'z_max'))
        mg_limits.append(config.getfloat('limits_mg', 'z_min'))

    if(UPDATE_TEMP):
        temp_limits.append(config.getfloat('limits_temp', 'x_max'))
        temp_limits.append(config.getfloat('limits_temp', 'x_min'))

    if(UPDATE_PRS):
        prs_limits.append(config.getfloat('limits_prs', 'x_max'))
        prs_limits.append(config.getfloat('limits_prs', 'x_min'))

    if(UPDATE_HUM):
        hum_limits.append(config.getfloat('limits_hum', 'x_max'))
        hum_limits.append(config.getfloat('limits_hum', 'x_min'))

    if(UPDATE_LGT):
        lgt_limits.append(config.getfloat('limits_lgt', 'x_max'))
        lgt_limits.append(config.getfloat('limits_lgt', 'x_min'))

except:
    print("\nERROR trying to read configuration file '"+FILE_NAME+"'\nExpected:\n"+
            "Section -> zeroc_ice\n\tkey -> 'dt.Server'\n\tkey -> 'FacilityID'\n\tkey -> 'DeviceID'\nSection -> <datatype>\n\tKey -> 'x_max'\n\tkey -> 'x_min'\n\tKey -> 'y_max'\n\tkey -> 'y_min'\n\tKey -> 'z_max'\n\tkey -> 'z_min'\n"+
            "(Decimal symbol: . )")
    exit(-1)

class manager(Ice.Application):
    FacilityID = FACILITY_ID
    DeviceID = DEVICE_ID

    def run(self, argv):
        properties = self.communicator().getProperties()
        proxy = self.communicator().stringToProxy(PROXY)

        dt = digitaltwin.dataSinkPrx.checkedCast(proxy)
        if not dt:
            raise RuntimeError("Invalid proxy")

        try:
            if(UPDATE_ACC):
                limits = digitaltwin.DataSetLimits(acc_limits[0], acc_limits[1], acc_limits[2], acc_limits[3], acc_limits[4], acc_limits[5])
                dt.updateDataSetLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Accelerometer, limits)
            if(UPDATE_GY):
                limits = digitaltwin.DataSetLimits(gy_limits[0], gy_limits[1], gy_limits[2], gy_limits[3], gy_limits[4], gy_limits[5])
                dt.updateDataSetLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Gyroscope, limits)
            if(UPDATE_MG):
                limits = digitaltwin.DataSetLimits(mg_limits[0], mg_limits[1], mg_limits[2], mg_limits[3], mg_limits[4], mg_limits[5])
                dt.updateDataSetLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Magnetometer, limits)
            if(UPDATE_TEMP):
                limits = digitaltwin.SingleDataLimits(temp_limits[0], temp_limits[1])
                dt.updateSingleDataLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Temperature, limits)
            if(UPDATE_PRS):
                limits = digitaltwin.SingleDataLimits(prs_limits[0], prs_limits[1])
                dt.updateSingleDataLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Pressure, limits)
            if(UPDATE_HUM):
                limits = digitaltwin.SingleDataLimits(hum_limits[0], hum_limits[1])
                dt.updateSingleDataLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Humidity, limits)
            if(UPDATE_LGT):
                limits = digitaltwin.SingleDataLimits(lgt_limits[0], lgt_limits[1])
                dt.updateSingleDataLimits(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Light, limits)

        except digitaltwin.RegistryNotFound:
            print("Registry not found")
        except digitaltwin.InsertingError:
            print("Error trying to insert the value")


async def main():
    sys.exit(manager().main(sys.argv))

asyncio.run(main())
