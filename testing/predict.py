import pandas as pd
import joblib

# =====================================================
# LOAD FILES ONCE
# =====================================================

MODEL_PATH = "random_forest_optuna.pkl"
ENCODER_PATH = "rf_target_encoder.pkl"
FEATURES_PATH = "rf_feature_columns.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURES_PATH)

# =====================================================
# PREDICTION FUNCTION
# =====================================================

def predict_price(
    Brand,
    Processor,
    Graphic_Processor,
    Capacity,
    RAM_Type,
    RAM_Speed,
    SSD_Capacity,
    SSD_Type,
    Graphics_Memory,
    Battery_Capacity,
    Battery_Type,
    Weight,
    Warranty,
    WiFi_Version,
    Bluetooth_Version,
    Category
):

    # =================================================
    # BASIC VALIDATION
    # =================================================

    if Capacity <= 0:
        raise ValueError("RAM Capacity must be greater than 0")

    if SSD_Capacity <= 0:
        raise ValueError("SSD Capacity must be greater than 0")

    if Weight <= 0:
        raise ValueError("Weight must be greater than 0")

    # =================================================
    # CREATE DATAFRAME
    # =================================================

    data = pd.DataFrame([{
        "Brand": Brand,
        "Processor": Processor,
        "Graphic Processor": Graphic_Processor,
        "Capacity": Capacity,
        "RAM Type": RAM_Type,
        "RAM Speed": RAM_Speed,
        "SSD Capacity": SSD_Capacity,
        "SSD Type": SSD_Type,
        "Graphics Memory": Graphics_Memory,
        "Battery Capacity": Battery_Capacity,
        "Battery Type": Battery_Type,
        "Weight": Weight,
        "Warranty": Warranty,
        "Wi-Fi Version": WiFi_Version,
        "Bluetooth Version": Bluetooth_Version,
        "Category": Category
    }])

    # =================================================
    # ONE HOT ENCODING
    # =================================================

    onehot_cols = [
        "Brand",
        "RAM Type",
        "SSD Type",
        "Wi-Fi Version",
        "Bluetooth Version",
        "Battery Type",
        "Category"
    ]

    data = pd.get_dummies(
        data,
        columns=onehot_cols,
        dtype=int
    )

    # =================================================
    # TARGET ENCODING
    # =================================================

    target_cols = [
        "Processor",
        "Graphic Processor"
    ]

    data[target_cols] = encoder.transform(
        data[target_cols]
    )

    # =================================================
    # MATCH TRAINING FEATURES
    # =================================================

    data = data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # =================================================
    # NUMERIC SAFETY
    # =================================================

    data = data.apply(
        pd.to_numeric,
        errors="coerce"
    ).fillna(0)

    data = data.astype("float32")

    # =================================================
    # PREDICTION
    # =================================================

    prediction = model.predict(data)[0]

    return round(float(prediction), 2)


# =====================================================
# EXAMPLE
# =====================================================

if __name__ == "__main__":

    try:

        price = predict_price(
            Brand="ASUS",
            Processor="Intel Core i5-13420H",
            Graphic_Processor="RTX 4050",
            Capacity=16,
            RAM_Type="DDR5",
            RAM_Speed=4800,
            SSD_Capacity=512,
            SSD_Type="NVMe",
            Graphics_Memory=6,
            Battery_Capacity=90,
            Battery_Type="Li-Ion",
            Weight=2.1,
            Warranty=1,
            WiFi_Version="Wi-Fi 6",
            Bluetooth_Version="5.2",
            Category="Gaming"
        )

        print(f"\nPredicted Price: Rs {price:,.2f}")

    except Exception as e:
        print(f"\nError: {e}")