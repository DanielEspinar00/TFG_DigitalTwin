using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class tabSingleDataObject : MonoBehaviour
{

    [Header("GraphDrawing")]
    [SerializeField] WindowGraphDrawing Value_Drawing;
    
    public void updateGraph(float val){
        Value_Drawing.UpdateValues(val);
    }

    public void updateLimit(digitaltwin.SingleDataLimits limits){
        Value_Drawing.UpdateLimits(limits.maxLimit, limits.minLimit);
    }

    public bool hasWarning(){
        
        return Value_Drawing.warning;
    }
}
