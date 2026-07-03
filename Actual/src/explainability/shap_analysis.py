import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("laptop_dataset_reduced.csv")

y = df["Price (Rs)"]
X = df.drop("Price (Rs)", axis=1)

# =====================================================
# SAME SPLIT AS TRAINING
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

X_test[target_cols] = encoder.transform(
    X_test[target_cols]
)

# =====================================================
# MATCH TRAINING FEATURES
# =====================================================

X_test = X_test.reindex(
    columns=feature_columns,
    fill_value=0
)

X_test = X_test.apply(
    pd.to_numeric,
    errors="coerce"
).fillna(0)

X_test = X_test.astype(np.float32)

# =====================================================
# FEATURE IMPORTANCE (ALWAYS WORKS)
# =====================================================

importance = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 20 Features")
print(importance.head(20))

importance.head(20).to_csv(
    "feature_importance.csv",
    index=False
)

# =====================================================
# SHAP
# =====================================================

print("\nGenerating SHAP plots...")

try:

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_test)

    # Summary Plot
    plt.figure()
    shap.summary_plot(
        shap_values,
        X_test,
        show=False
    )

    plt.tight_layout()
    plt.savefig(
        "shap_summary.png",
        dpi=300,
        bbox_inches="tight"
    )

    # Feature Importance Plot
    plt.figure()
    shap.summary_plot(
        shap_values,
        X_test,
        plot_type="bar",
        show=False
    )

    plt.tight_layout()
    plt.savefig(
        "shap_importance.png",
        dpi=300,
        bbox_inches="tight"
    )

    # Waterfall Example
    explanation = shap.Explanation(
        values=shap_values[0],
        base_values=explainer.expected_value,
        data=X_test.iloc[0],
        feature_names=X_test.columns
    )

    plt.figure()
    shap.plots.waterfall(
        explanation,
        show=False
    )

    plt.savefig(
        "shap_waterfall.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("\nGenerated:")
    print("shap_summary.png")
    print("shap_importance.png")
    print("shap_waterfall.png")
    print("feature_importance.csv")

except Exception as e:

    print("\nSHAP Failed")
    print(e)

    print("\nFeature importance CSV was still generated.")