import pandas as pd

from fastapi import APIRouter

from api.dependencies import (
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

from api.schemas import (
    LaptopInput,
    ClassificationResponse
)

router = APIRouter()

# =====================================================
# CLASSIFICATION
# =====================================================

@router.post(
    "/",
    response_model=ClassificationResponse
)
def classify_laptop(data: LaptopInput):

    # =====================================================
    # COMPUTE FEATURES
    # =====================================================
    
    processor = data.processor
    
    gpu = normalize_gpu(data.graphic_processor)
    
    ssd_type = normalize_ssd(data.ssd_type)
    
    wifi = normalize_wifi(data.wi_fi_version)
    
    bluetooth = normalize_bluetooth(data.bluetooth_version)
    
    processor_tier = get_processor_tier(processor)
    
    gpu_tier = get_gpu_tier(gpu)
    
    cpu_gpu_combo = f"{processor_tier}_{gpu_tier}"

    # =====================================================
    # CREATE INPUT DATAFRAME
    # =====================================================

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

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier,

    "CPU_GPU_Combo": cpu_gpu_combo

}])

    # =====================================================
    # DEBUG
    # =====================================================
    print("\n========== CLASSIFICATION INPUT ==========\n")
    print(input_df.T)

    # =====================================================
    # PREDICT
    # =====================================================

    prediction = classification_model.predict(input_df)

    predicted_category = prediction.flatten()[0]

    return ClassificationResponse(
        predicted_category=predicted_category
    )