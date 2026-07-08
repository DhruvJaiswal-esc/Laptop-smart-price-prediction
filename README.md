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

Generates model explanations using:

- SHAP feature importance
- LIME local explanations

### Report Generation

Automatically generates PDF reports containing:

- Input specifications
- Predicted price
- Predicted category
- SHAP explanation
- LIME explanation

### Persistent Storage

Stores:

- Prediction history
- Recommendation history
- Explainability reports

using PostgreSQL.

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg2
- Pydantic

## Machine Learning

- CatBoost
- Scikit-learn
- SHAP
- LIME
- Pandas
- NumPy

## Frontend

- Streamlit
- Plotly
- Requests

## Deployment

- Docker
- Render
- PostgreSQL (Render)

---


# Machine Learning Pipeline

```
Laptop Specifications
        │
        ▼
Feature Engineering
        │
        ▼
Classification Model
        │
        ▼
Predicted Category
        │
        ▼
Price Prediction Model
        │
        ▼
Predicted Price
        │
        ├──────────────► Recommendation Engine
        │
        └──────────────► SHAP + LIME Explainability
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Laptop-Market-Intelligence.git

cd Laptop-Market-Intelligence
```

---

## Backend

Install dependencies

```bash
pip install -r requirements.txt
```

Run the API

```bash
uvicorn api.main:app --reload
```

API Documentation

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

pip install -r requirements.txt

streamlit run app.py
```

---

# Environment Variables

## Backend

```
DATABASE_URL=<your_postgresql_connection_string>
```

Example

```
postgresql://postgres:password@localhost:5432/LaptopMarketIntelligence
```

---

## Frontend

```
API_BASE_URL=http://127.0.0.1:8000
```

Example for production

```
API_BASE_URL=https://your-backend.onrender.com
```

---

# Docker

Build

```bash
docker build -t laptop-market-intelligence .
```

Run

```bash
docker run -p 8000:8000 laptop-market-intelligence
```

---

# API Endpoints

## Prediction

```
POST /prediction
```

Predicts laptop price and category.

---

## Recommendation

```
POST /recommendation/{prediction_id}
```

Returns similar laptops.

---

## Explainability

```
POST /explainability/{prediction_id}
```

Generates SHAP and LIME explanations along with a PDF report.

---


# Deployment

The application is deployed using:

- Render Web Service (FastAPI Backend)
- Render PostgreSQL
- Render Web Service (Streamlit Frontend)
- Docker

---

# Future Improvements

- Semantic laptop search using Sentence Transformers
- User authentication
- Prediction history dashboard
- Advanced market analytics
- Price trend forecasting
- REST API versioning
- CI/CD pipeline with GitHub Actions
- Model monitoring and drift detection

---

# License

This project is licensed under the MIT License.

---

# Author

Dhruv Jaiswal

B.Tech Computer Science (Artificial Intelligence & Machine Learning)

K.R. Mangalam University

GitHub: https://github.com/Dhruv-Jaiswalesc



