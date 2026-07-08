# pyrefly: ignore [missing-import]
import streamlit as st

from api.client import explain

from components.sidebar import render_sidebar

from components.cards import (
    prediction_card,
    laptop_summary_card,
    section_header,
    workflow_crumb,
    empty_state,
)

from components.metrics import (
    explainability_spinner,
    explainability_success,
    show_error,
    shap_metrics,
    lime_metrics,
)

from components.charts import (
    shap_feature_importance,
    shap_positive_chart,
    shap_negative_chart,
    lime_feature_importance,
    lime_positive_chart,
    lime_negative_chart,
    show_plot,
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="Understand the Price", page_icon="◈", layout="wide")

render_sidebar()


# =====================================================
# HEADER
# =====================================================

workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=2)

section_header(
    "Understand the Price",
    "A plain-language look at why we landed on this number."
)


# =====================================================
# CHECK PREDICTION
# =====================================================

if not st.session_state.get("prediction_complete", False):

    st.divider()

    empty_state(
        "◈",
        "No price yet",
        "This page breaks down an existing price. Go to Get a Price "
        "first, then come back here."
    )

    st.stop()


prediction_id = st.session_state.get("prediction_id")


# =====================================================
# LOAD EXPLAINABILITY
# =====================================================

if st.session_state.get("explainability") is None:

    with explainability_spinner():
        response = explain(prediction_id)

    if not response["success"]:
        show_error(response["error"])
        st.stop()

    st.session_state.explainability = response["data"]

    explainability_success()


result = st.session_state.explainability

prediction = result["prediction"]
input_information = result["input"]
shap_result = result["shap"]
lime_result = result["lime"]
report_path = result["report"]


# =====================================================
# SUMMARY
# =====================================================

prediction_card(prediction["predicted_price"], prediction["predicted_category"])

st.divider()


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs(["Details", "The Breakdown", "Double-Check", "Report"])


# =====================================================
# DETAILS
# =====================================================

with tab1:

    laptop_summary_card(input_information, title="What You Told Us")


# =====================================================
# PRIMARY BREAKDOWN (SHAP)
# =====================================================

with tab2:

    section_header("What Shaped This Price", "The main factors behind this number.")

    shap_metrics(shap_result)

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    show_plot(shap_feature_importance(shap_result))

    show_plot(shap_positive_chart(shap_result))
    show_plot(shap_negative_chart(shap_result))


# =====================================================
# CROSS-CHECK (LIME)
# =====================================================

with tab3:

    section_header("A Second Opinion", "We checked our reasoning a different way — here's what that found.")

    lime_metrics(lime_result)

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    show_plot(lime_feature_importance(lime_result))

    show_plot(lime_positive_chart(lime_result))
    show_plot(lime_negative_chart(lime_result))


# =====================================================
# REPORT & RAW DATA
# =====================================================

with tab4:

    with st.expander("Raw Developer Data", expanded=False):
        st.json(result)