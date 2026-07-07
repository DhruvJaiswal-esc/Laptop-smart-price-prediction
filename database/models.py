from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.database import Base


# =====================================================
# PREDICTION HISTORY
# =====================================================

class PredictionHistory(Base):

    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    brand: Mapped[str] = mapped_column(String(100))

    processor: Mapped[str] = mapped_column(String(150))

    graphic_processor: Mapped[str] = mapped_column(
        String(150)
    )

    capacity: Mapped[int] = mapped_column(Integer)

    ram_type: Mapped[str] = mapped_column(
        String(50)
    )

    ram_speed: Mapped[int] = mapped_column(Integer)

    ssd_capacity: Mapped[int] = mapped_column(
        Integer
    )

    ssd_type: Mapped[str] = mapped_column(
        String(100)
    )

    graphics_memory: Mapped[int] = mapped_column(
        Integer
    )

    battery_capacity: Mapped[int] = mapped_column(
        Integer
    )

    battery_type: Mapped[str] = mapped_column(
        String(50)
    )

    weight: Mapped[float] = mapped_column(Float)

    warranty: Mapped[int] = mapped_column(Integer)

    wifi_version: Mapped[str] = mapped_column(
        String(50)
    )

    bluetooth_version: Mapped[str] = mapped_column(
        String(50)
    )

    predicted_category: Mapped[str] = mapped_column(
        String(100)
    )

    predicted_price: Mapped[float] = mapped_column(
        Float
    )

    # -----------------------------------------------

    explainability = relationship(

        "ExplainabilityHistory",

        back_populates="prediction",

        cascade="all, delete-orphan",

        uselist=False

    )

    recommendations = relationship(

        "RecommendationHistory",

        back_populates="prediction",

        cascade="all, delete-orphan"

    )


# =====================================================
# EXPLAINABILITY
# =====================================================

class ExplainabilityHistory(Base):

    __tablename__ = "explainability_history"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

        index=True

    )

    prediction_id: Mapped[int] = mapped_column(

        ForeignKey(

            "prediction_history.id",

            ondelete="CASCADE"

        )

    )

    shap_json: Mapped[str] = mapped_column(Text)

    lime_json: Mapped[str] = mapped_column(Text)

    report_path: Mapped[str] = mapped_column(Text)

    prediction = relationship(

        "PredictionHistory",

        back_populates="explainability"

    )


# =====================================================
# RECOMMENDATIONS
# =====================================================

class RecommendationHistory(Base):

    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

        index=True

    )

    prediction_id: Mapped[int] = mapped_column(

        ForeignKey(

            "prediction_history.id",

            ondelete="CASCADE"

        )

    )

    brand: Mapped[str] = mapped_column(

        String(100)

    )

    processor: Mapped[str] = mapped_column(

        String(150)

    )

    graphic_processor: Mapped[str] = mapped_column(

        String(150)

    )

    category: Mapped[str] = mapped_column(

        String(100)

    )

    prediction = relationship(

        "PredictionHistory",

        back_populates="recommendations"

    )