from catboost import CatBoostRegressor
import pandas as pd
import numpy as np

X = pd.DataFrame({
    "a": np.random.rand(1000),
    "b": np.random.rand(1000)
})

y = np.random.rand(1000)

model = CatBoostRegressor(
    iterations=100,
    task_type="GPU",
    devices="0",
    verbose=10
)

model.fit(X, y)

print("GPU training successful")