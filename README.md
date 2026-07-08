# 💻 Laptop Market Intelligence

<div align="center">

### Intelligent Laptop Price Prediction, Recommendation & Explainable AI Platform

A full-stack Machine Learning application that predicts laptop prices, classifies laptops into market segments, recommends similar devices, and explains every prediction using modern Explainable AI techniques.

Built with **FastAPI**, **CatBoost**, **PostgreSQL**, **Streamlit**, **Docker**, and deployed on **Render**.

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Deployed-2496ED?style=for-the-badge&logo=docker)

</div>

---

# ✨ Overview

Laptop Market Intelligence is an end-to-end Machine Learning platform designed to estimate laptop prices based on hardware specifications while providing intelligent recommendations and transparent AI explanations.

Unlike a traditional prediction model, this project combines multiple Machine Learning models with Explainable AI and a modern web interface to deliver a complete decision-support system.

---

# 🚀 Features

## 💰 Laptop Price Prediction

Estimate the market value of a laptop using a trained CatBoost Regression model.

✔ High accuracy predictions

✔ Feature engineered inputs

✔ Real-time inference

---

## 🏷 Laptop Classification

Automatically classify laptops into different market categories.

Examples include:

- 🎮 Gaming
- 💼 Business
- 🎓 Student
- ✈️ Ultrabook
- 🎨 Creator

---

## 🔍 Smart Laptop Recommendation

Find laptops with similar hardware configurations using a K-Nearest Neighbors recommendation engine.

Features include:

- Hardware similarity search
- Intelligent feature engineering
- Multiple recommendations
- Fast nearest-neighbor lookup

---

## 🧠 Explainable AI

Every prediction is accompanied by detailed model explanations.

Implemented using:

- SHAP
- LIME

Understand:

- Why the price was predicted
- Which hardware components affected the prediction
- Positive feature contributions
- Negative feature contributions

---



## 🗄 PostgreSQL Integration

Every prediction is securely stored inside PostgreSQL, including:

- Prediction data
- Recommendations
- Explainability results

---

# 🛠 Tech Stack

## 🖥 Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- psycopg2

---

## 🤖 Machine Learning

- CatBoost
- Scikit-Learn
- SHAP
- LIME
- Pandas
- NumPy

---

## 🎨 Frontend

- Streamlit
- Plotly
- Requests
- Pillow

---

## ☁ Deployment

- Docker
- Render
- PostgreSQL (Render)

---

# ⚙ Machine Learning Workflow

```text
Laptop Specifications
          │
          ▼
Feature Engineering
          │
          ▼
Category Classification
          │
          ▼
Price Prediction
          │
     ┌────┴────┐
     ▼         ▼
Recommendation  Explainability
```

---

# 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /prediction` | Predict laptop price and category |
| `POST /recommendation/{prediction_id}` | Generate similar laptop recommendations |
| `POST /explainability/{prediction_id}` | Generate SHAP, LIME |
| `GET /insights` | Dataset insights |

---

# 🖥 Running Locally

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Laptop-Market-Intelligence.git

cd Laptop-Market-Intelligence
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Backend

```bash
uvicorn api.main:app --reload
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
cd frontend

pip install -r requirements.txt

streamlit run app.py
```

---

# 🔑 Environment Variables

## Backend

```env
DATABASE_URL=postgresql://username:password@host:5432/database
```

---

## Frontend

```env
API_BASE_URL=https://your-backend.onrender.com
```

---

# 🐳 Docker

Build Docker Image

```bash
docker build -t laptop-market-intelligence .
```

Run Container

```bash
docker run -p 8000:8000 laptop-market-intelligence
```

---

# ☁ Deployment

The project is designed for cloud deployment using:

- 🚀 Render Web Service (Backend)
- 🎨 Render Web Service (Frontend)
- 🗄 Render PostgreSQL
- 🐳 Docker

---

# 📊 Project Highlights

✅ End-to-End Machine Learning Application

✅ Modern FastAPI Backend

✅ Professional Streamlit Dashboard

✅ Explainable AI using SHAP & LIME

✅ PostgreSQL Database Integration

✅ Dockerized Deployment

✅ Production Ready

---

# 🔮 Future Enhancements

- 🔍 Semantic Laptop Search
- 👤 User Authentication
- 📈 Price Trend Analysis
- 📊 Interactive Analytics Dashboard
- 🔄 Continuous Model Retraining
- ⚡ CI/CD with GitHub Actions
- 📱 Mobile Responsive Dashboard
- ☁ Multi-Cloud Deployment Support

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to improve the project:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Dhruv Jaiswal

**B.Tech CSE (Artificial Intelligence & Machine Learning)**

K.R. Mangalam University

GitHub: https://github.com/Dhruv-Jaiswalesc



---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a Star!

</div>
