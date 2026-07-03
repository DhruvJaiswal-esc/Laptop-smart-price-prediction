from pydantic import BaseModel, Field
from typing import Annotated


class LaptopInput(BaseModel):

    brand: Annotated[
        str,
        Field(..., example="ASUS", description="Laptop Brand")
    ]

    processor: Annotated[
        str,
        Field(..., example="Intel Core i5-13420H", description="Processor Name")
    ]

    graphic_processor: Annotated[
        str,
        Field(..., example="RTX 4050", description="Dedicated/Integrated GPU")
    ]

    capacity: Annotated[
        int,
        Field(..., example=16, description="RAM Capacity (GB)")
    ]

    ram_type: Annotated[
        str,
        Field(..., example="DDR5", description="RAM Type")
    ]

    ram_speed: Annotated[
        int,
        Field(..., example=4800, description="RAM Speed (MT/s)")
    ]

    ssd_capacity: Annotated[
        int,
        Field(..., example=512, description="SSD Capacity (GB)")
    ]

    ssd_type: Annotated[
        str,
        Field(..., example="NVMe", description="SSD Type")
    ]

    graphics_memory: Annotated[
        int,
        Field(..., example=6, description="GPU VRAM (GB)")
    ]

    battery_capacity: Annotated[
        int,
        Field(..., example=57, description="Battery Capacity (Wh)")
    ]

    battery_type: Annotated[
        str,
        Field(..., example="Li-Ion", description="Battery Type")
    ]

    weight: Annotated[
        float,
        Field(..., example=2.1, description="Laptop Weight (kg)")
    ]

    warranty: Annotated[
        int,
        Field(..., example=1, description="Warranty (Years)")
    ]

    wi_fi_version: Annotated[
        str,
        Field(..., example="Wi-Fi 6", description="Wi-Fi Version")
    ]

    bluetooth_version: Annotated[
        str,
        Field(..., example="5.3", description="Bluetooth Version")
    ]

    


class PricePredictionResponse(BaseModel):
    predicted_price: float
    predicted_category: str


class ClassificationResponse(BaseModel):
    predicted_category: str


class Recommendation(BaseModel):
    brand: str
    processor: str
    graphic_processor: str
    category: str


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]