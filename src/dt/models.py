from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, DateTime, String

Base = declarative_base()

class DataReading(Base):
    # Table name
    __tablename__ = 'Readings'

    # Attributes
    facility_id = Column(String(50), primary_key=True)
    device_id = Column(String(50), primary_key=True)
    timestamp = Column(DateTime(), primary_key=True , default=datetime.now())
    data_type = Column(String(20), primary_key=True)
    data_x = Column(Float(), nullable=False)
    data_y = Column(Float(), nullable=True, default=None)
    data_z = Column(Float(), nullable=True, default=None)

    def __str__(self):
        return self.facility_id + ", " + self.device_id + ", " + str(self.timestamp) + ", " + self.data_type + ", [" + str(self.data_x) + ", " + str(self.data_y) + ", " + str(self.data_z) + "]"

class Limits(Base):
    # Table name
    __tablename__ = 'Limits'

    # Attributes
    facility_id = Column(String(50), primary_key=True)
    device_id = Column(String(50), primary_key=True)
    data_type = Column(String(20), primary_key=True)
    x_max = Column(Float(), nullable=False)
    x_min = Column(Float(), nullable=False)
    y_max = Column(Float(), nullable=True, default=None)
    y_min = Column(Float(), nullable=True, default=None)
    z_max = Column(Float(), nullable=True, default=None)
    z_min = Column(Float(), nullable=True, default=None)

    def __str__(self):
        return self.facility_id + ", " + self.device_id + ", " + str(self.timestamp) + ", " + self.data_type + ", [" + str(self.data_x) + ", " + str(self.data_y) + ", " + str(self.data_z) + "]"

def dropAll(engine):
    Base.metadata.drop_all(engine)

def drop(engine, table):
    Base.metadata.drop_all(engine, tables=[table])

def createAll(engine):
    Base.metadata.create_all(engine)

