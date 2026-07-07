

from api.routes.prediction import router as prediction_router
from api.routes.classification import router as classification_router
from api.routes.recommendation import router as recommendation_router
from api.routes.explainability import router as explainability_router
from api.routes.insights import router as insights_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import create_database
import database.models



app = FastAPI(
    title="Laptop Market Intelligence API",
    description="API for Laptop Price Prediction, Classification, Recommendation and Explainability",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =====================================================
# ROUTES
# =====================================================
@app.on_event("startup")
def startup():

    create_database()
app.include_router(
    prediction_router,
    prefix="/prediction",
    tags=["Price Prediction"]
)

app.include_router(
    classification_router,
    prefix="/classification",
    tags=["Classification"]
)

app.include_router(
    recommendation_router,
    prefix="/recommendation",
    tags=["Recommendation"]
)

app.include_router(
    explainability_router,
    prefix="/explainability",
    tags=["Explainability"]
)

app.include_router(
    insights_router,
    prefix="/insights",
    tags=["Market Insights"]
)

# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {

        "Project": "Laptop Market Intelligence",

        "Version": "1.0.0",

        "Status": "Running"

    }