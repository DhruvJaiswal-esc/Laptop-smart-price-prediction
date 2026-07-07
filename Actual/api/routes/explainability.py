
import pandas as pd

from fastapi import APIRouter
from fastapi import HTTPException

from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db

from database.crud import (
    save_explainability,
    get_prediction,
    delete_explainability
)
from api.dependencies import (

    shap_explainer,

    lime_explainer,

    report_generator

)

from api.feature_engineering import (

    normalize_gpu,

    normalize_ssd,

    normalize_wifi,

    normalize_bluetooth,

    get_processor_tier,

    get_gpu_tier

)






router = APIRouter()


# =====================================================
# EXPLAINABILITY
# =====================================================

@router.post("/{prediction_id}")
def explain_prediction(

    prediction_id: int,

    db: Session = Depends(get_db)

    ):  
    prediction = get_prediction(
    db,
    prediction_id
)

    if prediction is None:
        raise HTTPException(
        status_code=404,
        detail="Prediction not found"
    )
    # =====================================================
    # NORMALIZE USER INPUT
    # =====================================================

    processor = prediction.processor

    gpu = normalize_gpu(

        prediction.graphic_processor

    )

    ssd_type = normalize_ssd(

        prediction.ssd_type

    )

    wifi = normalize_wifi(

        prediction.wifi_version

    )

    bluetooth = normalize_bluetooth(

        prediction.bluetooth_version

    )

    processor_tier = get_processor_tier(

        processor

    )

    gpu_tier = get_gpu_tier(

        gpu

    )

   

    # =====================================================
    # CLASSIFICATION INPUT
    # =====================================================

    

    predicted_category = prediction.predicted_category
    # =====================================================
    # PRICE PREDICTION INPUT
    # =====================================================

    prediction_df = pd.DataFrame([{

    "Brand": prediction.brand,

    "Processor": processor,

    "Graphic Processor": gpu,

    "Capacity": prediction.capacity,

    "RAM Type": prediction.ram_type,

    "RAM Speed": prediction.ram_speed,

    "SSD Capacity": prediction.ssd_capacity,

    "SSD Type": ssd_type,

    "Graphics Memory": prediction.graphics_memory,

    "Battery Capacity": prediction.battery_capacity,

    "Battery Type": prediction.battery_type,

    "Weight": prediction.weight,

    "Warranty": prediction.warranty,

    "Wi-Fi Version": wifi,

    "Bluetooth Version": bluetooth,

    "Category": predicted_category,

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier

}])
    # =====================================================
    # PRICE PREDICTION
    # =====================================================

    predicted_price = prediction.predicted_price
    
    # =====================================================
    # SHAP EXPLANATION
    # =====================================================

    shap_result = shap_explainer.explain_prediction(

        prediction_df,

        save_plots=True,

        top_n=10

    )

    # =====================================================
    # LIME EXPLANATION
    # =====================================================
 
    lime_result = lime_explainer.explain_prediction(

        prediction_df,

        save_html=True,

        top_n=10

    )
    report_path = report_generator.generate_report(

    laptop_information=prediction_df.iloc[0].to_dict(),

    predicted_price=predicted_price,

    predicted_category=predicted_category,

    shap_result=shap_result,

    lime_result=lime_result

    )
    delete_explainability(
    db,
    prediction_id
    )
    
    save_explainability(
        db=db,
        prediction_id=prediction_id,
        shap_result=shap_result,
        lime_result=lime_result,
        report_path=report_path
    )
        # =====================================================
    # RESPONSE
    # =====================================================

    response = {

    "prediction_id": prediction_id,

    "prediction": {

        "predicted_price": round(
            predicted_price,
            2
        ),

        "predicted_category": predicted_category

    },

    "input": prediction_df.iloc[0].to_dict(),

    "shap": shap_result,

    "lime": lime_result,

    "report": report_path

}

    return response