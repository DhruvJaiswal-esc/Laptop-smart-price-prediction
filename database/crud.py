from sqlalchemy.orm import Session
import json
from database.models import (
    PredictionHistory,
    ExplainabilityHistory,
    RecommendationHistory
)


# =====================================================
# PREDICTION CRUD
# =====================================================

def save_prediction(

    db: Session,

    data,

    predicted_price: float,

    predicted_category: str

):

    prediction = PredictionHistory(

        brand=data.brand,

        processor=data.processor,

        graphic_processor=data.graphic_processor,

        capacity=data.capacity,

        ram_type=data.ram_type,

        ram_speed=data.ram_speed,

        ssd_capacity=data.ssd_capacity,

        ssd_type=data.ssd_type,

        graphics_memory=data.graphics_memory,

        battery_capacity=data.battery_capacity,

        battery_type=data.battery_type,

        weight=data.weight,

        warranty=data.warranty,

        wifi_version=data.wi_fi_version,

        bluetooth_version=data.bluetooth_version,

        predicted_category=predicted_category,

        predicted_price=float(predicted_price)

    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return prediction


# =====================================================
# GET ONE PREDICTION
# =====================================================

def get_prediction(

    db: Session,

    prediction_id: int

):

    return (

        db.query(

            PredictionHistory

        )

        .filter(

            PredictionHistory.id == prediction_id

        )

        .first()

    )


# =====================================================
# GET ALL PREDICTIONS
# =====================================================

def get_prediction_history(

    db: Session

):

    return (

        db.query(

            PredictionHistory

        )

        .order_by(

            PredictionHistory.timestamp.desc()

        )

        .all()

    )


# =====================================================
# DELETE PREDICTION
# =====================================================

def delete_prediction(

    db: Session,

    prediction_id: int

):

    prediction = get_prediction(

        db,

        prediction_id

    )

    if prediction is None:

        return False

    db.delete(

        prediction

    )

    db.commit()

    return True


# =====================================================
# CLEAR HISTORY
# =====================================================

def clear_prediction_history(

    db: Session

):

    db.query(

        PredictionHistory

    ).delete()

    db.commit()

    return True
# =====================================================
# EXPLAINABILITY CRUD
# =====================================================


def save_explainability(

    db: Session,

    prediction_id: int,

    shap_result: dict,

    lime_result: dict,

    report_path: str

):

    explanation = ExplainabilityHistory(

        prediction_id=prediction_id,

        shap_json=json.dumps(

            shap_result,

            default=str

        ),

        lime_json=json.dumps(

            lime_result,

            default=str

        ),

        report_path=report_path

    )

    db.add(

        explanation

    )

    db.commit()

    db.refresh(

        explanation

    )

    return explanation


# =====================================================
# GET EXPLAINABILITY
# =====================================================

def get_explainability(

    db: Session,

    prediction_id: int

):

    return (

        db.query(

            ExplainabilityHistory

        )

        .filter(

            ExplainabilityHistory.prediction_id

            ==

            prediction_id

        )

        .first()

    )


# =====================================================
# DELETE EXPLAINABILITY
# =====================================================

def delete_explainability(

    db: Session,

    prediction_id: int

):

    explanation = get_explainability(

        db,

        prediction_id

    )

    if explanation is None:

        return False

    db.delete(

        explanation

    )

    db.commit()

    return True


# =====================================================
# UPDATE REPORT PATH
# =====================================================

def update_report_path(

    db: Session,

    prediction_id: int,

    report_path: str

):

    explanation = get_explainability(

        db,

        prediction_id

    )

    if explanation is None:

        return None

    explanation.report_path = report_path

    db.commit()

    db.refresh(

        explanation

    )

    return explanation


# =====================================================
# UPDATE SHAP
# =====================================================

def update_shap(

    db: Session,

    prediction_id: int,

    shap_result: dict

):

    explanation = get_explainability(

        db,

        prediction_id

    )

    if explanation is None:

        return None

    explanation.shap_json = json.dumps(

        shap_result,

        default=str

    )

    db.commit()

    db.refresh(

        explanation

    )

    return explanation


# =====================================================
# UPDATE LIME
# =====================================================

def update_lime(

    db: Session,

    prediction_id: int,

    lime_result: dict

):

    explanation = get_explainability(

        db,

        prediction_id

    )

    if explanation is None:

        return None

    explanation.lime_json = json.dumps(

        lime_result,

        default=str

    )

    db.commit()

    db.refresh(

        explanation

    )

    return explanation
# =====================================================
# RECOMMENDATION CRUD
# =====================================================

def save_recommendations(

    db: Session,

    prediction_id: int,

    recommendations

):

    saved_recommendations = []

    for recommendation in recommendations:

        recommendation_record = RecommendationHistory(

            prediction_id=prediction_id,

            brand=recommendation.brand,

            processor=recommendation.processor,

            graphic_processor=recommendation.graphic_processor,

            category=recommendation.category

        )

        db.add(

            recommendation_record

        )

        saved_recommendations.append(

            recommendation_record

        )

    db.commit()

    return saved_recommendations


# =====================================================
# GET RECOMMENDATIONS
# =====================================================

def get_recommendations(

    db: Session,

    prediction_id: int

):

    return (

        db.query(

            RecommendationHistory

        )

        .filter(

            RecommendationHistory.prediction_id

            ==

            prediction_id

        )

        .all()

    )


# =====================================================
# DELETE RECOMMENDATIONS
# =====================================================

def delete_recommendations(

    db: Session,

    prediction_id: int

):

    recommendations = get_recommendations(

        db,

        prediction_id

    )

    if not recommendations:

        return False

    for recommendation in recommendations:

        db.delete(

            recommendation

        )

    db.commit()

    return True


# =====================================================
# DELETE EVERYTHING
# =====================================================

def delete_prediction_complete(

    db: Session,

    prediction_id: int

):

    delete_recommendations(

        db,

        prediction_id

    )

    delete_explainability(

        db,

        prediction_id

    )

    return delete_prediction(

        db,

        prediction_id

    )


# =====================================================
# DATABASE STATISTICS
# =====================================================

def database_statistics(

    db: Session

):

    prediction_count = (

        db.query(

            PredictionHistory

        )

        .count()

    )

    explanation_count = (

        db.query(

            ExplainabilityHistory

        )

        .count()

    )

    recommendation_count = (

        db.query(

            RecommendationHistory

        )

        .count()

    )

    return {

        "predictions": prediction_count,

        "explanations": explanation_count,

        "recommendations": recommendation_count

    }


# =====================================================
# CLEAR ENTIRE DATABASE
# =====================================================

def clear_database(

    db: Session

):

    db.query(

        RecommendationHistory

    ).delete()

    db.query(

        ExplainabilityHistory

    ).delete()

    db.query(

        PredictionHistory

    ).delete()

    db.commit()

    return True