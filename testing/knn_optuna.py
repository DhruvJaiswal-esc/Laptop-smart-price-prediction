import pandas as pd
import numpy as np
import joblib
import optuna

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from category_encoders import TargetEncoder

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
# NUMERIC
# =====================================================

X_train = X_train.apply(pd.to_numeric, errors="coerce").fillna(0)
X_test = X_test.apply(pd.to_numeric, errors="coerce").fillna(0)

# =====================================================
# SCALING
# =====================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =====================================================
# OPTUNA
# =====================================================

def objective(trial):

    model = KNeighborsRegressor(
        n_neighbors=trial.suggest_int(
            "n_neighbors",
            3,
            25
        ),
        weights=trial.suggest_categorical(
            "weights",
            ["uniform", "distance"]
        ),
        p=trial.suggest_int(
            "p",
            1,
            2
        )
    )

    model.fit(X_train, y_train)

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
    n_trials=50,
    show_progress_bar=True
)

# =====================================================
# FINAL MODEL
# =====================================================

model = KNeighborsRegressor(
    **study.best_params
)

model.fit(
    X_train,
    y_train
)

pred = model.predict(X_test)

# =====================================================
# SAVE
# =====================================================

joblib.dump(
    model,
    "knn.pkl"
)

joblib.dump(
    scaler,
    "knn_scaler.pkl"
)

# =====================================================
# METRICS
# =====================================================

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

print("\n========== RESULTS ==========")
print("Best Params:", study.best_params)
print(f"MAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")