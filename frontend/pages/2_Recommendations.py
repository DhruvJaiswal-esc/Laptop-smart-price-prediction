import streamlit as st

from api.client import recommend

from components.sidebar import render_sidebar

from components.cards import (
    recommendation_grid,
    section_header,
    workflow_crumb,
    empty_state,
    stat_strip,
)

from components.metrics import (
    recommendation_spinner,
    recommendation_success,
    show_error,
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="Similar Laptops", page_icon="◈", layout="wide")

render_sidebar()


# =====================================================
# HEADER
# =====================================================

workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=1)

section_header(
    "Similar Laptops",
    "Laptops that are a lot like the one you just priced."
)


# =====================================================
# CHECK PREDICTION
# =====================================================

if not st.session_state.get("prediction_complete", False):

    st.divider()

    empty_state(
        "◈",
        "No price yet",
        "This page needs a price to compare against. Go to Get a Price "
        "first, then come back here."
    )

    st.stop()


prediction_id = st.session_state.get("prediction_id")


# =====================================================
# LOAD RECOMMENDATIONS
# =====================================================

if st.session_state.get("recommendations") is None:

    with recommendation_spinner():
        response = recommend(prediction_id)

    if not response["success"]:
        show_error(response["error"])
        st.stop()

    recommendation_success()

    st.session_state.recommendations = response["data"]["recommendations"]


recommendations = st.session_state.recommendations


# =====================================================
# SUMMARY
# =====================================================

stat_strip([
    {"label": "Matches Found", "value": len(recommendations)},
    {"label": "Reference", "value": prediction_id},
])


# =====================================================
# DISPLAY CARDS
# =====================================================

st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

section_header("Laptops Like This One")

recommendation_grid(recommendations)


# =====================================================
# RAW DATA
# =====================================================

with st.expander("Full details"):
    st.json(recommendations)


# =====================================================
# NEXT STEP
# =====================================================

st.divider()

st.info(
    "Continue to **Understand the Price** to see what shaped this price, "
    "plus a report you can download."
)
