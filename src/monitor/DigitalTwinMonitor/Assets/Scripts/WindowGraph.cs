using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class WindowGraph : MonoBehaviour
{

    [Header("Graph")]
    public RectTransform graphContainer;

    [Header("X AXIS")]
    [Range(50, 500)]
    [SerializeField] int dotsAmount = 300;
    [Range(0.1f, 0.9f)]
    [SerializeField] float previsionPart = 0.4f;
    [SerializeField] int xLabelsNum = 10;
    [SerializeField] RectTransform labelTemplateX;
    [Range(0, 10)]
    private float xLabelsOffset = 3f;
    [SerializeField] RectTransform dashXAxisTemplate;
    private bool showLabelsX = false;

    [Header("Y AXIS")]
    [SerializeField] float yMaximum = 1.5f;
    [SerializeField] float yMinimum = -1.5f;
    [Range(0, 20)]
    [SerializeField] int yLabelsNum = 10;
    [SerializeField] RectTransform labelTemplateY;
    [Range(0, 30)]
    [SerializeField] float yLabelsOffset = 5f;

    public RectTransform dashYAxisTemplate;
    [Space]
    public GameObject warningGameObject;

    private List<GameObject> axisGameObjectsList;

    [HideInInspector]
    private float graphWidth, graphHeight,xSize;

    void Awake()
    {
        axisGameObjectsList = new List<GameObject>();

        graphHeight = graphContainer.sizeDelta.y;
        graphWidth = graphContainer.sizeDelta.x;
        xSize = graphWidth / xLabelsNum;

        DrawGraphAxis();

    }

    private void DrawGraphAxis()
    {
        foreach (GameObject gameObject in axisGameObjectsList)
        {
            Destroy(gameObject);
        }
        axisGameObjectsList.Clear();

        // For each value passed
        for (int i = 0; i < xLabelsNum; i++)
        {
            float xPosition = xSize + i * xSize;

            if(showLabelsX){
                //Draw label X
                RectTransform labelX = Instantiate(labelTemplateX);
                labelX.SetParent(graphContainer, false);
                labelX.gameObject.SetActive(true);
                labelX.anchoredPosition = new Vector2(xPosition, -xLabelsOffset);
                labelX.GetComponent<Text>().text = (-xLabelsNum + i +1).ToString();
                axisGameObjectsList.Add(labelX.gameObject);
            }

            //Draw dash X
            RectTransform dashX = Instantiate(dashXAxisTemplate);
            dashX.SetParent(graphContainer, false);
            dashX.SetAsFirstSibling();
            dashX.gameObject.SetActive(true);
            dashX.anchoredPosition = new Vector2(xPosition + .5f, 0);
            dashX.localScale = new Vector3(graphHeight, 1, 1);
            axisGameObjectsList.Add(dashX.gameObject);

        }

        //Draw dash X at 0
        RectTransform dashX0 = Instantiate(dashXAxisTemplate);
        dashX0.GetComponent<Image>().color = new Color(255, 255, 255, 1);
        dashX0.SetParent(graphContainer, false);
        dashX0.gameObject.SetActive(true);
        dashX0.anchoredPosition = new Vector2(xLabelsNum*xSize*(1 - previsionPart) + .5f, 0);
        dashX0.localScale = new Vector3(graphHeight, 1, 1);
        dashX0.SetAsLastSibling();
        axisGameObjectsList.Add(dashX0.gameObject);

        //Draw labels Y
        for (int i = 0; i <= yLabelsNum; i++)
        {
            RectTransform labelY = Instantiate(labelTemplateY);
            labelY.SetParent(graphContainer, false);
            labelY.gameObject.SetActive(true);
            float normalizedValue = i * 1f / yLabelsNum;
            labelY.anchoredPosition = new Vector2(-yLabelsOffset, normalizedValue * graphHeight);
            labelY.GetComponent<Text>().text = (yMinimum + (normalizedValue * (yMaximum - yMinimum))).ToString("0.00");
            axisGameObjectsList.Add(labelY.gameObject);

            //Draw dash Y
            RectTransform dashY = Instantiate(dashYAxisTemplate);
            dashY.SetParent(graphContainer, false);
            dashY.SetAsFirstSibling();
            dashY.gameObject.SetActive(true);
            dashY.anchoredPosition = new Vector2(0, normalizedValue * graphHeight);
            dashY.localScale = new Vector3(graphWidth, 1, 1);
            axisGameObjectsList.Add(dashY.gameObject);
        }

        // Draw dash Y at 0
        RectTransform dashY0 = Instantiate(dashYAxisTemplate);
        dashY0.SetParent(graphContainer, false);
        dashY0.gameObject.SetActive(true);
        dashY0.anchoredPosition = new Vector2(0, ((-yMinimum) / (yMaximum - yMinimum)) * graphHeight);
        dashY0.localScale = new Vector3(graphWidth, 1, 1);
        dashY0.GetComponent<Image>().color = new Color(255, 255, 255, 1);
        dashY0.SetAsLastSibling();
        axisGameObjectsList.Add(dashY0.gameObject);
    }

    public void redrawGraph(float max, float min){
        this.yMaximum = max + (max - min)*0.2f;
        this.yMinimum = min - (max - min)*0.2f;
        this.DrawGraphAxis();
    }
    public float getYMaximum(){
        return this.yMaximum;
    }
    public float getYMinimum(){
        return this.yMinimum;
    }

    public int getDotsAmount(){
        return this.dotsAmount;
    }

    public float getPrevisionPart(){
        return this.previsionPart;
    }
}
