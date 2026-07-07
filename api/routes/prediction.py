import numpy as np
import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.crud import save_prediction
from fastapi import APIRouter


from api.schemas import (
    LaptopInput,
    PricePredictionResponse
)
from api.dependencies import (
    price_model,
    classification_model
)

from api.feature_engineering import (
    get_processor_tier,
    get_gpu_tier,
    normalize_gpu,
    normalize_ssd,
    normalize_wifi,
    normalize_bluetooth
)



router = APIRouter()

# =====================================================
# PRICE PREDICTION
# =====================================================

@router.post(
    "/",
    response_model=PricePredictionResponse
)
def predict_price(

    data: LaptopInput,

    db: Session = Depends(get_db)):

    # =====================================================
    # COMPUTE FEATURES
    # =====================================================
    
   # =====================================================
    # NORMALIZE INPUTS
    # =====================================================
    
    processor = data.processor
    
    gpu = normalize_gpu(data.graphic_processor)
    
    ssd_type = normalize_ssd(data.ssd_type)
    
    wifi = normalize_wifi(data.wi_fi_version)
    
    bluetooth = normalize_bluetooth(data.bluetooth_version)
    
    processor_tier = get_processor_tier(processor)
    
    gpu_tier = get_gpu_tier(gpu)
    
    cpu_gpu_combo = f"{processor_tier}_{gpu_tier}"
    
    processor_tier = get_processor_tier(processor)

    gpu_tier = get_gpu_tier(gpu)
    
    cpu_gpu_combo = f"{processor_tier}_{gpu_tier}"
    # =====================================================
    # CREATE INPUT DATAFRAME
    # =====================================================
    classification_df = pd.DataFrame([{

    "Brand": data.brand,

    "Processor": processor,

    "Graphic Processor": gpu,

    "Capacity": data.capacity,

    "RAM Type": data.ram_type,

    "RAM Speed": data.ram_speed,

    "SSD Capacity": data.ssd_capacity,

    "SSD Type": ssd_type,

    "Graphics Memory": data.graphics_memory,

    "Battery Capacity": data.battery_capacity,

    "Battery Type": data.battery_type,

    "Weight": data.weight,

    "Warranty": data.warranty,

    "Wi-Fi Version": wifi,

    "Bluetooth Version": bluetooth,

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier,

    "CPU_GPU_Combo": cpu_gpu_combo

}])
   
    print("\n========== CLASSIFICATION DF ==========")
    print(classification_df)
    
    print("\n========== VALUES ==========")
    for col in classification_df.columns:
        value = classification_df.iloc[0][col]
        print(f"{col}: {value} ({type(value)})")
    
    predicted_category = classification_model.predict(
        classification_df
    ).flatten()[0]
    input_df = pd.DataFrame([{

    "Brand": data.brand,

    "Processor": processor,

    "Graphic Processor": gpu,

    "Capacity": data.capacity,

    "RAM Type": data.ram_type,

    "RAM Speed": data.ram_speed,

    "SSD Capacity": data.ssd_capacity,

    "SSD Type": ssd_type,

    "Graphics Memory": data.graphics_memory,

    "Battery Capacity": data.battery_capacity,

    "Battery Type": data.battery_type,

    "Weight": data.weight,

    "Warranty": data.warranty,

    "Wi-Fi Version": wifi,

    "Bluetooth Version": bluetooth,

    "Category": predicted_category,

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier

}])
   
    # =====================================================
    # PREDICT
    # =====================================================

    predicted_log_price = price_model.predict(input_df)[0]

    predicted_price = float(
        np.expm1(predicted_log_price)
    )
    prediction = save_prediction(

    db=db,

    data=data,

    predicted_price=predicted_price,

    predicted_category=predicted_category

)

    return PricePredictionResponse(

    prediction_id=prediction.id,

    predicted_price=round(predicted_price,2),

    predicted_category=predicted_category

)