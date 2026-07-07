import pandas as pd
from database.crud import get_prediction
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.crud import delete_recommendations
from database.database import get_db
from database.crud import (
    
    save_recommendations
)
from api.schemas import (
    Recommendation,
    RecommendationResponse
)

from api.dependencies import (
    recommendation_model,
    recommendation_scaler,
    recommendation_feature_columns,
    recommendation_dataset,
   
)
from api.feature_engineering import (
    get_processor_tier,
    get_gpu_tier,
    normalize_gpu
)


router = APIRouter()

# =====================================================
# COMPUTE FEATURES
# =====================================================

    
@router.post("/{prediction_id}")
def recommend_laptops(

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
    # FIND MATCH IN DATASET
    # =====================================================
    processor = prediction.processor
    
    gpu = normalize_gpu(
    
        prediction.graphic_processor
    
    )
    
    processor_tier = get_processor_tier(
    
        processor
    
    )
    
    gpu_tier = get_gpu_tier(
    
        gpu
    
    )
    
    
    
   

   

    # =====================================================
    # CREATE INPUT
   
    input_df = pd.DataFrame([{

    "Brand": prediction.brand,

    "Processor Tier": processor_tier,

    "GPU Tier": gpu_tier,

    "Category": prediction.predicted_category,

    "Capacity": prediction.capacity,

    "SSD Capacity": prediction.ssd_capacity,

    "Graphics Memory": prediction.graphics_memory,

    "Weight": prediction.weight,

    "Battery Capacity": prediction.battery_capacity

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
   
    
    delete_recommendations(

    db,

    prediction_id

    )
    
    save_recommendations(
    
        db=db,
    
        prediction_id=prediction_id,
    
        recommendations=recommendations
    
    )
   
    return RecommendationResponse(
        recommendations=recommendations
    )