import pandas as pd
import numpy as np
import joblib
import optuna

from sklearn.model_selection import (
    train_test_split,
    KFold
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from category_encoders import TargetEncoder
from xgboost import XGBRegressor

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "laptop_dataset_with_tiers.csv"
)

# =====================================================
# TARGET
# =====================================================

X = df.drop(
    "Price (Rs)",
    axis=1
)

y = np.log1p(
    df["Price (Rs)"]
)

# =====================================================
# SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================================
# COLUMNS
# =====================================================

onehot_cols = [
    "Brand",
    "RAM Type",
    "SSD Type",
    "Wi-Fi Version",
    "Bluetooth Version",
    "Battery Type",
    "Category",
    "Processor Tier",
    "GPU Tier"
]

target_cols = [
    "Processor",
    "Graphic Processor"
]

# =====================================================
# OPTUNA OBJECTIVE
# =====================================================

def objective(trial):

    params = {

        "n_estimators": trial.suggest_int(
            "n_estimators",
            300,
            2500
        ),

        "max_depth": trial.suggest_int(
            "max_depth",
            3,
            12
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.01,
            0.3,
            log=True
        ),

        "min_child_weight": trial.suggest_int(
            "min_child_weight",
            1,
            10
        ),

        "subsample": trial.suggest_float(
            "subsample",
            0.5,
            1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree",
            0.5,
            1.0
        ),

        "gamma": trial.suggest_float(
            "gamma",
            0,
            5
        ),

        "reg_alpha": trial.suggest_float(
            "reg_alpha",
            0,
            5
        ),

        "reg_lambda": trial.suggest_float(
            "reg_lambda",
            0,
            10
        ),

        "objective": "reg:squarederror",
        "random_state": 42,
        "n_jobs": -1
    }

    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scores = []

    for train_idx, valid_idx in cv.split(X_train):

        X_tr = X_train.iloc[train_idx].copy()
        X_val = X_train.iloc[valid_idx].copy()

        y_tr = y_train.iloc[train_idx]
        y_val = y_train.iloc[valid_idx]

        encoder = TargetEncoder(
            cols=target_cols
        )

        X_tr[target_cols] = encoder.fit_transform(
            X_tr[target_cols],
            y_tr
        )

        X_val[target_cols] = encoder.transform(
            X_val[target_cols]
        )

        X_tr = pd.get_dummies(
            X_tr,
            columns=onehot_cols,
            dtype=int
        )

        X_val = pd.get_dummies(
            X_val,
            columns=onehot_cols,
            dtype=int
        )

        X_tr, X_val = X_tr.align(
            X_val,
            join="left",
            axis=1,
            fill_value=0
        )

        model = XGBRegressor(
            **params
        )

        model.fit(
            X_tr,
            y_tr
        )

        pred = model.predict(
            X_val
        )

        scores.append(
            r2_score(
                y_val,
                pred
            )
        )

    return np.mean(scores)

# =====================================================
# OPTUNA
# =====================================================

study = optuna.create_study(
    direction="maximize"
)

study.optimize(
    objective,
    n_trials=100,
    show_progress_bar=True
)

# =====================================================
# FINAL ENCODING
# =====================================================

encoder = TargetEncoder(
    cols=target_cols
)

X_train[target_cols] = encoder.fit_transform(
    X_train[target_cols],
    y_train
)

X_test[target_cols] = encoder.transform(
    X_test[target_cols]
)

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

X_train, X_test = X_train.align(
    X_test,
    join="left",
    axis=1,
    fill_value=0
)

# =====================================================
# FINAL MODEL
# =====================================================

best_model = XGBRegressor(
    **study.best_params,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

best_model.fit(
    X_train,
    y_train
)

# =====================================================
# SAVE FILES
# =====================================================

joblib.dump(
    best_model,
    "xgboost_optuna_best.pkl"
)

joblib.dump(
    encoder,
    "target_encoder.pkl"
)

joblib.dump(
    X_train.columns.tolist(),
    "feature_columns.pkl"
)

# =====================================================
# EVALUATION
# =====================================================

pred_log = best_model.predict(
    X_test
)

pred = np.expm1(
    pred_log
)

actual = np.expm1(
    y_test
)

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

# =====================================================
# RESULTS
# =====================================================

print("\n========== XGBOOST RESULTS ==========")

print("\nBest Parameters:")
print(study.best_params)

print(
    f"\nBest CV R²: {study.best_value:.4f}"
)

print(f"\nMAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")

print("\nSaved Files:")
print("xgboost_optuna_best.pkl")
print("target_encoder.pkl")
print("feature_columns.pkl")