using System;
using System.Collections;
using System.Collections.Generic;
using digitaltwin;
using UnityEngine;

public class dt_client : MonoBehaviour
{
    private MotorGraphic motorGraphicInfo;

    // ZeroC Ice
    [SerializeField] string proxyString = "DigitalTwinServer:default -p 10000";
    static Ice.Communicator communicator;
    private IEnumerator coroutineAcc, coroutineGy, coroutineMg, coroutineTemp, coroutinePrs, coroutineHum, coroutineLgt;
    public Ice.ObjectPrx obj;
    public dataSinkPrx washmachine;

    // Motor information
    [Header("Motor information")]
    [SerializeField] string facilityID = "Facility1";
    [SerializeField] string deviceID = "TestDevice1";

    [Header("Accelerometer")]
    [SerializeField] bool syncAccelerometer = true;
    [SerializeField] float updateTimeAccelerometer = 0.1f;
    [Header("Gyroscope")]
    [SerializeField] bool syncGyroscope = true;
    [SerializeField] float updateTimeGyroscope = 0.1f;
    [Header("Magnetometer")]
    [SerializeField] bool syncMagnetometer = true;
    [SerializeField] float updateTimeMagnetometer = 0.1f;
    [Header("Temperature")]
    [SerializeField] bool syncTemperature = true;
    [SerializeField] float updateTimeTemperature = 0.5f;
    [Header("Pressure")]
    [SerializeField] bool syncPressure = true;
    [SerializeField] float updateTimePressure = 0.5f;
    [Header("Humidity")]
    [SerializeField] bool syncHumidity = true;
    [SerializeField] float updateTimeHumidity = 0.5f;
    [Header("Light")]
    [SerializeField] bool syncLight = true;
    [SerializeField] float updateTimeLight = 0.5f;

    // Data
    [NonSerialized]
    private DataSet Acc = new DataSet(0, 0, 0), Gy = new DataSet(0, 0, 0), Mg = new DataSet(0, 0, 0);
    [NonSerialized]
    private float Temp = 0.0f, Prss = 0.0f, Hum = 0.0f, Lg = 0.0f;

    // Limits
    private DataSetLimits Acc_limits = new DataSetLimits(1, -1, 1, -1, 1, -1), Gy_limits = new DataSetLimits(1, -1, 1, -1, 1, -1), Mg_limits = new DataSetLimits(1, -1, 1, -1, 1, -1);
    private SingleDataLimits Temp_limits = new SingleDataLimits(1, -1), Prs_limits = new SingleDataLimits(1, -1), Hum_limits = new SingleDataLimits(1, -1), Lgt_limits = new SingleDataLimits(1, -1);

    // Averages
    private DataSet Acc_average = new DataSet(0, 0, 0), Gy_average = new DataSet(0, 0, 0), Mg_average = new DataSet(0, 0, 0);
    private float Temp_average = 0.0f, Prss_average = 0.0f, Hum_average = 0.0f, Lg_average = 0.0f;

    // Deviations
    private DataSet Acc_deviation = new DataSet(0, 0, 0), Gy_deviation = new DataSet(0, 0, 0), Mg_deviation = new DataSet(0, 0, 0);
    private float Temp_deviation = 0.0f, Prss_deviation = 0.0f, Hum_deviation = 0.0f, Lg_deviation = 0.0f;

    // Motor state aux
    [HideInInspector]
    public bool isConnected = false;

    private void startSync(string datatype)
    {
        try
        {
            switch (datatype)
            {
                case "Accelerometer":
                    try{
                        this.Acc_limits = this.washmachine.getDataSetLimits(this.facilityID, this.deviceID, TypeDataSet.Accelerometer);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineAcc = doSync(datatype);
                    StartCoroutine(coroutineAcc);

                    break;

                case "Gyroscope":
                    try{
                        this.Gy_limits = this.washmachine.getDataSetLimits(this.facilityID, this.deviceID, TypeDataSet.Gyroscope);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineGy = doSync(datatype);
                    StartCoroutine(coroutineGy);

                    break;

                case "Magnetometer":
                    try{
                        this.Mg_limits = this.washmachine.getDataSetLimits(this.facilityID, this.deviceID, TypeDataSet.Magnetometer);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineMg = doSync(datatype);
                    StartCoroutine(coroutineMg);

                    break;

                case "Temperature":
                    try{
                        this.Temp_limits = this.washmachine.getSingleDataLimits(this.facilityID, this.deviceID, TypeSingleData.Temperature);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineTemp = doSync(datatype);
                    StartCoroutine(coroutineTemp);

                    break;

                case "Pressure":
                    try{
                        this.Prs_limits = this.washmachine.getSingleDataLimits(this.facilityID, this.deviceID, TypeSingleData.Pressure);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutinePrs = doSync(datatype);
                    StartCoroutine(coroutinePrs);

                    break;

                case "Humidity":
                    try{
                        this.Hum_limits = this.washmachine.getSingleDataLimits(this.facilityID, this.deviceID, TypeSingleData.Humidity);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineHum = doSync(datatype);
                    StartCoroutine(coroutineHum);

                    break;

                case "Light":
                    try{
                        this.Lgt_limits = this.washmachine.getSingleDataLimits(this.facilityID, this.deviceID, TypeSingleData.Light);
                    }catch (RegistryNotFound){
                        Debug.LogWarning("Registry not found for Limits [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                    }

                    motorGraphicInfo.UpdateLimits(datatype); //Update graphic limits

                    coroutineLgt = doSync(datatype);
                    StartCoroutine(coroutineLgt);

                    break;

                default:
                    Debug.Log("Updating server's connection state");
                    break;
            }

        }
        catch
        {
            Debug.LogError("Connection Lost!");
            isConnected = false;
        }
    }
    IEnumerator doSync(string datatype)
    {
        float updateTime = 0;
        Debug.Log("doSync:Corrutine --> " + datatype);
        for (; ; ){
            try{
                try{
                    switch (datatype){
                        case "Accelerometer":

                            updateTime = updateTimeAccelerometer;
                            this.Acc = this.washmachine.getDataSetReading(this.facilityID, this.deviceID, TypeDataSet.Accelerometer);
                            break;

                        case "Gyroscope":
                            updateTime = updateTimeGyroscope;
                            this.Gy = this.washmachine.getDataSetReading(this.facilityID, this.deviceID, TypeDataSet.Gyroscope);
                            break;
                        case "Magnetometer":
                            updateTime = updateTimeMagnetometer;
                            this.Mg = this.washmachine.getDataSetReading(this.facilityID, this.deviceID, TypeDataSet.Magnetometer);
                            break;
                        case "Temperature":

                            updateTime = updateTimeTemperature;
                            this.Temp = this.washmachine.getSingleDataReading(this.facilityID, this.deviceID, TypeSingleData.Temperature);
                            break;

                        case "Pressure":

                            updateTime = updateTimePressure;
                            this.Prss = this.washmachine.getSingleDataReading(this.facilityID, this.deviceID, TypeSingleData.Pressure);
                            break;
                        
                        case "Humidity":
                            
                            updateTime = updateTimeHumidity;
                            this.Hum = this.washmachine.getSingleDataReading(this.facilityID, this.deviceID, TypeSingleData.Humidity);
                            break;

                        case "Light":
                            
                            updateTime = updateTimeLight;
                            this.Lg = this.washmachine.getSingleDataReading(this.facilityID, this.deviceID, TypeSingleData.Light);
                            break;

                        default:
                            break;
                    }
                    motorGraphicInfo.UpdateMotorInformation(datatype); //Update information

                }catch (RegistryNotFound){
                    Debug.LogWarning("Registry not found for [" + this.facilityID + ", " + this.deviceID + ", " + datatype + "]");
                }

            }catch{
                Debug.LogError("Connection Lost!");
                isConnected = false;
                motorGraphicInfo.UpdateMotorInformation(""); // Update conection state
                StopAllCoroutines();
            }

            yield return new WaitForSeconds(updateTime);
        }
    }
    // Start is called before the first frame update
    void Start()
    {
        motorGraphicInfo = GetComponent<MotorGraphic>();
        Connect();
    }

    // Update is called once per frame
    void Update()
    {
    }

    public void Connect()
    {
        Debug.Log("Linking motor (" + gameObject.name + ")");
        dt_client.communicator = Ice.Util.initialize();

        if (dt_client.communicator == null)
        {
            Debug.LogError("Fail!, getting communicator!");
        }
        else
        {
            this.obj = communicator.stringToProxy(proxyString);
            try
            {
                this.washmachine = dataSinkPrxHelper.checkedCast(this.obj);
                isConnected = true;

                if(syncAccelerometer)   this.startSync(TypeDataSet.Accelerometer.ToString());
                if(syncGyroscope)       this.startSync(TypeDataSet.Gyroscope.ToString());
                if(syncMagnetometer)    this.startSync(TypeDataSet.Magnetometer.ToString());
                if(syncTemperature)     this.startSync(TypeSingleData.Temperature.ToString());
                if(syncPressure)        this.startSync(TypeSingleData.Pressure.ToString());
                if(syncHumidity)        this.startSync(TypeSingleData.Humidity.ToString());
                if(syncLight)           this.startSync(TypeSingleData.Light.ToString());
            }
            catch
            {
                Debug.LogError("Error while getting washmachine Prx\n");
                isConnected = false;
            }
        }
        motorGraphicInfo.UpdateMotorInformation(""); // Update conection state
    }

    public void Refresh()
    {
        try
        {
            StopAllCoroutines();
        }
        catch { }
        Connect();
    }

    // Getters & Setters
    public string getFacilityID()
    {
        return this.facilityID;
    }
    public void setFacilityID(string id)
    {
        this.facilityID = id;
    }
    public string getDeviceID()
    {
        return this.deviceID;
    }
    public void setDeviceID(string id)
    {
        this.deviceID = id;
    }
    public string getProxy()
    {
        return this.proxyString;
    }
    public void setProxy(string prx)
    {
        this.proxyString = prx;
    }
    public DataSet getAccelerometer()
    {
        return this.Acc;
    }
    public DataSet getAccelerometerAvg()
    {
        return this.Acc_average;
    }
    public DataSet getAccelerometerDev()
    {
        return this.Acc_deviation;
    }
    public DataSet getGyroscope()
    {
        return this.Gy;
    }
    public DataSet getGyroscopeAvg()
    {
        return this.Gy_average;
    }
    public DataSet getGyroscopeDev()
    {
        return this.Gy_deviation;
    }
    public DataSet getMagnetometer()
    {
        return this.Mg;
    }
    public DataSet getMagnetometerAvg()
    {
        return this.Mg_average;
    }
    public DataSet getMagnetometerDev()
    {
        return this.Mg_deviation;
    }
    public float getTemperature()
    {
        return this.Temp;
    }
    public float getTemperatureAvg()
    {
        return this.Temp_average;
    }
    public float getTemperatureDev()
    {
        return this.Temp_deviation;
    }
    public float getPressure()
    {
        return this.Prss;
    }
    public float getPressureAvg()
    {
        return this.Prss_average;
    }
    public float getPressureDev()
    {
        return this.Prss_deviation;
    }
    public float getHumidity()
    {
        return this.Hum;
    }
    public float getHumidityAvg()
    {
        return this.Hum_average;
    }
    public float getHumidityDev()
    {
        return this.Hum_deviation;
    }
    public float getLight()
    {
        return this.Lg;
    }
    public float getLightAvg()
    {
        return this.Lg_average;
    }
    public float getLightDev()
    {
        return this.Lg_deviation;
    }

    public DataSetLimits getAccelerometerLimits()
    {
        return this.Acc_limits;
    }
    public DataSetLimits getGyroscopeLimits()
    {
        return this.Gy_limits;
    }
    public DataSetLimits getMagnetometerLimits()
    {
        return this.Mg_limits;
    }
    public SingleDataLimits getTemperatureLimits()
    {
        return this.Temp_limits;
    }
    public SingleDataLimits getPressureLimits()
    {
        return this.Prs_limits;
    }
    public SingleDataLimits getHumidityLimits()
    {
        return this.Hum_limits;
    }
    public SingleDataLimits getLightLimits()
    {
        return this.Lgt_limits;
    }
    public bool isAccSync(){
        return this.syncAccelerometer;
    }
    public bool isGySync(){
        return syncGyroscope;
    }
    public bool isMgSync(){
        return syncMagnetometer;
    }
    public bool isTempSync(){
        return syncTemperature;
    }
    public bool isPrsSync(){
        return syncPressure;
    }
    public bool isHumSync(){
        return syncHumidity;
    }
    public bool isLightSync(){
        return syncLight;
    }
}
