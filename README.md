# Laptop Market Intelligence

A production-ready Machine Learning platform that predicts laptop prices, classifies laptops into market segments, recommends similar devices, and provides explainable AI insights using SHAP and LIME.

The project is built using FastAPI, PostgreSQL, Streamlit, CatBoost, and Scikit-learn, following a modular backend architecture and a modern frontend dashboard.

---

## Features

### Price Prediction

- Predicts laptop prices using a trained CatBoost regression model.
- Accepts detailed laptop specifications.
- Returns estimated market price.

### Laptop Classification

- Predicts the laptop category using a CatBoost classification model.

Example categories include:

- Gaming
- Ultrabook
- Business
- Creator
- Student

### Laptop Recommendation

- Finds similar laptops using a K-Nearest Neighbors recommendation engine.
- Uses engineered hardware features for similarity matching.

### Explainable AI

