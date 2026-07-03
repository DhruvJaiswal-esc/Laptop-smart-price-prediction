
import pandas as pd

from fastapi import APIRouter

router = APIRouter()

df = pd.read_csv(
    "data/processed/laptop_dataset_enhanced.csv"
)


@router.get("/")
def market_insights():

    return {

        "total_laptops": len(df),

        "average_price": round(
            float(df["Price (Rs)"].mean()),
            2
        ),

        "average_ram": round(
            float(df["Capacity"].mean()),
            2
        ),

        "average_ssd": round(
            float(df["SSD Capacity"].mean()),
            2
        ),

        "average_weight": round(
            float(df["Weight"].mean()),
            2
        ),

        "top_brands": (
            df["Brand"]
            .value_counts()
            .head(5)
            .to_dict()
        ),

        "category_distribution": (
            df["Category"]
            .value_counts()
            .to_dict()
        ),

        "processor_tier_distribution": (
            df["Processor Tier"]
            .value_counts()
            .to_dict()
        ),

        "gpu_tier_distribution": (
            df["GPU Tier"]
            .value_counts()
            .to_dict()
        )

    }

