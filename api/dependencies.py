import joblib
import pandas as pd



from api.explainability.shap_utils import SHAPExplainer
from api.explainability.lime_utils import LIMEExplainer
from api.explainability.report import ExplainabilityReport

# =====================================================
# DATASET
# =====================================================

laptop_dataset = pd.read_csv(
    "data/processed/laptop_dataset_enhanced.csv"
)

# =====================================================
# MODELS
# =====================================================

price_model = joblib.load(
    "trained_models/regression/catboost.pkl"
)

classification_model = joblib.load(
    "trained_models/classification/classifier.pkl"
)

recommendation_model = joblib.load(
    "trained_models/recommendation/recommender.pkl"
)

recommendation_scaler = joblib.load(
    "trained_models/recommendation/scaler.pkl"
)

# =====================================================
# RECOMMENDATION DATA
# =====================================================

recommendation_features = joblib.load(
    "trained_models/recommendation/features.pkl"
)

recommendation_feature_columns = (
    recommendation_features.columns.tolist()
)

recommendation_dataset = joblib.load(
    "trained_models/recommendation/laptops.pkl"
)

# =====================================================
# NLP MODEL
# =====================================================



# =====================================================
# EXPLAINABILITY
# =====================================================

shap_explainer = SHAPExplainer(
    price_model
)

# =====================================================
# LIME TRAINING DATA
# =====================================================

lime_training_df = laptop_dataset.drop(
    columns=["Price (Rs)"]
)

print("\n===== LIME TRAINING =====")
print(lime_training_df.columns.tolist())
print(len(lime_training_df.columns))

lime_explainer = LIMEExplainer(
    price_model,
    lime_training_df
)

report_generator = ExplainabilityReport()