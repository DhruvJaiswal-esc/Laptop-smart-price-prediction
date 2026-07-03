import pandas as pd
import numpy as np
import joblib

from lime.lime_tabular import LimeTabularExplainer
from sklearn.model_selection import train_test_split

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("laptop_dataset_reduced.csv")

y = df["Price (Rs)"]
X = df.drop("Price (Rs)", axis=1)

# =====================================================
# SAME SPLIT USED DURING TRAINING
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================================
# LOAD SAVED FILES
# =====================================================

encoder = joblib.load("target_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")
model = joblib.load("xgboost_optuna_best.pkl")

# =====================================================
# ONE HOT ENCODING
# =====================================================

onehot_cols = [
    "Brand",
    "RAM Type",
    "SSD Type",
    "Wi-Fi Version",
    "Bluetooth Version",
    "Battery Type",
    "Category"
]

X_train = pd.get_dummies(
    X_train,
    columns=onehot_cols,
    dtype=int
)

X_test = pd.get_dummies(
    X_test,
    columns=onehot_cols,
    dtype=int
)

# =====================================================
# TARGET ENCODING
# =====================================================

target_cols = [
    "Processor",
    "Graphic Processor"
]

X_train[target_cols] = encoder.transform(
    X_train[target_cols]
)

X_test[target_cols] = encoder.transform(
    X_test[target_cols]
)

# =====================================================
# MATCH TRAINING FEATURES
# =====================================================

X_train = X_train.reindex(
    columns=feature_columns,
    fill_value=0
)

X_test = X_test.reindex(
    columns=feature_columns,
    fill_value=0
)

X_train = X_train.apply(
    pd.to_numeric,
    errors="coerce"
).fillna(0)

X_test = X_test.apply(
    pd.to_numeric,
    errors="coerce"
).fillna(0)

X_train = X_train.astype(np.float32)
X_test = X_test.astype(np.float32)

# =====================================================
# CREATE LIME EXPLAINER
# =====================================================

explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X_train.columns.tolist(),
    mode="regression",
    random_state=42
)

# =====================================================
# EXPLAIN ONE LAPTOP
# =====================================================

idx = 0

prediction = model.predict(
    X_test.iloc[[idx]]
)[0]

print(f"\nPredicted Price: Rs {prediction:,.0f}")

exp = explainer.explain_instance(
    X_test.iloc[idx].values,
    model.predict,
    num_features=10
)

# =====================================================
# SAVE OUTPUT
# =====================================================

exp.save_to_file(
    "lime_explanation.html"
)

print("\nSaved Successfully:")
print("lime_explanation.html")

# Print explanation in terminal

print("\nTop Factors:")

for feature, weight in exp.as_list():
    print(f"{feature} : {weight:.4f}")