import pandas as pd
from sklearn.model_selection import train_test_split
from category_encoders import TargetEncoder

df = pd.read_csv("laptop_dataset_reduced.csv")

# -----------------------------
# Target
# -----------------------------
y = df["Price (Rs)"]

X = df.drop("Price (Rs)", axis=1)

# -----------------------------
# Split FIRST
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# One-Hot Columns
# -----------------------------
onehot_cols = [
    "Brand",
    "RAM Type",
    "SSD Type",
    "Wi-Fi Version",
    "Bluetooth Version",
    "Category"
]

X_train = pd.get_dummies(
    X_train,
    columns=onehot_cols
)

X_test = pd.get_dummies(
    X_test,
    columns=onehot_cols
)

# Align columns
X_train, X_test = X_train.align(
    X_test,
    join="left",
    axis=1,
    fill_value=0
)

# -----------------------------
# Target Encoding
# -----------------------------
target_cols = [
    "Processor",
    "Graphic Processor"
]

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

print(X_train.shape)
print(X_test.shape)