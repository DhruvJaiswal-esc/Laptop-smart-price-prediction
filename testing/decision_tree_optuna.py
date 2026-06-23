import pandas as pd
import numpy as np
import joblib
import optuna

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
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
# ENCODING
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

X_train = pd.get_dummies(X_train, columns=onehot_cols, dtype=int)
X_test = pd.get_dummies(X_test, columns=onehot_cols, dtype=int)

X_train, X_test = X_train.align(
    X_test,
    join="outer",
    axis=1,
    fill_value=0
)

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
# OPTUNA
# =====================================================

def objective(trial):

    model = DecisionTreeRegressor(
        max_depth=trial.suggest_int(
            "max_depth",
            3,
            40
        ),
        min_samples_split=trial.suggest_int(
            "min_samples_split",
            2,
            20
        ),
        min_samples_leaf=trial.suggest_int(
            "min_samples_leaf",
            1,
            10
        ),
        random_state=42
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
    n_trials=50
)

# =====================================================
# FINAL MODEL
# =====================================================

model = DecisionTreeRegressor(
    **study.best_params,
    random_state=42
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
    "decision_tree.pkl"
)

# =====================================================
# RESULTS
# =====================================================

print("Best Params:", study.best_params)

print(
    "R²:",
    r2_score(
        y_test,
        pred
    )
)