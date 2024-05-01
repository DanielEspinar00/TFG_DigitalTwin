# -*- coding: utf-8 -*-
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#
#
# Ice version 3.7.3
#
# <auto-generated>
#
# Generated from file `dt.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module digitaltwin
_M_digitaltwin = Ice.openModule('digitaltwin')
__name__ = 'digitaltwin'

if 'RegistryNotFound' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.RegistryNotFound = Ice.createTempClass()
    class RegistryNotFound(Ice.UserException):
        def __init__(self):
            pass

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

        _ice_id = '::digitaltwin::RegistryNotFound'

    _M_digitaltwin._t_RegistryNotFound = IcePy.defineException('::digitaltwin::RegistryNotFound', RegistryNotFound, (), False, None, ())
    RegistryNotFound._ice_type = _M_digitaltwin._t_RegistryNotFound

    _M_digitaltwin.RegistryNotFound = RegistryNotFound
    del RegistryNotFound

if 'InsertingError' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.InsertingError = Ice.createTempClass()
    class InsertingError(Ice.UserException):
        def __init__(self):
            pass

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

        _ice_id = '::digitaltwin::InsertingError'

    _M_digitaltwin._t_InsertingError = IcePy.defineException('::digitaltwin::InsertingError', InsertingError, (), False, None, ())
    InsertingError._ice_type = _M_digitaltwin._t_InsertingError

    _M_digitaltwin.InsertingError = InsertingError
    del InsertingError

if 'TypeDataSet' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.TypeDataSet = Ice.createTempClass()
    class TypeDataSet(Ice.EnumBase):

        def __init__(self, _n, _v):
            Ice.EnumBase.__init__(self, _n, _v)

        def valueOf(self, _n):
            if _n in self._enumerators:
                return self._enumerators[_n]
            return None
        valueOf = classmethod(valueOf)

    TypeDataSet.Accelerometer = TypeDataSet("Accelerometer", 0)
    TypeDataSet.Gyroscope = TypeDataSet("Gyroscope", 1)
    TypeDataSet.Magnetometer = TypeDataSet("Magnetometer", 2)
    TypeDataSet._enumerators = { 0:TypeDataSet.Accelerometer, 1:TypeDataSet.Gyroscope, 2:TypeDataSet.Magnetometer }

    _M_digitaltwin._t_TypeDataSet = IcePy.defineEnum('::digitaltwin::TypeDataSet', TypeDataSet, (), TypeDataSet._enumerators)

    _M_digitaltwin.TypeDataSet = TypeDataSet
    del TypeDataSet

if 'TypeSingleData' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.TypeSingleData = Ice.createTempClass()
    class TypeSingleData(Ice.EnumBase):

        def __init__(self, _n, _v):
            Ice.EnumBase.__init__(self, _n, _v)

        def valueOf(self, _n):
            if _n in self._enumerators:
                return self._enumerators[_n]
            return None
        valueOf = classmethod(valueOf)

    TypeSingleData.Temperature = TypeSingleData("Temperature", 0)
    TypeSingleData.Pressure = TypeSingleData("Pressure", 1)
    TypeSingleData.Humidity = TypeSingleData("Humidity", 2)
    TypeSingleData.Light = TypeSingleData("Light", 3)
    TypeSingleData._enumerators = { 0:TypeSingleData.Temperature, 1:TypeSingleData.Pressure, 2:TypeSingleData.Humidity, 3:TypeSingleData.Light }

    _M_digitaltwin._t_TypeSingleData = IcePy.defineEnum('::digitaltwin::TypeSingleData', TypeSingleData, (), TypeSingleData._enumerators)

    _M_digitaltwin.TypeSingleData = TypeSingleData
    del TypeSingleData

if 'DataSet' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.DataSet = Ice.createTempClass()
    class DataSet(object):
        def __init__(self, x=0.0, y=0.0, z=0.0):
            self.x = x
            self.y = y
            self.z = z

        def __eq__(self, other):
            if other is None:
                return False
            elif not isinstance(other, _M_digitaltwin.DataSet):
                return NotImplemented
            else:
                if self.x != other.x:
                    return False
                if self.y != other.y:
                    return False
                if self.z != other.z:
                    return False
                return True

        def __ne__(self, other):
            return not self.__eq__(other)

        def __str__(self):
            return IcePy.stringify(self, _M_digitaltwin._t_DataSet)

        __repr__ = __str__

    _M_digitaltwin._t_DataSet = IcePy.defineStruct('::digitaltwin::DataSet', DataSet, (), (
        ('x', (), IcePy._t_float),
        ('y', (), IcePy._t_float),
        ('z', (), IcePy._t_float)
    ))

    _M_digitaltwin.DataSet = DataSet
    del DataSet

if 'SingleDataLimits' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.SingleDataLimits = Ice.createTempClass()
    class SingleDataLimits(object):
        def __init__(self, maxLimit=0.0, minLimit=0.0):
            self.maxLimit = maxLimit
            self.minLimit = minLimit

        def __eq__(self, other):
            if other is None:
                return False
            elif not isinstance(other, _M_digitaltwin.SingleDataLimits):
                return NotImplemented
            else:
                if self.maxLimit != other.maxLimit:
                    return False
                if self.minLimit != other.minLimit:
                    return False
                return True

        def __ne__(self, other):
            return not self.__eq__(other)

        def __str__(self):
            return IcePy.stringify(self, _M_digitaltwin._t_SingleDataLimits)

        __repr__ = __str__

    _M_digitaltwin._t_SingleDataLimits = IcePy.defineStruct('::digitaltwin::SingleDataLimits', SingleDataLimits, (), (
        ('maxLimit', (), IcePy._t_float),
        ('minLimit', (), IcePy._t_float)
    ))

    _M_digitaltwin.SingleDataLimits = SingleDataLimits
    del SingleDataLimits

if 'DataSetLimits' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.DataSetLimits = Ice.createTempClass()
    class DataSetLimits(object):
        def __init__(self, xMaxLimit=0.0, xMinLimit=0.0, yMaxLimit=0.0, yMinLimit=0.0, zMaxLimit=0.0, zMinLimit=0.0):
            self.xMaxLimit = xMaxLimit
            self.xMinLimit = xMinLimit
            self.yMaxLimit = yMaxLimit
            self.yMinLimit = yMinLimit
            self.zMaxLimit = zMaxLimit
            self.zMinLimit = zMinLimit

        def __eq__(self, other):
            if other is None:
                return False
            elif not isinstance(other, _M_digitaltwin.DataSetLimits):
                return NotImplemented
            else:
                if self.xMaxLimit != other.xMaxLimit:
                    return False
                if self.xMinLimit != other.xMinLimit:
                    return False
                if self.yMaxLimit != other.yMaxLimit:
                    return False
                if self.yMinLimit != other.yMinLimit:
                    return False
                if self.zMaxLimit != other.zMaxLimit:
                    return False
                if self.zMinLimit != other.zMinLimit:
                    return False
                return True

        def __ne__(self, other):
            return not self.__eq__(other)

        def __str__(self):
            return IcePy.stringify(self, _M_digitaltwin._t_DataSetLimits)

        __repr__ = __str__

    _M_digitaltwin._t_DataSetLimits = IcePy.defineStruct('::digitaltwin::DataSetLimits', DataSetLimits, (), (
        ('xMaxLimit', (), IcePy._t_float),
        ('xMinLimit', (), IcePy._t_float),
        ('yMaxLimit', (), IcePy._t_float),
        ('yMinLimit', (), IcePy._t_float),
        ('zMaxLimit', (), IcePy._t_float),
        ('zMinLimit', (), IcePy._t_float)
    ))

    _M_digitaltwin.DataSetLimits = DataSetLimits
    del DataSetLimits

_M_digitaltwin._t_dataSink = IcePy.defineValue('::digitaltwin::dataSink', Ice.Value, -1, (), False, True, None, ())

if 'dataSinkPrx' not in _M_digitaltwin.__dict__:
    _M_digitaltwin.dataSinkPrx = Ice.createTempClass()
    class dataSinkPrx(Ice.ObjectPrx):

        def getDataSetReading(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetReading.invoke(self, ((FacilityID, DeviceID, dataType), context))

        def getDataSetReadingAsync(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetReading.invokeAsync(self, ((FacilityID, DeviceID, dataType), context))

        def begin_getDataSetReading(self, FacilityID, DeviceID, dataType, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetReading.begin(self, ((FacilityID, DeviceID, dataType), _response, _ex, _sent, context))

        def end_getDataSetReading(self, _r):
            return _M_digitaltwin.dataSink._op_getDataSetReading.end(self, _r)

        def getSingleDataReading(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataReading.invoke(self, ((FacilityID, DeviceID, dataType), context))

        def getSingleDataReadingAsync(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataReading.invokeAsync(self, ((FacilityID, DeviceID, dataType), context))

        def begin_getSingleDataReading(self, FacilityID, DeviceID, dataType, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataReading.begin(self, ((FacilityID, DeviceID, dataType), _response, _ex, _sent, context))

        def end_getSingleDataReading(self, _r):
            return _M_digitaltwin.dataSink._op_getSingleDataReading.end(self, _r)

        def putDataSetReading(self, FacilityID, DeviceID, dataType, data, context=None):
            return _M_digitaltwin.dataSink._op_putDataSetReading.invoke(self, ((FacilityID, DeviceID, dataType, data), context))

        def putDataSetReadingAsync(self, FacilityID, DeviceID, dataType, data, context=None):
            return _M_digitaltwin.dataSink._op_putDataSetReading.invokeAsync(self, ((FacilityID, DeviceID, dataType, data), context))

        def begin_putDataSetReading(self, FacilityID, DeviceID, dataType, data, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_putDataSetReading.begin(self, ((FacilityID, DeviceID, dataType, data), _response, _ex, _sent, context))

        def end_putDataSetReading(self, _r):
            return _M_digitaltwin.dataSink._op_putDataSetReading.end(self, _r)

        def putSingleDataReading(self, FacilityID, DeviceID, dataType, data, context=None):
            return _M_digitaltwin.dataSink._op_putSingleDataReading.invoke(self, ((FacilityID, DeviceID, dataType, data), context))

        def putSingleDataReadingAsync(self, FacilityID, DeviceID, dataType, data, context=None):
            return _M_digitaltwin.dataSink._op_putSingleDataReading.invokeAsync(self, ((FacilityID, DeviceID, dataType, data), context))

        def begin_putSingleDataReading(self, FacilityID, DeviceID, dataType, data, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_putSingleDataReading.begin(self, ((FacilityID, DeviceID, dataType, data), _response, _ex, _sent, context))

        def end_putSingleDataReading(self, _r):
            return _M_digitaltwin.dataSink._op_putSingleDataReading.end(self, _r)

        def getDataSetLimits(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetLimits.invoke(self, ((FacilityID, DeviceID, dataType), context))

        def getDataSetLimitsAsync(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetLimits.invokeAsync(self, ((FacilityID, DeviceID, dataType), context))

        def begin_getDataSetLimits(self, FacilityID, DeviceID, dataType, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetLimits.begin(self, ((FacilityID, DeviceID, dataType), _response, _ex, _sent, context))

        def end_getDataSetLimits(self, _r):
            return _M_digitaltwin.dataSink._op_getDataSetLimits.end(self, _r)

        def getSingleDataLimits(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataLimits.invoke(self, ((FacilityID, DeviceID, dataType), context))

        def getSingleDataLimitsAsync(self, FacilityID, DeviceID, dataType, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataLimits.invokeAsync(self, ((FacilityID, DeviceID, dataType), context))

        def begin_getSingleDataLimits(self, FacilityID, DeviceID, dataType, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataLimits.begin(self, ((FacilityID, DeviceID, dataType), _response, _ex, _sent, context))

        def end_getSingleDataLimits(self, _r):
            return _M_digitaltwin.dataSink._op_getSingleDataLimits.end(self, _r)

        def updateDataSetLimits(self, FacilityID, DeviceID, dataType, limits, context=None):
            return _M_digitaltwin.dataSink._op_updateDataSetLimits.invoke(self, ((FacilityID, DeviceID, dataType, limits), context))

        def updateDataSetLimitsAsync(self, FacilityID, DeviceID, dataType, limits, context=None):
            return _M_digitaltwin.dataSink._op_updateDataSetLimits.invokeAsync(self, ((FacilityID, DeviceID, dataType, limits), context))

        def begin_updateDataSetLimits(self, FacilityID, DeviceID, dataType, limits, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_updateDataSetLimits.begin(self, ((FacilityID, DeviceID, dataType, limits), _response, _ex, _sent, context))

        def end_updateDataSetLimits(self, _r):
            return _M_digitaltwin.dataSink._op_updateDataSetLimits.end(self, _r)

        def updateSingleDataLimits(self, FacilityID, DeviceID, dataType, limits, context=None):
            return _M_digitaltwin.dataSink._op_updateSingleDataLimits.invoke(self, ((FacilityID, DeviceID, dataType, limits), context))

        def updateSingleDataLimitsAsync(self, FacilityID, DeviceID, dataType, limits, context=None):
            return _M_digitaltwin.dataSink._op_updateSingleDataLimits.invokeAsync(self, ((FacilityID, DeviceID, dataType, limits), context))

        def begin_updateSingleDataLimits(self, FacilityID, DeviceID, dataType, limits, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_updateSingleDataLimits.begin(self, ((FacilityID, DeviceID, dataType, limits), _response, _ex, _sent, context))

        def end_updateSingleDataLimits(self, _r):
            return _M_digitaltwin.dataSink._op_updateSingleDataLimits.end(self, _r)

        def getDataSetAverage(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetAverage.invoke(self, ((FacilityID, DeviceID, dataType, secs), context))

        def getDataSetAverageAsync(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetAverage.invokeAsync(self, ((FacilityID, DeviceID, dataType, secs), context))

        def begin_getDataSetAverage(self, FacilityID, DeviceID, dataType, secs, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetAverage.begin(self, ((FacilityID, DeviceID, dataType, secs), _response, _ex, _sent, context))

        def end_getDataSetAverage(self, _r):
            return _M_digitaltwin.dataSink._op_getDataSetAverage.end(self, _r)

        def getSingleDataAverage(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataAverage.invoke(self, ((FacilityID, DeviceID, dataType, secs), context))

        def getSingleDataAverageAsync(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataAverage.invokeAsync(self, ((FacilityID, DeviceID, dataType, secs), context))

        def begin_getSingleDataAverage(self, FacilityID, DeviceID, dataType, secs, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataAverage.begin(self, ((FacilityID, DeviceID, dataType, secs), _response, _ex, _sent, context))

        def end_getSingleDataAverage(self, _r):
            return _M_digitaltwin.dataSink._op_getSingleDataAverage.end(self, _r)

        def getDataSetDeviation(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetDeviation.invoke(self, ((FacilityID, DeviceID, dataType, secs), context))

        def getDataSetDeviationAsync(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetDeviation.invokeAsync(self, ((FacilityID, DeviceID, dataType, secs), context))

        def begin_getDataSetDeviation(self, FacilityID, DeviceID, dataType, secs, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getDataSetDeviation.begin(self, ((FacilityID, DeviceID, dataType, secs), _response, _ex, _sent, context))

        def end_getDataSetDeviation(self, _r):
            return _M_digitaltwin.dataSink._op_getDataSetDeviation.end(self, _r)

        def getSingleDataDeviation(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataDeviation.invoke(self, ((FacilityID, DeviceID, dataType, secs), context))

        def getSingleDataDeviationAsync(self, FacilityID, DeviceID, dataType, secs, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataDeviation.invokeAsync(self, ((FacilityID, DeviceID, dataType, secs), context))

        def begin_getSingleDataDeviation(self, FacilityID, DeviceID, dataType, secs, _response=None, _ex=None, _sent=None, context=None):
            return _M_digitaltwin.dataSink._op_getSingleDataDeviation.begin(self, ((FacilityID, DeviceID, dataType, secs), _response, _ex, _sent, context))

        def end_getSingleDataDeviation(self, _r):
            return _M_digitaltwin.dataSink._op_getSingleDataDeviation.end(self, _r)

        @staticmethod
        def checkedCast(proxy, facetOrContext=None, context=None):
            return _M_digitaltwin.dataSinkPrx.ice_checkedCast(proxy, '::digitaltwin::dataSink', facetOrContext, context)

        @staticmethod
        def uncheckedCast(proxy, facet=None):
            return _M_digitaltwin.dataSinkPrx.ice_uncheckedCast(proxy, facet)

        @staticmethod
        def ice_staticId():
            return '::digitaltwin::dataSink'
    _M_digitaltwin._t_dataSinkPrx = IcePy.defineProxy('::digitaltwin::dataSink', dataSinkPrx)

    _M_digitaltwin.dataSinkPrx = dataSinkPrx
    del dataSinkPrx

    _M_digitaltwin.dataSink = Ice.createTempClass()
    class dataSink(Ice.Object):

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::digitaltwin::dataSink')

        def ice_id(self, current=None):
            return '::digitaltwin::dataSink'

        @staticmethod
        def ice_staticId():
            return '::digitaltwin::dataSink'

        def getDataSetReading(self, FacilityID, DeviceID, dataType, current=None):
            raise NotImplementedError("servant method 'getDataSetReading' not implemented")

        def getSingleDataReading(self, FacilityID, DeviceID, dataType, current=None):
            raise NotImplementedError("servant method 'getSingleDataReading' not implemented")

        def putDataSetReading(self, FacilityID, DeviceID, dataType, data, current=None):
            raise NotImplementedError("servant method 'putDataSetReading' not implemented")

        def putSingleDataReading(self, FacilityID, DeviceID, dataType, data, current=None):
            raise NotImplementedError("servant method 'putSingleDataReading' not implemented")

        def getDataSetLimits(self, FacilityID, DeviceID, dataType, current=None):
            raise NotImplementedError("servant method 'getDataSetLimits' not implemented")

        def getSingleDataLimits(self, FacilityID, DeviceID, dataType, current=None):
            raise NotImplementedError("servant method 'getSingleDataLimits' not implemented")

        def updateDataSetLimits(self, FacilityID, DeviceID, dataType, limits, current=None):
            raise NotImplementedError("servant method 'updateDataSetLimits' not implemented")

        def updateSingleDataLimits(self, FacilityID, DeviceID, dataType, limits, current=None):
            raise NotImplementedError("servant method 'updateSingleDataLimits' not implemented")

        def getDataSetAverage(self, FacilityID, DeviceID, dataType, secs, current=None):
            raise NotImplementedError("servant method 'getDataSetAverage' not implemented")

        def getSingleDataAverage(self, FacilityID, DeviceID, dataType, secs, current=None):
            raise NotImplementedError("servant method 'getSingleDataAverage' not implemented")

        def getDataSetDeviation(self, FacilityID, DeviceID, dataType, secs, current=None):
            raise NotImplementedError("servant method 'getDataSetDeviation' not implemented")

        def getSingleDataDeviation(self, FacilityID, DeviceID, dataType, secs, current=None):
            raise NotImplementedError("servant method 'getSingleDataDeviation' not implemented")

        def __str__(self):
            return IcePy.stringify(self, _M_digitaltwin._t_dataSinkDisp)

        __repr__ = __str__

    _M_digitaltwin._t_dataSinkDisp = IcePy.defineClass('::digitaltwin::dataSink', dataSink, (), None, ())
    dataSink._ice_type = _M_digitaltwin._t_dataSinkDisp

    dataSink._op_getDataSetReading = IcePy.Operation('getDataSetReading', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0)), (), ((), _M_digitaltwin._t_DataSet, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_getSingleDataReading = IcePy.Operation('getSingleDataReading', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0)), (), ((), IcePy._t_float, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_putDataSetReading = IcePy.Operation('putDataSetReading', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0), ((), _M_digitaltwin._t_DataSet, False, 0)), (), ((), IcePy._t_int, False, 0), (_M_digitaltwin._t_InsertingError,))
    dataSink._op_putSingleDataReading = IcePy.Operation('putSingleDataReading', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0), ((), IcePy._t_float, False, 0)), (), ((), IcePy._t_int, False, 0), (_M_digitaltwin._t_InsertingError,))
    dataSink._op_getDataSetLimits = IcePy.Operation('getDataSetLimits', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0)), (), ((), _M_digitaltwin._t_DataSetLimits, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_getSingleDataLimits = IcePy.Operation('getSingleDataLimits', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0)), (), ((), _M_digitaltwin._t_SingleDataLimits, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_updateDataSetLimits = IcePy.Operation('updateDataSetLimits', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0), ((), _M_digitaltwin._t_DataSetLimits, False, 0)), (), ((), IcePy._t_int, False, 0), (_M_digitaltwin._t_InsertingError,))
    dataSink._op_updateSingleDataLimits = IcePy.Operation('updateSingleDataLimits', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0), ((), _M_digitaltwin._t_SingleDataLimits, False, 0)), (), ((), IcePy._t_int, False, 0), (_M_digitaltwin._t_InsertingError,))
    dataSink._op_getDataSetAverage = IcePy.Operation('getDataSetAverage', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0), ((), IcePy._t_int, False, 0)), (), ((), _M_digitaltwin._t_DataSet, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_getSingleDataAverage = IcePy.Operation('getSingleDataAverage', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0), ((), IcePy._t_int, False, 0)), (), ((), IcePy._t_float, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_getDataSetDeviation = IcePy.Operation('getDataSetDeviation', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeDataSet, False, 0), ((), IcePy._t_int, False, 0)), (), ((), _M_digitaltwin._t_DataSet, False, 0), (_M_digitaltwin._t_RegistryNotFound,))
    dataSink._op_getSingleDataDeviation = IcePy.Operation('getSingleDataDeviation', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _M_digitaltwin._t_TypeSingleData, False, 0), ((), IcePy._t_int, False, 0)), (), ((), IcePy._t_float, False, 0), (_M_digitaltwin._t_RegistryNotFound,))

    _M_digitaltwin.dataSink = dataSink
    del dataSink

# End of module digitaltwin
