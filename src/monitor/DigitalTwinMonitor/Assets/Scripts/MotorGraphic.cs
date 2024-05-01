using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MotorGraphic : MonoBehaviour
{
    private bool isShowing;
    private bool isInRange;

    [Header("Interaction")]
    [SerializeField] KeyCode interactKey;
    [SerializeField] GameObject interactMessageUI;
    [SerializeField] GameObject warningIcon;
    [SerializeField] Color warnColor = new Color(160, 0, 0, 1);
    [SerializeField] Color baseColor = new Color(0, 160, 0, 1);

    [Header("Values UI references")]
    [SerializeField] Canvas screenSpaceCanvas;
    [SerializeField] Canvas worldSpaceCanvas;
    [SerializeField] GameObject informationPanel;
    [SerializeField] Text connectionStateLabel;
    [SerializeField] InputField FacilityIDField;
    [SerializeField] InputField DeviceIDField;
    [SerializeField] InputField proxyField;
    [Space]
    [Header("Tabs")]
    [SerializeField] Dropdown tabSelector;
    [Space]
    [SerializeField] tabDataSetObject tab_Accelerometer;
    [SerializeField] tabDataSetObject tab_Gyroscope;
    [SerializeField] tabDataSetObject tab_Magnetometer;
    [SerializeField] tabSingleDataObject tab_Temperature, tab_Pressure, tab_Humidity, tab_Light;
    [Space]
    [SerializeField] GameObject worldWarningGameObject;
    [SerializeField] GameObject menuWarningGameObject;
    private bool isWarning = false;

    // aux
    private GameObject player;
    private GameObject cameraControl;
    private dt_client motor;

    //Motor graphics
    [Header("Motor graphics")]
    [SerializeField] AudioSource motorSound;
    [SerializeField] GameObject motorBody;
    [SerializeField] GameObject rotatoryPart;
    private Vector3 initialPosition;
    [Range(0, 5)]
    public float vibration = 2f;
    [Range(1, 100)]
    public float rotationSpeed = 30f;


    private void Awake()
    {
        // Initialize variables
        motor = GetComponent<dt_client>();
        player = GameObject.FindGameObjectWithTag("Player");
        cameraControl = GameObject.FindGameObjectWithTag("CinemachineCamera");

        //Initial position for vibration
        initialPosition = motorBody.transform.position;

        // Set IDs
        FacilityIDField.text = motor.getFacilityID();
        DeviceIDField.text = motor.getDeviceID();

        // Add Listener to implement tabs
        tabSelector.onValueChanged.AddListener(delegate
        {
            onTabSelected(tabSelector.value);
        });
    }

    private void Start()
    {
        onTabSelected(0);   //Initialize with first tab selected
        updateInfo();
        screenSpaceCanvas.gameObject.SetActive(false);
        informationPanel.transform.SetParent(worldSpaceCanvas.transform, false);
    }
    private void Update()
    {
        if (isInRange)
        {  //If player is in range
            if (Input.GetKeyDown(interactKey) && !isShowing)
            {  //If player is pressing interact key
                ShowMotorInfoPanel();
            }
        }

        if (motor.isConnected)
        {
            
            //Motor Vibration
            motorBody.transform.position = initialPosition;
            motorBody.transform.Translate(Random.insideUnitSphere * vibration * Time.deltaTime, motorBody.transform);
            //Motor rotation
            rotatoryPart.transform.Rotate(new Vector3(0, vibration, 0), rotatoryPart.transform.rotation.x + rotationSpeed);
            //Motor sound volume
            motorSound.volume = 0.7f;
        }

        if((motor.isAccSync() && tab_Accelerometer!=null && tab_Accelerometer.hasWarning()) ||
            (motor.isGySync() && tab_Gyroscope!=null && tab_Gyroscope.hasWarning()) ||
            (motor.isMgSync() && tab_Magnetometer!=null && tab_Magnetometer.hasWarning()) ||
            (motor.isTempSync() && tab_Temperature!=null && tab_Temperature.hasWarning()) ||
            (motor.isPrsSync() && tab_Pressure!=null && tab_Pressure.hasWarning()) ||
            (motor.isHumSync() && tab_Humidity!=null && tab_Humidity.hasWarning()) ||
            (motor.isLightSync() && tab_Light!=null && tab_Light.hasWarning())){
            
            if(isWarning == false){
                isWarning = true;
                worldWarningGameObject.SetActive(true);
                menuWarningGameObject.SetActive(true);

                //Motor Color
                for (int i = 0; i < motorBody.transform.childCount; i++){
                    motorBody.transform.GetChild(i).gameObject.GetComponent<Renderer>().material.color = warnColor;
                }
            }
            

        }else{
            if(isWarning == true){
                isWarning = false;
                worldWarningGameObject.SetActive(false);
                menuWarningGameObject.SetActive(false);

                //Motor Color
                for (int i = 0; i < motorBody.transform.childCount; i++){
                    motorBody.transform.GetChild(i).gameObject.GetComponent<Renderer>().material.color = baseColor;
                }
            }
        }

        
    }

    public void UpdateMotorInformation(string dataToUpdate)
    {
        try{
            // Set values on the labels
            switch (dataToUpdate)
            {
                case "Accelerometer":
                    tab_Accelerometer.updateGraphs(motor.getAccelerometer());
                    break;
                case "Gyroscope":
                    tab_Gyroscope.updateGraphs(motor.getGyroscope());
                    break;
                case "Magnetometer":
                    tab_Magnetometer.updateGraphs(motor.getMagnetometer());
                    break;
                case "Temperature":
                    tab_Temperature.updateGraph(motor.getTemperature());
                    break;
                case "Pressure":
                    tab_Pressure.updateGraph(motor.getPressure());
                    break;
                case "Humidity":
                    tab_Humidity.updateGraph(motor.getHumidity());
                    break;
                case "Light":
                    tab_Light.updateGraph(motor.getLight());
                    break;
                default:
                    Debug.Log("Updating server's connection state");
                    break;
            }

        }catch{
            Debug.LogWarning("Error trying to update information on option '" + dataToUpdate + "'");
        }

        // Set the connection state
        if (motor.isConnected)
        {
            connectionStateLabel.text = "Conectado";
            connectionStateLabel.color = new Color(0, 255, 0, 1);
            if (!motorSound.isPlaying) motorSound.Play();
        }
        else
        {
            connectionStateLabel.text = "No conectado";
            connectionStateLabel.color = new Color(255, 0, 0, 1);
            motorSound.Stop();
        }

    }

    public void UpdateLimits(string dataToUpdate)
    {
        try{
            // Set values on the labels
            switch (dataToUpdate)
            {
                case "Accelerometer":
                    tab_Accelerometer.updateLimits(motor.getAccelerometerLimits());
                    break;
                case "Gyroscope":
                    tab_Gyroscope.updateLimits(motor.getGyroscopeLimits());
                    break;
                case "Magnetometer":
                    tab_Magnetometer.updateLimits(motor.getMagnetometerLimits());
                    break;
                case "Temperature":
                    tab_Temperature.updateLimit(motor.getTemperatureLimits());
                    break;
                case "Pressure":
                    tab_Pressure.updateLimit(motor.getPressureLimits());
                    break;
                case "Humidity":
                    tab_Humidity.updateLimit(motor.getHumidityLimits());
                    break;
                case "Light":
                    tab_Light.updateLimit(motor.getLightLimits());
                    break;
                default:
                    break;
            }

        }catch{
            Debug.LogWarning("Error trying to update limits on option '" + dataToUpdate + "'");
        }
    }

    // Refresh the motor connection with the established proxy
    public void refreshMotorConnection()
    {
        Debug.Log("Refreshing [" + FacilityIDField.text + ", " + DeviceIDField.text + "]: " + proxyField.text);
        motor.setFacilityID(FacilityIDField.text);
        motor.setDeviceID(DeviceIDField.text);
        motor.setProxy(proxyField.text);
        motor.Refresh();

    }
    public void ShowMotorInfoPanel()
    {
        //Lock Player and camera
        player.GetComponent<PlayerMovement>().enabled = false;
        cameraControl.SetActive(false);

        // Show motor info
        isShowing = true;
        informationPanel.transform.SetParent(screenSpaceCanvas.transform, false);
        informationPanel.transform.SetAsFirstSibling();
        
        updateInfo();
        screenSpaceCanvas.gameObject.SetActive(true);
        Cursor.lockState = CursorLockMode.Confined;
    }

    public void HideMotorInfoPanel()
    {
        //Unlock player and camera
        player.GetComponent<PlayerMovement>().enabled = true;
        cameraControl.SetActive(true);

        // Show motor info
        isShowing = false;
        updateInfo();
        screenSpaceCanvas.gameObject.SetActive(false);
        informationPanel.transform.SetParent(worldSpaceCanvas.transform, false);
        Cursor.lockState = CursorLockMode.Locked;
    }

    private void updateInfo(){
        FacilityIDField.text = motor.getFacilityID();
        DeviceIDField.text = motor.getDeviceID();
        proxyField.text = motor.getProxy();
    }

    private void OnTriggerEnter(Collider collision)
    {
        if (collision.gameObject.CompareTag("Player"))
        {
            isInRange = true;
            //Show interact message
            interactMessageUI.SetActive(true);
            Debug.Log("Player in range");
        }
    }

    private void OnTriggerExit(Collider collision)
    {
        if (collision.gameObject.CompareTag("Player"))
        {
            isInRange = false;
            //Hide interact message
            interactMessageUI.SetActive(false);
            Debug.Log("Player out of range");
        }
    }

    private void onTabSelected(int change)
    {
        Debug.Log("Tab selected: " + change);

        deactivateAllTabs();

        try
        {
            switch (change)
            {
                case 0: //Accelerometer
                    Debug.Log("Dropdown: Selected Accelerometer tab (option 0)");
                    tab_Accelerometer.gameObject.SetActive(true);
                    break;
                case 1: //Gyroscope
                    Debug.Log("Dropdown: Selected Gyroscope tab (option 1)");
                    tab_Gyroscope.gameObject.SetActive(true);
                    break;
                case 2: //Magnetometer
                    Debug.Log("Dropdown: Selected Magnetometer tab (option 2)");
                    tab_Magnetometer.gameObject.SetActive(true);
                    break;
                case 3: //Temperature
                    Debug.Log("Dropdown: Selected Temperature tab (option 3)");
                    tab_Temperature.gameObject.SetActive(true);
                    break;
                case 4: //Pressure
                    Debug.Log("Dropdown: Selected Pressure tab (option 4)");
                    tab_Pressure.gameObject.SetActive(true);
                    break;
                case 5: //Humidity
                    Debug.Log("Dropdown: Selected Humidity tab (option 5)");
                    tab_Humidity.gameObject.SetActive(true);
                    break;
                case 6: //Light
                    Debug.Log("Dropdown: Selected Light tab (option 6)");
                    tab_Light.gameObject.SetActive(true);
                    break;
                default:    // Not possible
                    Debug.LogWarning("Dropdown error: Invalid option (" + change + ")");
                    break;
            }
        }
        catch { }

    }

    private void deactivateAllTabs()
    {
        try
        {
            tab_Accelerometer.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Gyroscope.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Magnetometer.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Temperature.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Pressure.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Humidity.gameObject.SetActive(false);
        }
        catch { }
        try
        {
            tab_Light.gameObject.SetActive(false);
        }
        catch { }
    }
}
