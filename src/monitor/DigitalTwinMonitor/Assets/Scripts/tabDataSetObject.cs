using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using digitaltwin;

public class tabDataSetObject : MonoBehaviour
{

    [Header("GraphDrawings")]
    [SerializeField] WindowGraphDrawing X_Drawing;
    [SerializeField] WindowGraphDrawing Y_Drawing;
    [SerializeField] WindowGraphDrawing Z_Drawing;

    public void updateGraphs(digitaltwin.DataSet values){
        X_Drawing.UpdateValues(values.x);
        Y_Drawing.UpdateValues(values.y);
        Z_Drawing.UpdateValues(values.z);
    }

    public void updateLimits(digitaltwin.DataSetLimits limits){
        X_Drawing.UpdateLimits(limits.xMaxLimit, limits.xMinLimit);
        Y_Drawing.UpdateLimits(limits.yMaxLimit, limits.yMinLimit);
        Z_Drawing.UpdateLimits(limits.zMaxLimit, limits.zMinLimit);
    }

    public bool hasWarning(){
        
        if(X_Drawing.warning){
            return true;
        }else if(Y_Drawing.warning){
            return true;
        }else if(Z_Drawing.warning){
            return true;
        }else{
            return false;
        }
    }

}
