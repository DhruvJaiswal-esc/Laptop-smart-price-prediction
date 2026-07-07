import os
from pathlib import Path

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt


class SHAPExplainer:

    """
    SHAP Explainer for CatBoost Regression Models.
    """

    def __init__(
        self,
        model,
        save_directory="reports/shap"
    ):

        self.model = model

        self.explainer = shap.TreeExplainer(
            self.model
        )

        self.save_directory = Path(
            save_directory
        )

        self.save_directory.mkdir(
            parents=True,
            exist_ok=True
        )
        # =====================================================
    # PYTHON TYPE
    # =====================================================

    def _python_value(self, value):

        if isinstance(value, np.integer):
            return int(value)

        if isinstance(value, np.floating):
            return float(value)

        if isinstance(value, np.bool_):
            return bool(value)

        if isinstance(value, np.ndarray):
            return value.tolist()

        return value

    # =====================================================
    # INTERNAL
    # =====================================================

    def _explanation(
        self,
        input_df: pd.DataFrame
    ):

        """
        Returns SHAP Explanation object.
        """

        return self.explainer(
            input_df
        )

    # =====================================================
    # SHAP VALUES
    # =====================================================

    def shap_values(
        self,
        input_df: pd.DataFrame
    ):

        explanation = self._explanation(
            input_df
        )

        return explanation.values[0]

    # =====================================================
    # BASE VALUE
    # =====================================================

    def base_value(self):

        value = self.explainer.expected_value

        if isinstance(
            value,
            np.ndarray
        ):
            return float(value[0])

        return self._python_value(value)

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

        # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    def feature_importance(
        self,
        input_df: pd.DataFrame
    ):

        explanation = self._explanation(
            input_df
        )

        shap_values = explanation.values[0]

        result = []

        for feature, value, impact in zip(

            input_df.columns,

            input_df.iloc[0],

            shap_values

        ):

            value = self._python_value(value)

            impact = float(impact)

            result.append({

                "feature": str(feature),

                "value": value,

                "impact": impact,

                "absolute_impact": abs(impact),

                "direction": (

                    "Increase"

                    if impact >= 0

                    else "Decrease"

                )

            })

        result.sort(

            key=lambda x: x["absolute_impact"],

            reverse=True

        )

        return result

    # =====================================================
    # TOP FEATURES
    # =====================================================

    def top_features(

        self,

        input_df,

        top_n=10

    ):

        return self.feature_importance(

            input_df

        )[:top_n]

    # =====================================================
    # POSITIVE
    # =====================================================

    def positive_features(

        self,

        input_df,

        top_n=5

    ):

        features = self.feature_importance(

            input_df

        )

        positives = [

            feature

            for feature in features

            if feature["impact"] > 0

        ]

        return positives[:top_n]

    # =====================================================
    # NEGATIVE
    # =====================================================

    def negative_features(

        self,

        input_df,

        top_n=5

    ):

        features = self.feature_importance(

            input_df

        )

        negatives = [

            feature

            for feature in features

            if feature["impact"] < 0

        ]

        return negatives[:top_n]
        # =====================================================
    # WATERFALL PLOT
    # =====================================================

    def save_waterfall_plot(

        self,

        input_df,

        filename="waterfall.png"

    ):

        explanation = self._explanation(
            input_df
        )

        output_path = self.save_directory / filename

        plt.figure(figsize=(10, 6))

        shap.plots.waterfall(
            explanation[0],
            max_display=15,
            show=False
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return str(output_path)

    # =====================================================
    # BAR PLOT
    # =====================================================

    def save_bar_plot(

        self,

        input_df,

        filename="bar.png"

    ):

        explanation = self._explanation(
            input_df
        )

        output_path = self.save_directory / filename

        plt.figure(figsize=(10, 6))

        shap.plots.bar(
            explanation,
            max_display=15,
            show=False
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return str(output_path)

    # =====================================================
    # BEESWARM PLOT
    # =====================================================

    def save_beeswarm_plot(

        self,

        input_df,

        filename="beeswarm.png"

    ):

        explanation = self._explanation(
            input_df
        )

        output_path = self.save_directory / filename

        plt.figure(figsize=(10, 6))

        shap.plots.beeswarm(
            explanation,
            max_display=15,
            show=False
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return str(output_path)

    # =====================================================
    # DECISION PLOT
    # =====================================================

    def save_decision_plot(

        self,

        input_df,

        filename="decision.png"

    ):

        explanation = self._explanation(
            input_df
        )

        output_path = self.save_directory / filename

        plt.figure(figsize=(12, 6))

        shap.decision_plot(

            self.base_value(),

            explanation.values[0],

            input_df.iloc[0],

            show=False

        )

        plt.tight_layout()

        plt.savefig(

            output_path,

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

        return str(output_path)

    # =====================================================
    # FORCE PLOT
    # =====================================================

    def save_force_plot(

        self,

        input_df,

        filename="force.html"

    ):

        explanation = self._explanation(
            input_df
        )

        output_path = self.save_directory / filename

        force_plot = shap.plots.force(

            self.base_value(),

            explanation.values[0],

            input_df.iloc[0],

            matplotlib=False,

            show=False

        )

        shap.save_html(

            str(output_path),

            force_plot

        )

        return str(output_path)

    # =====================================================
    # GENERATE ALL PLOTS
    # =====================================================

    def generate_all_plots(

        self,

        input_df

    ):

        return {

            "waterfall": self.save_waterfall_plot(

                input_df

            ),

            "bar": self.save_bar_plot(

                input_df

            ),

            "beeswarm": self.save_beeswarm_plot(

                input_df

            ),

            "decision": self.save_decision_plot(

                input_df

            ),

            "force": self.save_force_plot(

                input_df

            )

        }
        # =====================================================
    # SHAP SUMMARY
    # =====================================================

    def summary(self, input_df):

        explanation = self._explanation(input_df)

        return {

            "base_value": self.base_value(),

            "prediction":

                float(

                    self.base_value()

                    +

                    explanation.values[0].sum()

                ),

            "num_features":

                int(len(input_df.columns))

        }

    # =====================================================
    # JSON EXPORT
    # =====================================================

    def to_json(

        self,

        input_df,

        top_n=10

    ):

        return {

            "summary":

                self.summary(

                    input_df

                ),

            "top_features":

                self.top_features(

                    input_df,

                    top_n

                ),

            "positive_features":

                self.positive_features(

                    input_df,

                    top_n

                ),

            "negative_features":

                self.negative_features(

                    input_df,

                    top_n

                )

        }

    # =====================================================
    # COMPLETE EXPLANATION
    # =====================================================

    def explain_prediction(

        self,

        input_df,

        save_plots=True,

        top_n=10

    ):

        response = {

            "summary":

                self.summary(

                    input_df

                ),

            "all_features":

                self.feature_importance(

                    input_df

                ),

            "top_features":

                self.top_features(

                    input_df,

                    top_n

                ),

            "positive_features":

                self.positive_features(

                    input_df,

                    top_n

                ),

            "negative_features":

                self.negative_features(

                    input_df,

                    top_n

                )

        }

        if save_plots:

            try:

                response["plots"] = self.generate_all_plots(

                    input_df

                )

            except Exception as e:

                response["plots"] = {

                    "error": str(e)

                }

        return response

    # =====================================================
    # PRINT EXPLANATION
    # =====================================================

    def print_explanation(

        self,

        input_df,

        top_n=10

    ):

        explanation = self.explain_prediction(

            input_df,

            save_plots=False,

            top_n=top_n

        )

        print("\n========== SHAP EXPLANATION ==========\n")

        print(

            f"Base Value : "

            f"{explanation['summary']['base_value']:.4f}"

        )

        print(

            f"Prediction : "

            f"{explanation['summary']['prediction']:.4f}"

        )

        print("\nTop Features:\n")

        for feature in explanation["top_features"]:

            sign = "+" if feature["impact"] >= 0 else "-"

            print(

                f"{feature['feature']}"

                f" ({feature['value']})"

                f" : "

                f"{sign}"

                f"{abs(feature['impact']):.5f}"

            )

        print("\n======================================\n")