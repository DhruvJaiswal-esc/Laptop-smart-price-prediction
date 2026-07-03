
import joblib
from fastapi import FastAPI

from sentence_transformers import SentenceTransformer
import pandas as pd

laptop_dataset = pd.read_csv(
    "data/processed/laptop_dataset_enhanced.csv"
)


price_model = joblib.load(
    "trained_models/regression/catboost.pkl"
)

classification_model = joblib.load(
    "trained_models/classification/classifier.pkl"
)

recommendation_model = joblib.load(
    "trained_models/recommendation/recommender.pkl"
)

recommendation_scaler = joblib.load(
    "trained_models/recommendation/scaler.pkl"
)


recommendation_features = joblib.load(
    "trained_models/recommendation/features.pkl"
)

recommendation_feature_columns = (
    recommendation_features.columns.tolist()
)
recommendation_dataset = joblib.load(
    "trained_models/recommendation/laptops.pkl"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

