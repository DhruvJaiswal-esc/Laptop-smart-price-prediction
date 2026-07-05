import numpy as np
import pandas as pd

from pathlib import Path

from lime.lime_tabular import LimeTabularExplainer


class LIMEExplainer:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(

        self,

        model,

        training_df: pd.DataFrame,

        save_directory="reports/lime"

    ):

        self.model = model

        self.save_directory = Path(
            save_directory
        )

        self.save_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # ------------------------------------------
        # Copy dataframe
        # ------------------------------------------

        self.training_df = training_df.copy()

        # ------------------------------------------
        # Remove target if accidentally supplied
        # ------------------------------------------

        if "Price (Rs)" in self.training_df.columns:

            self.training_df = self.training_df.drop(
                columns=["Price (Rs)"]
            )

        # ------------------------------------------
        # Feature order
        # ------------------------------------------

        self.feature_names = list(
            self.training_df.columns
        )

        # ------------------------------------------
        # Detect categorical columns
        # ------------------------------------------

        self.categorical_columns = list(

            self.training_df.select_dtypes(

                include=["object"]

            ).columns

        )

        # ------------------------------------------
        # Detect numerical columns
        # ------------------------------------------

        self.numeric_columns = [

            col

            for col in self.feature_names

            if col not in self.categorical_columns

        ]

        # ------------------------------------------
        # Category maps
        # ------------------------------------------

        self.forward_maps = {}

        self.backward_maps = {}

        encoded_training = self.training_df.copy()

        # ------------------------------------------
        # Encode categoricals
        # ------------------------------------------

        for column in self.categorical_columns:

            values = (

                encoded_training[column]

                .astype(str)

                .fillna("Unknown")

                .unique()

            )

            values = sorted(values)

            forward = {

                value: idx

                for idx, value

                in enumerate(values)

            }

            backward = {

                idx: value

                for value, idx

                in forward.items()

            }

            self.forward_maps[column] = forward

            self.backward_maps[column] = backward

            encoded_training[column] = (

                encoded_training[column]

                .astype(str)

                .fillna("Unknown")

                .map(forward)

                .astype(float)

            )

        # ------------------------------------------
        # Numeric cleanup
        # ------------------------------------------

        for column in self.numeric_columns:

            encoded_training[column] = pd.to_numeric(

                encoded_training[column],

                errors="coerce"

            ).fillna(0)

        self.training_matrix = encoded_training

        # ------------------------------------------
        # LIME categorical indices
        # ------------------------------------------

        categorical_features = [

            self.feature_names.index(col)

            for col in self.categorical_columns

        ]

        categorical_names = {

            self.feature_names.index(col):

            list(

                self.forward_maps[col].keys()

            )

            for col in self.categorical_columns

        }

        # ------------------------------------------
        # Build explainer
        # ------------------------------------------

        self.explainer = LimeTabularExplainer(

            training_data=self.training_matrix.to_numpy(),

            feature_names=self.feature_names,

            categorical_features=categorical_features,

            categorical_names=categorical_names,

            mode="regression",

            discretize_continuous=False,

            random_state=42

        )

    # =====================================================
    # REORDER FEATURES
    # =====================================================

    def _reorder(

        self,

        df: pd.DataFrame

    ):

        df = df.copy()

        return df[

            self.feature_names

        ]

    # =====================================================
    # ENCODE
    # =====================================================

    def _encode(

        self,

        df: pd.DataFrame

    ):

        df = self._reorder(df)

        encoded = df.copy()

        for column in self.categorical_columns:

            mapping = self.forward_maps[column]

            encoded[column] = (

                encoded[column]

                .astype(str)

                .fillna("Unknown")

                .map(mapping)

                .fillna(0)

                .astype(float)

            )

        for column in self.numeric_columns:

            encoded[column] = pd.to_numeric(

                encoded[column],

                errors="coerce"

            ).fillna(0)

        return encoded

    # =====================================================
    # DECODE
    # =====================================================

    def _decode(

        self,

        matrix

    ):

        df = pd.DataFrame(

            matrix,

            columns=self.feature_names

        )

        for column in self.categorical_columns:

            reverse = self.backward_maps[column]

            df[column] = (

                df[column]

                .round()

                .astype(int)

                .map(reverse)

                .fillna(

                    list(

                        reverse.values()

                    )[0]

                )

            )

        for column in self.numeric_columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            ).fillna(0)

        return df

    # =====================================================
    # CATBOOST PREDICT FUNCTION
    # =====================================================

    def predict(

        self,

        encoded_matrix

    ):

        decoded = self._decode(

            encoded_matrix

        )

        predictions = self.model.predict(

            decoded

        )

        return np.array(

            predictions,

            dtype=float

        )

    # =====================================================
    # PREPARE INSTANCE
    # =====================================================

    def prepare_instance(

        self,

        input_df

    ):

        encoded = self._encode(

            input_df

        )

        return encoded.iloc[0].to_numpy()
        # =====================================================
    # EXPLAIN INSTANCE
    # =====================================================

    def explain(

        self,

        input_df: pd.DataFrame,

        num_features=10,

        num_samples=5000

    ):

        encoded_instance = self.prepare_instance(

            input_df

        )

        explanation = self.explainer.explain_instance(

            data_row=encoded_instance,

            predict_fn=self.predict,

            num_features=num_features,

            num_samples=num_samples

        )

        return explanation

    # =====================================================
    # RAW EXPLANATION
    # =====================================================

    def raw(

        self,

        input_df

    ):

        return self.explain(

            input_df

        )

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    def feature_importance(

        self,

        input_df,

        num_features=10

    ):

        explanation = self.explain(

            input_df,

            num_features=num_features

        )

        features = []

        for feature, weight in explanation.as_list():

            features.append({

                "feature": feature,

                "impact": float(weight),

                "absolute_impact": abs(

                    float(weight)

                ),

                "direction":

                    "Increase"

                    if weight >= 0

                    else "Decrease"

            })

        features.sort(

            key=lambda x:

            x["absolute_impact"],

            reverse=True

        )

        return features

    # =====================================================
    # TOP FEATURES
    # =====================================================

    def top_features(

        self,

        input_df,

        top_n=10

    ):

        return self.feature_importance(

            input_df,

            num_features=top_n

        )

    # =====================================================
    # POSITIVE FEATURES
    # =====================================================

    def positive_features(

        self,

        input_df,

        top_n=5

    ):

        features = self.feature_importance(

            input_df,

            num_features=20

        )

        return [

            feature

            for feature in features

            if feature["impact"] > 0

        ][:top_n]

    # =====================================================
    # NEGATIVE FEATURES
    # =====================================================

    def negative_features(

        self,

        input_df,

        top_n=5

    ):

        features = self.feature_importance(

            input_df,

            num_features=20

        )

        return [

            feature

            for feature in features

            if feature["impact"] < 0

        ][:top_n]

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(

        self,

        input_df,

        top_n=10

    ):

        prediction = float(

            np.expm1(

                self.model.predict(

                    input_df

                )[0]

            )

        )

        return {

            "prediction": prediction,

            "top_features": top_n,

            "num_features": len(

                self.feature_names

            )

        }

    # =====================================================
    # AS LIST
    # =====================================================

    def as_list(

        self,

        input_df,

        num_features=10

    ):

        explanation = self.explain(

            input_df,

            num_features=num_features

        )

        return explanation.as_list()

    # =====================================================
    # AS MAP
    # =====================================================

    def as_map(

        self,

        input_df,

        num_features=10

    ):

        explanation = self.explain(

            input_df,

            num_features=num_features

        )

        return explanation.as_map()
        # =====================================================
    # SAVE HTML
    # =====================================================

    def save_html(

        self,

        input_df,

        filename="lime_explanation.html",

        num_features=10

    ):

        explanation = self.explain(

            input_df,

            num_features=num_features

        )

        filepath = self.save_directory / filename

        explanation.save_to_file(

            str(filepath)

        )

        return str(filepath)

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

                    input_df,

                    top_n

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

        top_n=10,

        save_html=True

    ):

        result = {

            "summary":

                self.summary(

                    input_df,

                    top_n

                ),

            "all_features":

                self.feature_importance(

                    input_df,

                    len(

                        self.feature_names

                    )

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

        if save_html:

            result["html"] = self.save_html(

                input_df,

                num_features=top_n

            )

        return result

    # =====================================================
    # PRINT EXPLANATION
    # =====================================================

    def print_explanation(

        self,

        input_df,

        top_n=10

    ):

        result = self.explain_prediction(

            input_df,

            top_n=top_n,

            save_html=False

        )

        print("\n========== LIME ==========\n")

        print(

            "Prediction :",

            result["summary"]["prediction"]

        )

        print()

        for feature in result["top_features"]:

            sign = "+"

            if feature["impact"] < 0:

                sign = "-"

            print(

                f"{feature['feature']:<45}"

                f"{sign}"

                f"{abs(feature['impact']):.6f}"

            )

        print("\n==========================\n")

    # =====================================================
    # API RESPONSE
    # =====================================================

    def api_response(

        self,

        input_df,

        top_n=10

    ):

        explanation = self.explain_prediction(

            input_df,

            top_n=top_n,

            save_html=True

        )

        return {

            "prediction":

                explanation["summary"]["prediction"],

            "top_features":

                explanation["top_features"],

            "positive_features":

                explanation["positive_features"],

            "negative_features":

                explanation["negative_features"],

            "html_report":

                explanation["html"]

        }

    # =====================================================
    # COMPLETE REPORT
    # =====================================================

    def full_report(

        self,

        input_df,

        top_n=10

    ):

        report = self.api_response(

            input_df,

            top_n

        )

        report["raw"] = self.raw(

            input_df

        )

        report["list"] = self.as_list(

            input_df,

            top_n

        )

        report["map"] = self.as_map(

            input_df,

            top_n

        )

        return report
    