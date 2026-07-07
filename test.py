import pandas as pd

from api.explainability.shap_utils import SHAPExplainer
from api.dependencies import price_model

input_df = pd.DataFrame([{

    "Brand": "ASUS",

    "Processor": "Intel Core i5-13420H",

    "Graphic Processor": "RTX 4050",

    "Capacity": 16,

    "RAM Type": "DDR5",

    "RAM Speed": 4800,

    "SSD Capacity": 512,

    "SSD Type": "NVMe",

    "Graphics Memory": 6,

    "Battery Capacity": 57,

    "Battery Type": "Li-Ion",

    "Weight": 2.2,

    "Warranty": 1,

    "Wi-Fi Version": "Wi-Fi 6",

    "Bluetooth Version": "5.3",

    "Category": "Gaming",

    "Processor Tier": "High End",

    "GPU Tier": "Mid Range"

}])

explainer = SHAPExplainer(price_model)

result = explainer.explain_prediction(input_df)

print(result)