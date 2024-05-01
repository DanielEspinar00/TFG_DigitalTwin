import datetime

import logging
import sys, Ice

import digitaltwin
import models
import calculations as calcs

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from configparser import ConfigParser


# Config default values
DB_ADDR = 'postgresql:///tfg_history'
DB_DROP_ALL = False
DB_DROP_READINGS = False
DB_DROP_LIMITS = False

ZICE_ADAP_NAME = 'DigitalTwinAdapter'
ZICE_APAD_ENDPOINT = 'default -p 10000'
ZICE_IDENTITY = 'DigitalTwinServer'

# Config file
config = ConfigParser()

FILE_NAME = 'dt.config'

try:
    config.read(FILE_NAME)

    DB_ADDR = config.get('database', 'address')
    DB_DROP_ALL = config.getboolean('database', 'drop_all')
    DB_DROP_READINGS = config.getboolean('database', 'drop_readings')
    DB_DROP_LIMITS = config.getboolean('database', 'drop_limits')

    ZICE_ADAP_NAME = config.get('zeroc-ice', 'adapter.name')
    ZICE_APAD_ENDPOINT = config.get('zeroc-ice', 'adapter.endpoint')
    ZICE_IDENTITY = config.get('zeroc-ice', 'identity')

except:
    print("\nERROR trying to read configuration file 'dt.config'\nExpected:\n"+
            "Section -> 'database'\n\tKey -> 'address'\n\tkey -> 'drop_all'\n\tkey -> 'drop_readings'\n\tkey -> 'drop_limits'\n"+
            "Section -> 'zeroc-ice'\n\tKey -> 'adapter.name'\n\tkey -> 'adapter.endpoint'\n\tkey -> 'identity'\n")
    exit(-1)

# Database management
engine = create_engine(DB_ADDR)

Session = sessionmaker(engine)
session = Session()

#   ZeroC-Ice server
class dataSinkI(digitaltwin.dataSink):

    # Pull
    def getDataSetReading(self, FacilityID, DeviceID, dataType, current=None):
        logging.info("getDataSetReading ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")
        
        reading = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                    ).filter(models.DataReading.device_id==DeviceID
                                                    ).filter(models.DataReading.data_type==dataType.name
                                                    ).order_by(desc(models.DataReading.timestamp)).first()
        
        if reading:
            return digitaltwin.DataSet(reading.data_x, reading.data_y, reading.data_z)
        else:   # No reading found
            logging.warning("No registry found")
            raise digitaltwin.RegistryNotFound

    def getSingleDataReading(self, FacilityID, DeviceID, dataType, current=None):
        logging.info("getSingleDataReading ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")
        
        reading = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                        ).filter(models.DataReading.device_id==DeviceID
                                                        ).filter(models.DataReading.data_type==dataType.name
                                                        ).order_by(desc(models.DataReading.timestamp)).first()
        
        if reading:
            return reading.data_x
        else:   # No reading found
            logging.warning("No registry found")
            raise digitaltwin.RegistryNotFound

    # Push
    def putDataSetReading(self, FacilityID, DeviceID, dataType, data, current=None):
        logging.info("putDataSetReading ["+FacilityID+", "+DeviceID+", "+dataType.name+", "+ str(data) + "]")

        moment = datetime.datetime.now()
        reading = models.DataReading(facility_id=FacilityID, device_id=DeviceID, timestamp=moment, data_type=dataType.name, data_x=data.x, data_y=data.y, data_z=data.z)
        
        session.add(reading)
        try:
            session.commit()
        except:
            raise digitaltwin.InsertingError

        return 1

    def putSingleDataReading(self, FacilityID, DeviceID, dataType, data, current=None):
        logging.info("putSingleDataReading ["+FacilityID+", "+DeviceID+", "+dataType.name+", "+ str(data) + "]")

        moment = datetime.datetime.now()
        reading = models.DataReading(facility_id=FacilityID, device_id=DeviceID, timestamp=moment, data_type=dataType.name, data_x=data)
        
        session.add(reading)
        try:
            session.commit()
        except:
            raise digitaltwin.InsertingError
    
        return 1
    
    # Limits
    def getDataSetLimits(self, FacilityID, DeviceID, dataType, current=None):
        logging.info("getDataSetLimits ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        reading = session.query(models.Limits).filter(models.Limits.facility_id==FacilityID
                                                    ).filter(models.Limits.device_id==DeviceID
                                                    ).filter(models.Limits.data_type==dataType.name
                                                    ).first()
        
        if reading:
            return digitaltwin.DataSetLimits(reading.x_max, reading.x_min, reading.y_max, reading.y_min, reading.z_max, reading.z_min)
        else:   # No reading found
            logging.warning("No registry found")
            raise digitaltwin.RegistryNotFound
                            
    
    def getSingleDataLimits(self, FacilityID, DeviceID, dataType, current=None):
        logging.info("getSingleDataLimits ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        reading = session.query(models.Limits).filter(models.Limits.facility_id==FacilityID
                                                    ).filter(models.Limits.device_id==DeviceID
                                                    ).filter(models.Limits.data_type==dataType.name
                                                    ).first()
        
        if reading:
            return digitaltwin.SingleDataLimits(reading.x_max, reading.x_min)
        else:   # No reading found
            logging.warning("No registry found")
            raise digitaltwin.RegistryNotFound

    def updateDataSetLimits(self, FacilityID, DeviceID, dataType, limits, current=None):
        logging.info("updateDataSetLimits ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        limit = session.query(models.Limits).filter(models.Limits.facility_id==FacilityID
                                                    ).filter(models.Limits.device_id==DeviceID
                                                    ).filter(models.Limits.data_type==dataType.name
                                                    ).first()
        
        if limit:   # Limit found

            limit.x_max = limits.xMaxLimit
            limit.x_min = limits.xMinLimit
            limit.y_max = limits.yMaxLimit
            limit.y_min = limits.yMinLimit
            limit.z_max = limits.zMaxLimit
            limit.z_min = limits.zMinLimit

            session.add(limit)
            try:
                session.commit()
            except:
                raise digitaltwin.InsertingError
            return 1

        else:   # No limit found

            limit = models.Limits(facility_id=FacilityID, device_id=DeviceID, data_type=dataType.name, x_max=limits.xMaxLimit, x_min = limits.xMinLimit, y_max = limits.yMaxLimit, y_min = limits.yMinLimit, z_max = limits.zMaxLimit, z_min = limits.zMinLimit)
            
            session.add(limit)
            try:
                session.commit()
            except:
                raise digitaltwin.InsertingError
            return 1
    
    def updateSingleDataLimits(self, FacilityID, DeviceID, dataType, limits, current=None):
        logging.info("updateSingleDataLimits ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        limit = session.query(models.Limits).filter(models.Limits.facility_id==FacilityID
                                                    ).filter(models.Limits.device_id==DeviceID
                                                    ).filter(models.Limits.data_type==dataType.name
                                                    ).first()
        
        if limit:   # Limit found

            limit.x_max = limits.maxLimit
            limit.x_min = limits.minLimit

            session.add(limit)
            try:
                session.commit()
            except:
                raise digitaltwin.InsertingError
            return 1

        else:   # No limit found

            limit = models.Limits(facility_id=FacilityID, device_id=DeviceID, data_type=dataType.name, x_max=limits.maxLimit, x_min = limits.minLimit)
            
            session.add(limit)
            try:
                session.commit()
            except:
                raise digitaltwin.InsertingError
            return 1
    
    # Average
    def getDataSetAverage(self, FacilityID, DeviceID, dataType, secs, current=None):
        logging.info("getDataSetAverage ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")
        
        moment = datetime.datetime.now() - datetime.timedelta(seconds=secs)
        readings = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                    ).filter(models.DataReading.device_id==DeviceID
                                                    ).filter(models.DataReading.data_type==dataType.name
                                                    ).filter(models.DataReading.timestamp > moment
                                                    ).order_by(desc(models.DataReading.timestamp))
        n_reads = readings.count() #Number of regisries read

        if n_reads>1:
            
            # Divide values in lists
            list_x = []
            list_y = []
            list_z = []

            for read in readings:
                list_x.append(read.data_x)
                list_y.append(read.data_y)
                list_z.append(read.data_z)
            
            #Calculate average
            averages = digitaltwin.DataSet(calcs.calculateAverage(list_x), calcs.calculateAverage(list_y), calcs.calculateAverage(list_z))

            return averages

        else:   # Not enough entries
            logging.warning("No enough registries")
            raise digitaltwin.RegistryNotFound

    def getSingleDataAverage(self, FacilityID, DeviceID, dataType, secs, current=None):
        logging.info("getSingleDataAverage ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        moment = datetime.datetime.now() - datetime.timedelta(seconds=secs)
        readings = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                        ).filter(models.DataReading.device_id==DeviceID
                                                        ).filter(models.DataReading.data_type==dataType.name
                                                        ).filter(models.DataReading.timestamp > moment
                                                        ).order_by(desc(models.DataReading.timestamp))
        n_reads = readings.count() #Number of regisries read

        if n_reads>1:
            # Calculate average
            list_values = []

            for read in readings:
                list_values.append(read.data_x)

            return calcs.calculateAverage(list_values)

        else:   # Not enough entries
            logging.warning("No enough registries")
            raise digitaltwin.RegistryNotFound

    # Standard deviation
    def getDataSetDeviation(self, FacilityID, DeviceID, dataType, secs, current=None):
        logging.info("getDataSetDeviation ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        moment = datetime.datetime.now() - datetime.timedelta(seconds=secs)
        readings = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                    ).filter(models.DataReading.device_id==DeviceID
                                                    ).filter(models.DataReading.data_type==dataType.name
                                                    ).filter(models.DataReading.timestamp > moment
                                                    ).order_by(desc(models.DataReading.timestamp))
        n_reads = readings.count() #Number of regisries read

        if n_reads>1:
            # Divide values in lists
            list_x = []
            list_y = []
            list_z = []

            for read in readings:
                list_x.append(read.data_x)
                list_y.append(read.data_y)
                list_z.append(read.data_z)
            
            # Calculate standard deviations
            deviations = digitaltwin.DataSet(calcs.calculateDeviation(list_x), calcs.calculateDeviation(list_y), calcs.calculateDeviation(list_z))

            return deviations

        else:   # Not enough entries
            logging.warning("No enough registries")
            raise digitaltwin.RegistryNotFound

    def getSingleDataDeviation(self, FacilityID, DeviceID, dataType, secs, current=None):
        logging.info("getSingleDataDeviation ["+FacilityID+", "+DeviceID+", "+dataType.name+"]")

        moment = datetime.datetime.now() - datetime.timedelta(seconds=secs)
        readings = session.query(models.DataReading).filter(models.DataReading.facility_id==FacilityID
                                                        ).filter(models.DataReading.device_id==DeviceID
                                                        ).filter(models.DataReading.data_type==dataType.name
                                                        ).filter(models.DataReading.timestamp > moment
                                                        ).order_by(desc(models.DataReading.timestamp)) 
        n_reads = readings.count() #Number of regisries read

        if n_reads>1:

            list_values = []

            for read in readings:
                list_values.append(read.data_x)

            # Calculate standard deviations
            return calcs.calculateDeviation(list_values)
            
        else:   # Not enough entries
            logging.warning("No enough registries")
            raise digitaltwin.RegistryNotFound
    

if __name__ == '__main__':

    # try:
    #     if(DB_DROP_ALL):
    #         models.dropAll(engine)
    #     else:
    #         if(DB_DROP_READINGS):
    #             models.drop(engine, models.DataReading.__table__)
    #         if(DB_DROP_LIMITS):
    #             models.drop(engine, models.Limits.__table__)

    #     models.createAll(engine)
    # except:
    #     print('ERROR - Error intentando conectar con la base de datos')
    #     exit(0)
    
    if(DB_DROP_ALL):
            models.dropAll(engine)
    else:
        if(DB_DROP_READINGS):
            models.drop(engine, models.DataReading.__table__)
        if(DB_DROP_LIMITS):
            models.drop(engine, models.Limits.__table__)

    models.createAll(engine)

    with Ice.initialize(sys.argv) as communicator:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        object = dataSinkI()
    
        adapter = communicator.createObjectAdapterWithEndpoints(ZICE_ADAP_NAME, ZICE_APAD_ENDPOINT)
        proxy = adapter.add(object, communicator.stringToIdentity(ZICE_IDENTITY))
        print(proxy)
        adapter.activate()
        communicator.waitForShutdown()
