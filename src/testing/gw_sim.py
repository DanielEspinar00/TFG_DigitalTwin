import sys
import Ice
import sched
import time
import digitaltwin
import asyncio
import sys

from configparser import ConfigParser

# Config file
config = ConfigParser()

FILE_NAME = 'gw_sim.config'

PROXY = ''
FACILITY_ID = ''
DEVICE_ID = ''

SEND_RATE = 0.01

value = 0.5
step = 0.01
upper_limit = 0.9
lower_limit = 0.1

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

    SEND_RATE = config.getfloat('zeroc_ice','send_rate')

    acc_limits.append(config.getfloat('limits_acc', 'x_max'))
    acc_limits.append(config.getfloat('limits_acc', 'x_min'))
    acc_limits.append(config.getfloat('limits_acc', 'y_max'))
    acc_limits.append(config.getfloat('limits_acc', 'y_min'))
    acc_limits.append(config.getfloat('limits_acc', 'z_max'))
    acc_limits.append(config.getfloat('limits_acc', 'z_min'))

    gy_limits.append(config.getfloat('limits_gy', 'x_max'))
    gy_limits.append(config.getfloat('limits_gy', 'x_min'))
    gy_limits.append(config.getfloat('limits_gy', 'y_max'))
    gy_limits.append(config.getfloat('limits_gy', 'y_min'))
    gy_limits.append(config.getfloat('limits_gy', 'z_max'))
    gy_limits.append(config.getfloat('limits_gy', 'z_min'))

    mg_limits.append(config.getfloat('limits_mg', 'x_max'))
    mg_limits.append(config.getfloat('limits_mg', 'x_min'))
    mg_limits.append(config.getfloat('limits_mg', 'y_max'))
    mg_limits.append(config.getfloat('limits_mg', 'y_min'))
    mg_limits.append(config.getfloat('limits_mg', 'z_max'))
    mg_limits.append(config.getfloat('limits_mg', 'z_min'))

    temp_limits.append(config.getfloat('limits_temp', 'x_max'))
    temp_limits.append(config.getfloat('limits_temp', 'x_min'))

    prs_limits.append(config.getfloat('limits_prs', 'x_max'))
    prs_limits.append(config.getfloat('limits_prs', 'x_min'))

    hum_limits.append(config.getfloat('limits_hum', 'x_max'))
    hum_limits.append(config.getfloat('limits_hum', 'x_min'))

    lgt_limits.append(config.getfloat('limits_lgt', 'x_max'))
    lgt_limits.append(config.getfloat('limits_lgt', 'x_min'))

except:
    print("\nERROR trying to read configuration file '"+FILE_NAME+"'\nExpected:\n" +
          "Section -> zeroc_ice\n\tkey -> 'dt.Server'\n\tkey -> 'FacilityID'\n\tkey -> 'DeviceID'\nSection -> <datatype>\n\tKey -> 'x_max'\n\tkey -> 'x_min'\n\tKey -> 'y_max'\n\tkey -> 'y_min'\n\tKey -> 'z_max'\n\tkey -> 'z_min'\n" +
          "(Decimal symbol: . )")
    exit(-1)


def motor_simulation(dt, FacilityID, DeviceID):    # Simulate sensor reads
    global value, step, upper_limit, lower_limit
    if((value >= upper_limit) or (value <= lower_limit)):
        step = -step

    value = value + step

    try:
        # Accelerometer
        acc_x = acc_limits[1] + (acc_limits[0]-acc_limits[1])*value
        acc_y = acc_limits[3] + (acc_limits[2]-acc_limits[3])*value
        acc_z = acc_limits[5] + (acc_limits[4]-acc_limits[5])*value
        dt.putDataSetReading(FacilityID, DeviceID, digitaltwin.TypeDataSet.Accelerometer, digitaltwin.DataSet(acc_x, acc_y, acc_z))

        # Gyroscope
        gy_x = gy_limits[1] + (gy_limits[0]-gy_limits[1])*value
        gy_y = gy_limits[3] + (gy_limits[2]-gy_limits[3])*value
        gy_z = gy_limits[5] + (gy_limits[4]-gy_limits[5])*value
        dt.putDataSetReading(FacilityID, DeviceID, digitaltwin.TypeDataSet.Gyroscope, digitaltwin.DataSet(gy_x, gy_y, gy_z))

        # # Magnetometer
        mg_x = mg_limits[1] + (mg_limits[0]-mg_limits[1])*value
        mg_y = mg_limits[3] + (mg_limits[2]-mg_limits[3])*value
        mg_z = mg_limits[5] + (mg_limits[4]-mg_limits[5])*value
        dt.putDataSetReading(FacilityID, DeviceID, digitaltwin.TypeDataSet.Magnetometer, digitaltwin.DataSet(mg_x, mg_y, mg_z))

        # Temperature
        t = temp_limits[1] + (temp_limits[0]-temp_limits[1])*value
        dt.putSingleDataReading(FacilityID, DeviceID, digitaltwin.TypeSingleData.Temperature, t)

        # Pressure
        p = prs_limits[1] + (prs_limits[0]-prs_limits[1])*value
        dt.putSingleDataReading(FacilityID, DeviceID, digitaltwin.TypeSingleData.Pressure, p)

        # Humidity
        h = hum_limits[1] + (hum_limits[0]-hum_limits[1])*value
        dt.putSingleDataReading(FacilityID, DeviceID, digitaltwin.TypeSingleData.Humidity, h)

        # Light
        l = lgt_limits[1] + (lgt_limits[0]-lgt_limits[1])*value
        dt.putSingleDataReading(FacilityID, DeviceID, digitaltwin.TypeSingleData.Light, l)

    except digitaltwin.InsertingError:
        print("Error trying to insert the value")

    print(value)


class gw(Ice.Application):
    FacilityID = FACILITY_ID
    DeviceID = DEVICE_ID

    def run(self, argv):
        proxy = self.communicator().stringToProxy(PROXY)

        s = sched.scheduler(time.time, time.sleep)
        dt = digitaltwin.dataSinkPrx.checkedCast(proxy)
        if not dt:
            raise RuntimeError("Invalid proxy")

        # # Valores específicos
        # try:
            # dt.putSingleDataReading(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Temperature, 10)

            # dt.putDataSetReading(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Accelerometer, digitaltwin.DataSet(10, 0.3, -0.4))

            # a = dt.getDataSetDeviation(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Accelerometer, 10)
            # print(a)
            # b = dt.getSingleDataAverage(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Temperature, 10)
            # print(b)

            # a = dt.getDataSetPrediction(self.FacilityID, self.DeviceID, digitaltwin.TypeDataSet.Accelerometer, 10, 4)
            # print(a)
            # b = dt.getSingleDataPrediction(self.FacilityID, self.DeviceID, digitaltwin.TypeSingleData.Temperature, 10, 5)
            # print(b)

        # except digitaltwin.RegistryNotFound:
        #     print("Registry not found")
        # except digitaltwin.InsertingError:
        #     print("Error trying to insert the value")

        while True:
            s.enter(SEND_RATE, 1, motor_simulation,
                    (dt, self.FacilityID, self.DeviceID))
            s.run()


async def main():
    sys.exit(gw().main(sys.argv))

asyncio.run(main())
