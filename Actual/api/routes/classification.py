import pandas as pd

from fastapi import APIRouter

from api.dependencies import (
    classification_model,
    laptop_dataset
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
    # FIND MATCH IN DATASET
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

        "Processor Tier": processor_tier,

        "GPU Tier": gpu_tier,
        "CPU_GPU_Combo": cpu_gpu_combo

    }])

    # =====================================================
    # DEBUG
    # =====================================================

    print("\n========== MATCH ==========\n")
    print(match.T)

    print("\n========== INPUT ==========\n")
    print(input_df.T)
    print("\nColumns sent to model:")
    print(input_df.columns.tolist())
    
    print("\nNumber of columns:")
    print(len(input_df.columns))
    
    print("\nModel expects:")
    print(classification_model.feature_names_)

    # =====================================================
    # PREDICT
    # =====================================================

    prediction = classification_model.predict(input_df)

    predicted_category = prediction.flatten()[0]

    return ClassificationResponse(
        predicted_category=predicted_category
    )