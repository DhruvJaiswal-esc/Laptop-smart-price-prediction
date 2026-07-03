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
    laptop_dataset
)

router = APIRouter()


@router.post(
    "/",
    response_model=RecommendationResponse
)
def recommend_laptops(data: LaptopInput):

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

    # =====================================================
    # CREATE INPUT
    # =====================================================

    input_df = pd.DataFrame([{

        "Brand": data.brand,

        "Processor Tier": processor_tier,

        "GPU Tier": gpu_tier,

        "Category": data.category,

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