module digitaltwin
{

    exception RegistryNotFound {};
    exception InsertingError {};

    enum TypeDataSet {
        Accelerometer,
	    Gyroscope,
	    Magnetometer
	};
    enum TypeSingleData{
        Temperature,
        Pressure,
        Humidity,
        Light
    };

    struct DataSet{
        float x;
        float y;
        float z;
    };
    
    struct SingleDataLimits{
        float maxLimit;
        float minLimit;
    };

    struct DataSetLimits{
        float xMaxLimit;
        float xMinLimit;
        float yMaxLimit;
        float yMinLimit;
        float zMaxLimit;
        float zMinLimit;
    };

    interface dataSink
    {
            // Pull
        DataSet getDataSetReading(string FacilityID, string DeviceID, TypeDataSet dataType) throws RegistryNotFound;
        float getSingleDataReading(string FacilityID, string DeviceID, TypeSingleData dataType) throws RegistryNotFound;
            // Push
        int putDataSetReading(string FacilityID, string DeviceID, TypeDataSet dataType, DataSet data) throws InsertingError;
        int putSingleDataReading(string FacilityID, string DeviceID, TypeSingleData dataType, float data) throws InsertingError;

            // Limits
        DataSetLimits getDataSetLimits(string FacilityID, string DeviceID, TypeDataSet dataType) throws RegistryNotFound;
        SingleDataLimits getSingleDataLimits(string FacilityID, string DeviceID, TypeSingleData dataType) throws RegistryNotFound;

        int updateDataSetLimits(string FacilityID, string DeviceID, TypeDataSet dataType, DataSetLimits limits) throws InsertingError;
        int updateSingleDataLimits(string FacilityID, string DeviceID, TypeSingleData dataType, SingleDataLimits limits) throws InsertingError;


            // Average
        DataSet getDataSetAverage(string FacilityID, string DeviceID, TypeDataSet dataType, int secs) throws RegistryNotFound;
        float getSingleDataAverage(string FacilityID, string DeviceID, TypeSingleData dataType, int secs) throws RegistryNotFound;
        
            // Standard deviation
        DataSet getDataSetDeviation(string FacilityID, string DeviceID, TypeDataSet dataType, int secs) throws RegistryNotFound;
        float getSingleDataDeviation(string FacilityID, string DeviceID, TypeSingleData dataType, int secs) throws RegistryNotFound;

    }
}

// Accelerometer
// Gyroscope
// Magnetometer
//
// Temperature
// Pressure
// Humidity
// Light