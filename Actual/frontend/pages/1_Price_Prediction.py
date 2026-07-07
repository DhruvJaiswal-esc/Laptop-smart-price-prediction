import streamlit as st

from api.client import predict

from components.sidebar import render_sidebar

from components.forms import laptop_input_form, validate_input

from components.cards import (
    prediction_card,
    laptop_summary_card,
    section_header,
    workflow_crumb,
    step_list,
)

from components.metrics import (
    prediction_spinner,
    prediction_success,
    show_error,
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="Price Prediction", page_icon="◈", layout="wide")

render_sidebar()


# =====================================================
# HEADER
# =====================================================

workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=0)

section_header(
    "Get a Price",
    "Enter the laptop's details below and we'll estimate its price and category."
)


# =====================================================
# FORM
# =====================================================

submitted, laptop_information = laptop_input_form()


# =====================================================
# PREDICT
# =====================================================

if submitted:

    valid, message = validate_input(laptop_information)

    if not valid:
        show_error(message)
        st.stop()

    with prediction_spinner():
        response = predict(laptop_information)

    if not response["success"]:
        show_error(response["error"])
        st.stop()

    prediction = response["data"]

    st.session_state.prediction_id = prediction["prediction_id"]

    st.session_state.prediction = {
        "predicted_price": prediction["predicted_price"],
        "predicted_category": prediction["predicted_category"],
    }

    st.session_state.prediction_complete = True
    st.session_state.laptop_information = laptop_information

    prediction_success()


# =====================================================
# DISPLAY RESULTS
# =====================================================

if st.session_state.prediction is not None:

    st.divider()

    section_header("Here's the price", f"Reference: {st.session_state.prediction_id}")

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:

        prediction_card(
            st.session_state.prediction["predicted_price"],
            st.session_state.prediction["predicted_category"]
        )

    with col2:

        st.success("Saved. You can move on when you're ready.")

        step_list([
            {
                "title": "See similar laptops",
                "desc": "Find laptops that are a lot like the one you just priced.",
            },
            {
                "title": "Understand the price",
                "desc": "See what pushed the price up or down, plus a report you can download.",
            },
        ])

    st.divider()

    laptop_summary_card(st.session_state.laptop_information)

else:

    st.divider()
    st.caption("Fill in the details above to see your laptop's price here.")
