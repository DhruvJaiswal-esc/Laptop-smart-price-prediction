import numpy as np
import pandas as pd

from fastapi import APIRouter


from api.schemas import (
    LaptopInput,
    PricePredictionResponse
)
from api.dependencies import (
    price_model,
    classification_model,
    laptop_dataset
)



router = APIRouter()

# =====================================================
# PRICE PREDICTION
# =====================================================

@router.post(
    "/",
    response_model=PricePredictionResponse
)
def predict_price(data: LaptopInput):

    # =====================================================
    # COMPUTE FEATURES
    # =====================================================
    
    # =====================================================
    # FIND CLOSEST MATCH
    # =====================================================

    processor_matches = laptop_dataset[
        laptop_dataset["Processor"]
        .str.contains(
            data.processor,
            case=False,
            na=False,
            regex=False
        )
    ]
    
    gpu_matches = processor_matches[
        processor_matches["Graphic Processor"]
        .str.contains(
            data.graphic_processor,
            case=False,
            na=False,
            regex=False
        )
    ]
    
    if gpu_matches.empty:
    
        processor_matches = laptop_dataset[
            laptop_dataset["Processor"]
            .str.lower()
            .str.contains(
                data.processor.lower().replace("intel ", "").replace("amd ", ""),
                na=False
            )
        ]
    
        gpu_matches = processor_matches[
            processor_matches["Graphic Processor"]
            .str.lower()
            .str.contains(
                data.graphic_processor.lower().replace("nvidia ", "").replace("geforce ", ""),
                na=False
            )
        ]
    
    if gpu_matches.empty:
        raise ValueError(
            f"Couldn't find {data.processor} + {data.graphic_processor}"
        )
    
    match = gpu_matches.iloc[0]
    
    processor_tier = match["Processor Tier"]
    gpu_tier = match["GPU Tier"]
    cpu_gpu_combo = f"{processor_tier}_{gpu_tier}"
    # =====================================================
    # CREATE INPUT DATAFRAME
    # =====================================================
    classification_df = pd.DataFrame([{

    "Brand": data.brand,

    "Processor": match["Processor"],

    "Graphic Processor": match["Graphic Processor"],

    "Capacity": data.capacity,

    "RAM Type": data.ram_type,

    "RAM Speed": match["RAM Speed"],

    "SSD Capacity": data.ssd_capacity,

    "SSD Type": match["SSD Type"],

    "Graphics Memory": data.graphics_memory,

    "Battery Capacity": data.battery_capacity,

    "Battery Type": data.battery_type,

    "Weight": data.weight,

    "Warranty": data.warranty,

    "Wi-Fi Version": match["Wi-Fi Version"],

    "Bluetooth Version": match["Bluetooth Version"],

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier,

    "CPU_GPU_Combo": cpu_gpu_combo

}])
    predicted_category = classification_model.predict(
    classification_df
).flatten()[0]
    input_df = pd.DataFrame([{

    "Brand": data.brand,

    "Processor": match["Processor"],

    "Graphic Processor": match["Graphic Processor"],

    "Capacity": data.capacity,

    "RAM Type": data.ram_type,

    "RAM Speed": match["RAM Speed"],

    "SSD Capacity": data.ssd_capacity,

    "SSD Type": match["SSD Type"],

    "Graphics Memory": data.graphics_memory,

    "Battery Capacity": data.battery_capacity,

    "Battery Type": data.battery_type,

    "Weight": data.weight,

    "Warranty": data.warranty,

    "Wi-Fi Version": match["Wi-Fi Version"],

    "Bluetooth Version": match["Bluetooth Version"],

    "Category": predicted_category,

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier

}])
    # =====================================================
    # DEBUG
    # =====================================================

    print(input_df.T)
    print("\n========== MATCH FOUND ==========\n")
    print(match.T)
    # =====================================================
    # PREDICT
    # =====================================================

    predicted_log_price = price_model.predict(input_df)[0]

    predicted_price = float(
        np.expm1(predicted_log_price)
    )

    return PricePredictionResponse(
        predicted_price=round(
            predicted_price,
            2
        ),predicted_category=predicted_category
    )