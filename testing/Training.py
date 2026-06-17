import pandas as pd
import numpy as np
import joblib
import optuna
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from category_encoders import TargetEncoder
from xgboost import XGBRegressor

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("laptop_dataset_reduced.csv")

y = df["Price (Rs)"]
X = df.drop("Price (Rs)", axis=1)

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

X_train, X_test = X_train.align(
    X_test,
    join="outer",
    axis=1,
    fill_value=0
)

# =====================================================
# TARGET ENCODING
# =====================================================

target_cols = [
    "Processor",
    "Graphic Processor"
]

encoder = TargetEncoder(cols=target_cols)

X_train[target_cols] = encoder.fit_transform(
    X_train[target_cols],
    y_train
)

X_test[target_cols] = encoder.transform(
    X_test[target_cols]
)

# =====================================================
# FORCE NUMERIC
# =====================================================

X_train = X_train.apply(pd.to_numeric, errors="coerce").fillna(0)
X_test = X_test.apply(pd.to_numeric, errors="coerce").fillna(0)

X_train = X_train.astype(np.float32)
X_test = X_test.astype(np.float32)

# =====================================================
# SAVE PREPROCESSING FILES
# =====================================================

joblib.dump(
    encoder,
    "target_encoder.pkl"
)

joblib.dump(
    X_train.columns.tolist(),
    "feature_columns.pkl"
)

# =====================================================
# OPTUNA
# =====================================================

def objective(trial):

    params = {
        "n_estimators": trial.suggest_int(
            "n_estimators", 300, 2000
        ),

        "max_depth": trial.suggest_int(
            "max_depth", 3, 15
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.01,
            0.3,
            log=True
        ),

        "min_child_weight": trial.suggest_int(
            "min_child_weight", 1, 10
        ),

        "subsample": trial.suggest_float(
            "subsample", 0.5, 1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree", 0.5, 1.0
        ),

        "gamma": trial.suggest_float(
            "gamma", 0, 5
        ),

        "reg_alpha": trial.suggest_float(
            "reg_alpha", 0, 5
        ),

        "reg_lambda": trial.suggest_float(
            "reg_lambda", 0, 10
        ),

        "random_state": 42,
        "n_jobs": -1
    }

    model = XGBRegressor(**params)

    model.fit(
        X_train,
        y_train
    )

    pred = model.predict(X_test)

    return r2_score(
        y_test,
        pred
    )

study = optuna.create_study(
    direction="maximize"
)

study.optimize(
    objective,
    n_trials=100,
    show_progress_bar=True
)

# =====================================================
# FINAL MODEL
# =====================================================

best_model = XGBRegressor(
    **study.best_params,
    random_state=42,
    n_jobs=-1
)

best_model.fit(
    X_train,
    y_train
)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    best_model,
    "xgboost_optuna_best.pkl"
)

# =====================================================
# EVALUATION
# =====================================================

pred = best_model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        pred
    )
)

r2 = r2_score(
    y_test,
    pred
)

print("\n========== FINAL RESULTS ==========")
print(f"MAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")



