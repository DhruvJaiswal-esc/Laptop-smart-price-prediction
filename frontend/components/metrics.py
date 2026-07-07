import streamlit as st

from config import (
    SPINNER_PREDICTION,
    SPINNER_RECOMMENDATION,
    SPINNER_EXPLAINABILITY,
)


# =====================================================
# PRICE METRIC
# =====================================================

def price_metric(predicted_price: float):

    st.metric(
        label="Price",
        value=f"₹{predicted_price:,.0f}"
    )


# =====================================================
# CATEGORY METRIC
# =====================================================

def category_metric(category: str):

    st.metric(
        label="Category",
        value=category
    )


# =====================================================
# PREDICTION METRICS
# =====================================================

def prediction_metrics(predicted_price: float, predicted_category: str):

    col1, col2 = st.columns(2)

    with col1:
        price_metric(predicted_price)

    with col2:
        category_metric(predicted_category)


# =====================================================
# PRICE FACTOR SUMMARY (primary breakdown)
# =====================================================

def shap_metrics(shap_result):

    if shap_result is None:
        return

    positive = len(shap_result.get("positive_features", []))
    negative = len(shap_result.get("negative_features", []))

    # "all_features" isn't part of the /explainability contract - fall
    # back to top_features so this doesn't silently read 0.
    total = len(shap_result.get("all_features", shap_result.get("top_features", [])))

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Pushed Price Up", positive)
    with c2:
        st.metric("Pushed Price Down", negative)
    with c3:
        st.metric("Things We Looked At", total)


# =====================================================
# PRICE FACTOR SUMMARY (cross-check breakdown)
# =====================================================

def lime_metrics(lime_result):

    if lime_result is None:
        return

    positive = len(lime_result.get("positive_features", []))
    negative = len(lime_result.get("negative_features", []))

    # "all_features" isn't part of the /explainability contract - fall
    # back to top_features so this doesn't silently read 0.
    total = len(lime_result.get("all_features", lime_result.get("top_features", [])))

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Pushed Price Up", positive)
    with c2:
        st.metric("Pushed Price Down", negative)
    with c3:
        st.metric("Things We Looked At", total)


# =====================================================
# SYSTEM STATUS
# =====================================================

def backend_metric(connected: bool):

    if connected:
        st.success("Ready to use")
    else:
        st.error("Not available right now")


# =====================================================
# RECOMMENDATION METRICS
# =====================================================

def recommendation_metrics(recommendations):

    if recommendations is None:
        return

    st.metric("Recommendations", len(recommendations))


# =====================================================
# LOADING INDICATORS
# =====================================================

def prediction_spinner():
    return st.spinner(SPINNER_PREDICTION)


def recommendation_spinner():
    return st.spinner(SPINNER_RECOMMENDATION)


def explainability_spinner():
    return st.spinner(SPINNER_EXPLAINABILITY)


# =====================================================
# SUCCESS MESSAGES
# =====================================================

def prediction_success():
    st.success("Here's your price.")


def recommendation_success():
    st.success("Found some similar laptops.")


def explainability_success():
    st.success("Here's what shaped this price.")


# =====================================================
# ERROR MESSAGE
# =====================================================

def show_error(message):
    st.error(message)
