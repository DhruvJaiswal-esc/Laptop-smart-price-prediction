import pandas as pd
import numpy as np
import joblib

from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("laptop_dataset_reduced.csv")

# Log-transform target
y = np.log1p(df["Price (Rs)"])

X = df.drop("Price (Rs)", axis=1)

# ==========================================
# CATEGORICAL FEATURES
# ==========================================

cat_features = [
    "Brand",
    "Processor",
    "Graphic Processor",
    "RAM Type",
    "SSD Type",
    "Wi-Fi Version",
    "Bluetooth Version",
    "Battery Type",
    "Category"
]

for col in cat_features:
    X[col] = X[col].astype(str)

cat_feature_indices = [
    X.columns.get_loc(col)
    for col in cat_features
]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# CATBOOST
# ==========================================

model = CatBoostRegressor(
    iterations=1000,
    depth=8,
    learning_rate=0.05,
    loss_function="RMSE",
    verbose=100,
    random_seed=42
)

model.fit(
    X_train,
    y_train,
    cat_features=cat_feature_indices
)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "catboost_model.pkl"
)

# ==========================================
# PREDICT
# ==========================================

pred_log = model.predict(X_test)

# Convert back from log scale
pred = np.expm1(pred_log)
actual = np.expm1(y_test)

# ==========================================
# METRICS
# ==========================================

mae = mean_absolute_error(
    actual,
    pred
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        pred
    )
)

r2 = r2_score(
    actual,
    pred
)

print("\n========== RESULTS ==========")
print(f"MAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")

print("\nSaved:")
print("catboost_model.pkl")