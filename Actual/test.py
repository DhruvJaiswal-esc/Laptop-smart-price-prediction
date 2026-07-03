import joblib

feature_columns = joblib.load(
    "trained_models/recommendation/features.pkl"
)

print(len(feature_columns))

for col in feature_columns:
    print(col)