import pandas as pd
import joblib

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/laptop_dataset_enhanced.csv"
)

# =====================================================
# FEATURES FOR RECOMMENDATION
# =====================================================

features = df[[
    "Brand",

    "Processor Tier",
   

    "GPU Tier",
   


    "Category",

    "Capacity",

    "SSD Capacity",

    "Graphics Memory",

    "Weight",

    "Battery Capacity"
]].copy()

# =====================================================
# ONE HOT ENCODE CATEGORICALS
# =====================================================

categorical_cols = [
    "Brand",

    "Processor Tier",
   

    "GPU Tier",
   


    "Category"
]

features = pd.get_dummies(
    features,
    columns=categorical_cols,
    dtype=int
)

# =====================================================
# SCALE FEATURES
# =====================================================

scaler = StandardScaler()

features_scaled = scaler.fit_transform(
    features
)

# =====================================================
# RECOMMENDATION MODEL
# =====================================================

model = NearestNeighbors(
    n_neighbors=6,
    metric="cosine"
)

model.fit(features_scaled)

# =====================================================
# SAVE ARTIFACTS
# =====================================================

joblib.dump(
    model,
    "trained_models/recommendation/recommender.pkl"
)

joblib.dump(
    scaler,
    "trained_models/recommendation/scaler.pkl"
)

joblib.dump(
    features,
    "trained_models/recommendation/features.pkl"
)

joblib.dump(
    df,
    "trained_models/recommendation/laptops.pkl"
)

print("\nRecommendation Model Saved Successfully")

print("\nSaved Files:")

print("trained_models/recommendation/recommender.pkl")
print("trained_models/recommendation/scaler.pkl")
print("trained_models/recommendation/features.pkl")
print("trained_models/recommendation/laptops.pkl")

# =====================================================
# TEST RECOMMENDATION
# =====================================================

sample_index = 0

distances, indices = model.kneighbors(
    features_scaled[sample_index].reshape(1, -1)
)

print("\nSelected Laptop:\n")

print(
    df.iloc[sample_index][[
        "Brand",
        "Processor",
        "Graphic Processor",
        "Category"
    ]]
)

print("\nRecommended Laptops:\n")

for idx in indices[0][1:]:

    print(
        f"{df.iloc[idx]['Brand']} | "
        f"{df.iloc[idx]['Processor']} | "
        f"{df.iloc[idx]['Graphic Processor']} | "
        f"{df.iloc[idx]['Category']}"
    )