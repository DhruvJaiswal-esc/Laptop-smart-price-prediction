import pandas as pd
import numpy as np
import joblib
import optuna

from catboost import CatBoostRegressor, Pool

from sklearn.model_selection import (
    train_test_split,
    KFold
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("laptop_dataset_with_tiers.csv")

# =====================================================
# FEATURES / TARGET
# =====================================================

X = df.drop("Price (Rs)", axis=1)
y = np.log1p(df["Price (Rs)"])

# =====================================================
# CATEGORICAL FEATURES
# =====================================================

cat_features = [
    "Brand", "Processor", "Graphic Processor", "Processor Tier",
    "GPU Tier", "RAM Type", "SSD Type", "Wi-Fi Version",
    "Bluetooth Version", "Battery Type", "Category"
]

for col in cat_features:
    X[col] = X[col].astype(str)

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================================
# CAT FEATURE INDICES
# =====================================================

cat_feature_indices = [
    X_train.columns.get_loc(col) for col in cat_features
]

# =====================================================
# OPTUNA OBJECTIVE
# =====================================================

def objective(trial):

    params = {
        "iterations": trial.suggest_int("iterations", 1000, 4000),
        "depth": trial.suggest_int("depth", 4, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 20),
        
        # Optimized GPU parameters
        "border_count": 64, 
        "max_ctr_complexity": 1, 
        
        "loss_function": "RMSE",
        "random_seed": 42,
        "task_type": "GPU",
        "devices": "0",
        "verbose": False
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = []

    for train_idx, valid_idx in cv.split(X_train):

        X_tr = X_train.iloc[train_idx]
        X_val = X_train.iloc[valid_idx]

        y_tr = y_train.iloc[train_idx]
        y_val = y_train.iloc[valid_idx]

        # Use GPU Pool processing to skip Pandas-to-C++ translation overhead
        train_pool = Pool(X_tr, y_tr, cat_features=cat_feature_indices)
        valid_pool = Pool(X_val, y_val, cat_features=cat_feature_indices)

        model = CatBoostRegressor(**params)

        model.fit(
            train_pool, 
            eval_set=valid_pool,
            early_stopping_rounds=30, 
            verbose=False
        )

        pred = model.predict(valid_pool)
        score = r2_score(y_val, pred)
        scores.append(score)

    return np.mean(scores)

# =====================================================
# OPTUNA STUDY
# =====================================================

study = optuna.create_study(direction="maximize")

study.optimize(
    objective,
    n_trials=100,
    # [FIX] Set to 1 to prevent multiple threads from locking GPU 0 simultaneously
    n_jobs=1, 
    show_progress_bar=True
)

# =====================================================
# FINAL MODEL
# =====================================================

full_train_pool = Pool(X_train, y_train, cat_features=cat_feature_indices)

best_model = CatBoostRegressor(
    **study.best_params,
    border_count=64,             
    max_ctr_complexity=1,        
    loss_function="RMSE",
    random_seed=42,
    task_type="GPU",
    devices="0",
    verbose=100
)

best_model.fit(full_train_pool)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(best_model, "catboost_model_gpu.pkl")

# =====================================================
# PREDICTIONS
# =====================================================

pred_log = best_model.predict(X_test)
pred = np.expm1(pred_log)
actual = np.expm1(y_test)

# =====================================================
# METRICS
# =====================================================

mae = mean_absolute_error(actual, pred)
rmse = np.sqrt(mean_squared_error(actual, pred))
r2 = r2_score(actual, pred)

# =====================================================
# RESULTS
# =====================================================

print("\n========== CATBOOST RESULTS ==========")

print("\nBest Parameters:")
print(study.best_params)

print(f"\nBest CV R²: {study.best_value:.4f}")

print(f"\nMAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")

print("\nSaved:")
print("catboost_model_gpu.pkl")