import pandas as pd

from fastapi import APIRouter

from api.schemas import (
    LaptopInput,
    Recommendation,
    RecommendationResponse
)

from api.dependencies import (
    recommendation_model,
    recommendation_scaler,
    recommendation_feature_columns,
    recommendation_dataset,
    classification_model
)
from api.feature_engineering import (
    get_processor_tier,
    get_gpu_tier,
    normalize_gpu
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
# COMPUTE FEATURES
# =====================================================

    
@router.post(
    "/",
    response_model=RecommendationResponse
)
def recommend_laptops(data: LaptopInput):

    # =====================================================
    # FIND MATCH IN DATASET
    # =====================================================
    processor = data.processor
    gpu = normalize_gpu(data.graphic_processor)
    
    processor_tier = get_processor_tier(processor)
    
    gpu_tier = get_gpu_tier(gpu)
    
    cpu_gpu_combo = f"{processor_tier}_{gpu_tier}"

   

   

    # =====================================================
    # CREATE INPUT
    classification_df = pd.DataFrame([{

    "Brand": data.brand,

    "Processor": processor,

    "Graphic Processor": gpu,

    "Capacity": data.capacity,

    "RAM Type": data.ram_type,

    "RAM Speed": data.ram_speed,

    "SSD Capacity": data.ssd_capacity,

    "SSD Type": normalize_ssd(data.ssd_type),

    "Graphics Memory": data.graphics_memory,

    "Battery Capacity": data.battery_capacity,

    "Battery Type": data.battery_type,

    "Weight": data.weight,

    "Warranty": data.warranty,

    "Wi-Fi Version": normalize_wifi(data.wi_fi_version),

    "Bluetooth Version": normalize_bluetooth(data.bluetooth_version),

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier,

    "CPU_GPU_Combo": cpu_gpu_combo

}])
    predicted_category = classification_model.predict(
    classification_df
    ).flatten()[0]
    input_df = pd.DataFrame([{

        "Brand": data.brand,

        "Processor Tier": processor_tier,

        "GPU Tier": gpu_tier,
        "Category": predicted_category,


        "Capacity": data.capacity,

        "SSD Capacity": data.ssd_capacity,

        "Graphics Memory": data.graphics_memory,

        "Weight": data.weight,

        "Battery Capacity": data.battery_capacity

    }])

    input_df = pd.get_dummies(
        input_df,
        dtype=int
    )

    input_df = input_df.reindex(
        columns=recommendation_feature_columns,
        fill_value=0
    )

    input_scaled = recommendation_scaler.transform(
        input_df
    )

    distances, indices = recommendation_model.kneighbors(
        input_scaled
    )

    recommendations = []

    for idx in indices[0][1:]:

        laptop = recommendation_dataset.iloc[idx]

        recommendations.append(

            Recommendation(

                brand=laptop["Brand"],

                processor=laptop["Processor"],

                graphic_processor=laptop["Graphic Processor"],

                category=laptop["Category"]

            )

        )

    return RecommendationResponse(
        recommendations=recommendations
    )