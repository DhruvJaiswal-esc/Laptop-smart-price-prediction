import streamlit as st

from config import (
    SPINNER_PREDICTION,
    SPINNER_RECOMMENDATION,
    SPINNER_EXPLAINABILITY,
)


def prediction_spinner():
    return st.spinner(SPINNER_PREDICTION)

def recommendation_spinner():
    return st.spinner(SPINNER_RECOMMENDATION)

def explainability_spinner():
    return st.spinner(SPINNER_EXPLAINABILITY)

def prediction_success():
    st.success("Here's your price.")

def recommendation_success():
    st.success("Found some similar laptops.")

def explainability_success():
    st.success("Here's what shaped this price.")

def show_error(message):
    st.error(message)


def shap_metrics(shap_result):
    if shap_result is None:
        return
    positive = len(shap_result.get("positive_features", []))
    negative = len(shap_result.get("negative_features", []))
    total = len(shap_result.get("all_features", shap_result.get("top_features", [])))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pushed Price Up", positive)
    with c2:
        st.metric("Pushed Price Down", negative)
    with c3:
        st.metric("Things We Looked At", total)


def lime_metrics(lime_result):
    if lime_result is None:
        return
    positive = len(lime_result.get("positive_features", []))
    negative = len(lime_result.get("negative_features", []))
    total = len(lime_result.get("all_features", lime_result.get("top_features", [])))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pushed Price Up", positive)
    with c2:
        st.metric("Pushed Price Down", negative)
    with c3:
        st.metric("Things We Looked At", total)
