
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def explain_model():

    return {

        "message": "SHAP and LIME explainability endpoint.",

        "status": "Coming Soon"

    }

