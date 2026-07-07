import pandas as pd
import numpy as np
import joblib

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/laptop_dataset_enhanced.csv"
)

# =====================================================
# FEATURES / TARGET
# =====================================================

X = df.drop(
    ["Price (Rs)", "Category"],
    axis=1
)

y = df["Category"]

# =====================================================
# CPU GPU COMBO
# =====================================================

X["CPU_GPU_Combo"] = (
    X["Processor Tier"].astype(str)
    + "_"
    + X["GPU Tier"].astype(str)
)

# =====================================================
# CATEGORICAL FEATURES
# =====================================================

cat_features = [

    "Brand",

    "Processor",
    "Processor Tier",

    "Graphic Processor",
    "GPU Tier",

    "CPU_GPU_Combo",

    "RAM Type",
    "SSD Type",

    "Wi-Fi Version",
    "Bluetooth Version",

    "Battery Type"

    ]

for col in cat_features:
    X[col] = X[col].astype(str)

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================================
# CAT FEATURE INDICES
# =====================================================

cat_feature_indices = [
    X_train.columns.get_loc(col)
    for col in cat_features
]

# =====================================================
# MODEL
# =====================================================

model = CatBoostClassifier(

    iterations=2000,
    depth=8,
    learning_rate=0.05,

    loss_function="MultiClass",

    auto_class_weights="Balanced",

    task_type="GPU",
    devices="0",

    random_seed=42,

    verbose=100
)

# =====================================================
# TRAIN
# =====================================================

model.fit(

    X_train,
    y_train,

    cat_features=cat_feature_indices,

    eval_set=(X_test, y_test),

    early_stopping_rounds=100
)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    "trained_models/classification/classifier.pkl"
)

# =====================================================
# PREDICTIONS
# =====================================================

pred = model.predict(X_test)

pred = pred.flatten()

# =====================================================
# METRICS
# =====================================================

accuracy = accuracy_score(
    y_test,
    pred
)

weighted_f1 = f1_score(
    y_test,
    pred,
    average="weighted"
)

# =====================================================
# RESULTS
# =====================================================

print("\n========== CLASSIFICATION RESULTS ==========")

print(f"\nAccuracy     : {accuracy:.4f}")
print(f"Weighted F1  : {weighted_f1:.4f}")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        pred
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        pred
    )
)

print("\nSaved:")

print(
    "trained_models/classification/classifier.pkl"
)