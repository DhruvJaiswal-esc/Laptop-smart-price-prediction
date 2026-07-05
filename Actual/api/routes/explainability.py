import numpy as np
import pandas as pd
import pprint 
from fastapi import APIRouter

from api.schemas import (
    LaptopInput
)

from api.dependencies import (

    price_model,

    classification_model,

    laptop_dataset,

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

@router.post("/")
def explain_prediction(

    data: LaptopInput

):

    # =====================================================
    # NORMALIZE USER INPUT
    # =====================================================

    processor = data.processor

    gpu = normalize_gpu(

        data.graphic_processor

    )

    ssd_type = normalize_ssd(

        data.ssd_type

    )

    wifi = normalize_wifi(

        data.wi_fi_version

    )

    bluetooth = normalize_bluetooth(

        data.bluetooth_version

    )

    processor_tier = get_processor_tier(

        processor

    )

    gpu_tier = get_gpu_tier(

        gpu

    )

    cpu_gpu_combo = (

        f"{processor_tier}_{gpu_tier}"

    )

    # =====================================================
    # CLASSIFICATION INPUT
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

    # =====================================================
    # CATEGORY
    # =====================================================

    predicted_category = (

        classification_model

        .predict(

            classification_df

        )

        .flatten()[0]

    )
        # =====================================================
    # PRICE PREDICTION INPUT
    # =====================================================

    prediction_df = pd.DataFrame([{

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
    # PRICE PREDICTION
    # =====================================================

    predicted_log_price = price_model.predict(

        prediction_df

    )[0]

    predicted_price = float(

        np.expm1(

            predicted_log_price

        )

    )

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
    print("\n===== LIME PREDICTION =====")
    print(prediction_df.columns.tolist())
    print(len(prediction_df.columns))
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
        # =====================================================
    # RESPONSE
    # =====================================================

    response = {

    "prediction": {

        "predicted_price": round(
            predicted_price,
            2
        ),

        "predicted_category": predicted_category

    },

    "input": {

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

        "GPU Tier": gpu_tier

    },

    "shap": shap_result,

    "lime": lime_result,

    "report": report_path

}

    return response