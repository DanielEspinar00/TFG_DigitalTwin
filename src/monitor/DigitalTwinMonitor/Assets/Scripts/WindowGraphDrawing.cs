using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;
using System;

public class WindowGraphDrawing : MonoBehaviour
{
    [Header("Graph")]
    [SerializeField] WindowGraph graphBase;
    [SerializeField] Color graphColor = new Color(255, 255, 255, 1);
    [SerializeField] Sprite dotSprite;
    [Range(1,10)]
    [SerializeField] int dotSize = 5;

    [SerializeField] Color limitColor = new Color(255, 255, 0, 1);
    [SerializeField] Color predictionColor = new Color(255, 255, 255, 0.5f);

    [Range(3, 40)]
    [SerializeField] int step = 5;

    [Header("Value fields")]
    [SerializeField] Text valueField;
    [SerializeField] Text averageField;
    [SerializeField] Text maxField;
    [SerializeField] Text minField;
    [SerializeField] Text upLimitField;
    [SerializeField] Text lowLimitField;

    private LineGraph lineGraph;
    private List<LineGraphObject> graphVisualObjectList = new List<LineGraphObject>();
    private List<LineGraphObject> graphPredictionObjectList = new List<LineGraphObject>();

    private float graphWidth, graphHeight, xSize, predictionAmount, readingsAmount;

    private RectTransform lineAverage, limitsZone;

    private float upperLimit, lowerLimit;

    [NonSerialized]
    public bool warning = false;
    private float currentMax = 0.0f, currentMin = 0.0f;

    void Start()
    {
        lineGraph = new LineGraph(graphBase.graphContainer, graphColor, predictionColor, dotSprite, dotSize);

        // Calculate graph dimensions
        graphHeight = graphHeight = graphBase.graphContainer.sizeDelta.y;
        graphWidth = graphBase.graphContainer.sizeDelta.x * (1 - graphBase.getPrevisionPart());

        predictionAmount = (int)graphBase.getDotsAmount() * graphBase.getPrevisionPart();
        readingsAmount = graphBase.getDotsAmount() - predictionAmount;

        xSize = graphWidth / readingsAmount;
        
        // Draw average line
        float yPosition = (((graphBase.getYMaximum() + graphBase.getYMinimum())/2 - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;
        lineAverage = Instantiate(graphBase.dashYAxisTemplate);
        lineAverage.SetParent(graphBase.graphContainer, false);
        lineAverage.GetComponent<Image>().color = limitColor;
        lineAverage.gameObject.SetActive(true);
        lineAverage.anchoredPosition = new Vector2(0, yPosition);
        lineAverage.localScale = new Vector3(graphWidth, 1, 1);

        // Draw top margin
        limitsZone = Instantiate(graphBase.dashYAxisTemplate);
        limitsZone.SetParent(graphBase.graphContainer, false);
        limitColor.a = 0.3f;
        limitsZone.GetComponent<Image>().color = limitColor;
        limitsZone.gameObject.SetActive(true);
        limitsZone.anchoredPosition = new Vector2(0, yPosition);
        limitsZone.localScale = new Vector3(graphWidth, 10, 1);

        // Fill the values list
        List<float> valueList = new List<float>();
        for(int i= 0; i < readingsAmount; i++){
            valueList.Add((graphBase.getYMaximum() + graphBase.getYMinimum())/2);
        }

        // Initialize dots and connections
        DrawDots(valueList);
        DrawPredictions(valueList);
    }

    public void DrawDots(List<float> valueList)
    {

        foreach (LineGraphObject graphVisualObject in graphVisualObjectList)
        {
            graphVisualObject.CleanUp();
        }
        graphVisualObjectList.Clear();

        int xIndex = 0;

        // For each value passed
        for (int i = (valueList.Count - 1); i >= Mathf.Max(valueList.Count - readingsAmount, 0); i--)
        {
            float xPosition = readingsAmount * xSize;
            float yPosition = ((valueList[i] - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

            graphVisualObjectList.Add(lineGraph.CreateLineGraphObject(valueList[i], new Vector2(xPosition, yPosition)));

            xIndex++;
        }
    }

    public void DrawPredictions(List<float> valueList)
    {

        foreach (LineGraphObject graphVisualObject in graphPredictionObjectList)
        {
            graphVisualObject.CleanUp();
        }
        graphPredictionObjectList.Clear();

        int xIndex = 0;

        // For each value passed
        for (int i = (valueList.Count - 1); i >= Mathf.Max(valueList.Count - predictionAmount, 0); i--)
        {
            float xPosition = (readingsAmount + predictionAmount) * xSize;
            float yPosition = ((valueList[i] - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

            graphPredictionObjectList.Add(lineGraph.CreatePredictionObject(valueList[i], new Vector2(xPosition, yPosition)));

            xIndex++;
        }
    }

    private void AddValue(float value, int pos){
        float xPosition = (readingsAmount * xSize) - pos * xSize;
        float yPosition = ((value - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

        graphVisualObjectList.Add(lineGraph.CreateLineGraphObject(value, new Vector2(xPosition, yPosition)));
    }

    public void UpdateValues(float value){
        bool outOfMargins = false;
        float auxMax = value, auxMin = value;
        
        if(graphVisualObjectList.Count < readingsAmount){
            AddValue(value, 0);
        }else{

            for(int i = 0; i < (graphVisualObjectList.Count-1); i++){
                // Get the value and position of the next dot
                float aux = graphVisualObjectList[i+1].getValue();
                Vector2 pos = graphVisualObjectList[i+1].GetGraphPostion();

                graphVisualObjectList[i].SetGraphObjectInfo(new Vector2(pos.x - xSize, pos.y), aux);

                //Check if value surpasses limits
                if(aux > upperLimit || aux < lowerLimit) outOfMargins = true;

                //Update max and min
                if(aux>auxMax) auxMax = aux;
                else if(aux < auxMin) auxMin = aux;

            }

            // Calculate new position of last dot
            float xPosition = xSize + (graphVisualObjectList.Count-1) * xSize;
            float yPosition = ((value - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;
            graphVisualObjectList[graphVisualObjectList.Count-1].SetGraphObjectInfo(new Vector2(xPosition, yPosition), value);
            //Check if value surpasses limits
            if(value > upperLimit || value < lowerLimit) outOfMargins = true;

            //Check if value gets out of the box
            if(value > graphBase.getYMaximum() || value < graphBase.getYMinimum()){
                this.refreshGraph();
            }

            UpdatePredictions();
        }

        currentMax = auxMax;
        currentMin = auxMin;

        setValuesText(value);
        graphBase.warningGameObject.SetActive(outOfMargins);
        warning = outOfMargins;
    }

    private void UpdatePredictions(){
        for(int i=0; i < (graphPredictionObjectList.Count-1); i++){
            // Get the value and position of the next dot
            float aux = graphPredictionObjectList[i+1].getValue();
            Vector2 pos = graphPredictionObjectList[i+1].GetGraphPostion();
            
            graphPredictionObjectList[i].SetGraphObjectInfo(new Vector2(pos.x - xSize, pos.y), aux);
        }

        // Calculate new value
        float value = 0f;

        for(int i=0; i < step; i++){
            value += graphVisualObjectList[graphVisualObjectList.Count-1 - i].getValue();
        }

        float xPosition = xSize + (graphPredictionObjectList.Count-1) * xSize + readingsAmount*xSize;
        float yPosition = (((value/step) - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

        graphPredictionObjectList[graphPredictionObjectList.Count-1].SetGraphObjectInfo(new Vector2(xPosition, yPosition), value/step);

    }

    public void UpdateLimits(float max, float min){
        // Update values
        this.upperLimit = max;
        this.lowerLimit = min;

        reDrawLimits();
    }

    public void refreshGraph(){
        graphBase.redrawGraph(Math.Max(upperLimit, currentMax), Math.Min(lowerLimit, currentMin));
        reDrawDots();
        reDrawLimits();
    }

    private void reDrawDots(){
        for(int i = 0; i < graphVisualObjectList.Count; i++){
            float value = graphVisualObjectList[i].getValue();
            Vector2 pos = graphVisualObjectList[i].GetGraphPostion();
            float xPosition = xSize + i * xSize;
            float yPosition = ((value - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

            graphVisualObjectList[i].SetGraphObjectInfo(new Vector2(pos.x, yPosition), value);
        }
        for(int i = 0; i < graphPredictionObjectList.Count; i++){
            float value = graphPredictionObjectList[i].getValue();
            Vector2 pos = graphPredictionObjectList[i].GetGraphPostion();
            float xPosition = xSize + i * xSize;
            float yPosition = ((value - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;

            graphPredictionObjectList[i].SetGraphObjectInfo(new Vector2(pos.x, yPosition), value);
        }
    }

    private void reDrawLimits(){
        // Draw average
        float yPosition = (((this.upperLimit+this.lowerLimit)/2 - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;
        lineAverage.anchoredPosition = new Vector2(0, yPosition);

        // Draw Limits
        float aux = (((upperLimit) - graphBase.getYMinimum()) / (graphBase.getYMaximum() - graphBase.getYMinimum())) * graphHeight;
        float margin = aux - yPosition;
        limitsZone.anchoredPosition = new Vector2(0, yPosition);
        limitsZone.localScale = new Vector3(graphWidth, margin, 1);
        Debug.Log("Mitad: "+(this.upperLimit+this.lowerLimit)+", Min: "+graphBase.getYMinimum());
    }

    // Set labels text
    private void setValuesText(float value){
        if(valueField != null) valueField.text = value.ToString("0.00");
        //if(averageField != null) averageField.text = average.ToString("0.00");
        if(maxField != null) maxField.text = currentMax.ToString("0.00");
        if(minField != null) minField.text = currentMin.ToString("0.00");
        if(upLimitField != null) upLimitField.text = upperLimit.ToString("0.00");
        if(lowLimitField != null) lowLimitField.text = lowerLimit.ToString("0.00");
    }

    // Get angle from a vector
    public static float GetAngleFromVector(Vector3 vector)
    {
        vector = vector.normalized;
        float angle = Mathf.Atan2(vector.y, vector.x) * Mathf.Rad2Deg;
        if (angle < 0) angle += 360;

        return angle;
    }

    // Line graph class
    private class LineGraph
    {
        private RectTransform graphContainer;
        private Color graphColor, predictionColor;
        private Sprite dotSprite;
        private int dotSize;
        private LineGraphObject lastLineGraphObject, lastLineGraphPredictionObject;

        public LineGraph(RectTransform graphContainer, Color graphColor, Color predictionColor, Sprite dotSprite, int dotSize)
        {
            this.graphContainer = graphContainer;
            this.graphColor = graphColor;
            this.predictionColor = predictionColor;
            this.dotSprite = dotSprite;
            this.dotSize = dotSize;
            this.lastLineGraphObject = null;
            this.lastLineGraphPredictionObject = null;

            
        }

        public LineGraphObject CreateLineGraphObject(float value, Vector2 graphPosition)
        {

            GameObject dotObject = CreateDot(graphPosition, graphColor);
            dotObject.transform.SetAsLastSibling();

            GameObject dotConnectionGameObject = null;
            
            if (lastLineGraphObject != null)
            {
                dotConnectionGameObject = CreateDotConnection(lastLineGraphObject.GetGraphPostion(), dotObject.GetComponent<RectTransform>().anchoredPosition, graphColor);
                dotConnectionGameObject.transform.SetAsLastSibling();
            }

            LineGraphObject lineGraphObject = new LineGraphObject(graphPosition, value, dotObject, dotConnectionGameObject, lastLineGraphObject);

            lastLineGraphObject = lineGraphObject;

            return lineGraphObject;
        }

        public LineGraphObject CreatePredictionObject(float value, Vector2 graphPosition)
        {

            GameObject dotGameObject = CreateDot(graphPosition, predictionColor);
            dotGameObject.transform.SetAsLastSibling();

            GameObject dotConnectionGameObject = null;
            
            if (lastLineGraphPredictionObject != null)
            {
                dotConnectionGameObject = CreateDotConnection(lastLineGraphPredictionObject.GetGraphPostion(), dotGameObject.GetComponent<RectTransform>().anchoredPosition, predictionColor);
                dotConnectionGameObject.transform.SetAsLastSibling();
            }

            LineGraphObject lineGraphObject = new LineGraphObject(graphPosition, value, dotGameObject, dotConnectionGameObject, lastLineGraphPredictionObject);

            lastLineGraphPredictionObject = lineGraphObject;

            return lineGraphObject;
        }

        private GameObject CreateDot(Vector2 position, Color dotColor)
        {
            GameObject dotObject = new GameObject("dot", typeof(Image));
            dotObject.transform.SetParent(graphContainer, false);
            dotObject.GetComponent<Image>().sprite = dotSprite;
            dotObject.GetComponent<Image>().color = dotColor;
            RectTransform dotRectT = dotObject.GetComponent<RectTransform>();
            dotRectT.anchoredPosition = position;
            dotRectT.sizeDelta = new Vector2(dotSize, dotSize);
            dotRectT.anchorMin = new Vector2(0, 0);
            dotRectT.anchorMax = new Vector2(0, 0);

            return dotObject;
        }

        // Draw line between dots
        private GameObject CreateDotConnection(Vector2 dotPositionA, Vector2 dotPositionB, Color connectionColor)
        {
            GameObject dotConnection = new GameObject("dotConnection", typeof(Image));
            dotConnection.transform.SetParent(graphContainer, false);
            dotConnection.GetComponent<Image>().color = connectionColor;
            RectTransform dotConnRectT = dotConnection.GetComponent<RectTransform>();
            Vector2 dir = (dotPositionB - dotPositionA).normalized;
            float distance = Vector2.Distance(dotPositionA, dotPositionB);
            dotConnRectT.anchorMin = new Vector2(0, 0);
            dotConnRectT.anchorMax = new Vector2(0, 0);
            dotConnRectT.sizeDelta = new Vector2(distance, 0.1f);
            dotConnRectT.anchoredPosition = dotPositionA + dir * distance * .5f;
            dotConnRectT.localEulerAngles = new Vector3(0, 0, GetAngleFromVector(dir));

            return dotConnection;
        }
    }

    // Line Graph Object Class
    public class LineGraphObject
    {
        public event EventHandler OnChangedGraphObjectInfo;
        GameObject dotGameObject;
        float value;
        Vector2 position;
        GameObject dotConnectionGameObject;
        LineGraphObject lastVisualObject;
        public LineGraphObject(Vector2 position, float value, GameObject dotGameObject, GameObject dotConnectionGameObject, LineGraphObject lastVisualObject)
        {
            this.position = position;
            this.value = value;
            this.dotGameObject = dotGameObject;
            this.dotConnectionGameObject = dotConnectionGameObject;
            this.lastVisualObject = lastVisualObject;

            if(lastVisualObject != null){
                lastVisualObject.OnChangedGraphObjectInfo += LastObject_OnChangedGraphObjectInfo;
            }
        }

        private void LastObject_OnChangedGraphObjectInfo(object sender, EventArgs e){
            UpdateDotConnecion();
        }

        public void SetGraphObjectInfo(Vector2 position, float value)
        {
            this.position = position;
            this.value = value;

            RectTransform rectT = dotGameObject.GetComponent<RectTransform>();
            rectT.anchoredPosition = position;
            rectT.SetAsLastSibling();

            UpdateDotConnecion();

            if(OnChangedGraphObjectInfo != null) OnChangedGraphObjectInfo(this, EventArgs.Empty);
        }

        public void CleanUp()
        {
            Destroy(dotGameObject);
            Destroy(dotConnectionGameObject);
        }

        public float getValue(){
            return this.value;
        }

        public Vector2 GetGraphPostion(){
            RectTransform rectTransform = dotGameObject.GetComponent<RectTransform>();
            return rectTransform.anchoredPosition;
        }

        private void UpdateDotConnecion(){
            if (dotConnectionGameObject != null)
            {
                RectTransform dotConnRectT = dotConnectionGameObject.GetComponent<RectTransform>();
                Vector2 dir = (lastVisualObject.GetGraphPostion() - this.GetGraphPostion()).normalized;
                float distance = Vector2.Distance(this.GetGraphPostion(), lastVisualObject.GetGraphPostion());
                dotConnRectT.sizeDelta = new Vector2(distance, 3f);
                dotConnRectT.anchoredPosition = this.GetGraphPostion() + dir * distance * .5f;
                dotConnRectT.localEulerAngles = new Vector3(0, 0, GetAngleFromVector(dir));
                dotConnRectT.SetAsLastSibling();
            }
        }
    }
}
