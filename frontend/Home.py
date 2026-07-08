import streamlit as st

from config import PAGE_CONFIG, PROJECT_TITLE

from components.sidebar import render_sidebar
from components.cards import (
    section_header,
    feature_card,
    step_list,
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(**PAGE_CONFIG)

# =====================================================
# SIDEBAR (glassmorphic)
# =====================================================

current_page = render_sidebar()

# =====================================================
# HOME PAGE
# =====================================================

if current_page == "home":

    # --- Hero ---
    st.markdown(
        f"""
        <div class="hero-section">
            <div class="hero-eyebrow">
                <span class="hero-dot"></span>
                Simple, clear laptop pricing
            </div>
            <h1 class="hero-title">{PROJECT_TITLE}</h1>
            <p class="hero-desc">
                Tell us about a laptop and we'll estimate its price, show you similar
                laptops, and explain exactly what shaped that number — in plain language,
                not a marketing page.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Feature cards ---
    st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)

    section_header("What you can do here", "Three steps, one result.")

    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "₹", "Get a Price",
            "Enter a laptop's specs and get an instant price estimate with a category label."
        )

    with col2:
        feature_card(
            "⇄", "Similar Laptops",
            "See laptops that are close to the one you priced — same tier, similar specs."
        )

    with col3:
        feature_card(
            "◈", "Understand the Price",
            "A plain-language breakdown of what pushed the price up or down, plus a report."
        )

    # --- How it works ---
    st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)

    section_header("Getting started", "Use the sidebar navigation, in this order.")

    step_list([
        {
            "title": "Get a Price",
            "desc": "Enter a laptop's details on the Get a Price page. Everything else builds on this step.",
        },
        {
            "title": "See Similar Laptops",
            "desc": "Once you have a price, find laptops that are a lot like the one you just priced.",
        },
        {
            "title": "Understand the Price",
            "desc": "See what shaped the price, with a full breakdown and a downloadable report.",
        },
    ])

    st.divider()
    st.caption("Laptop Price Checker")


# =====================================================
# PREDICT PAGE
# =====================================================

elif current_page == "predict":

    from api.client import predict
    from components.forms import laptop_input_form, validate_input
    from components.cards import (
        prediction_card, laptop_summary_card,
        section_header, workflow_crumb, step_list,
    )
    from components.metrics import prediction_spinner, prediction_success, show_error

    workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=0)

    section_header(
        "Get a Price",
        "Enter the laptop's details below and we'll estimate its price and category."
    )

    submitted, laptop_information = laptop_input_form()

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
                {"title": "See similar laptops", "desc": "Find laptops that are a lot like the one you just priced."},
                {"title": "Understand the price", "desc": "See what pushed the price up or down, plus a report you can download."},
            ])

        st.divider()
        laptop_summary_card(st.session_state.laptop_information)
    else:
        st.divider()
        st.caption("Fill in the details above to see your laptop's price here.")


# =====================================================
# RECOMMEND PAGE
# =====================================================

elif current_page == "recommend":

    from api.client import recommend
    from components.cards import (
        recommendation_grid, section_header,
        workflow_crumb, empty_state, stat_strip,
    )
    from components.metrics import recommendation_spinner, recommendation_success, show_error

    workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=1)

    section_header("Similar Laptops", "Laptops that are a lot like the one you just priced.")

    if not st.session_state.get("prediction_complete", False):
        st.divider()
        empty_state("◈", "No price yet",
            "This page needs a price to compare against. Go to Get a Price first, then come back here.")
        st.stop()

    prediction_id = st.session_state.get("prediction_id")

    if st.session_state.get("recommendations") is None:
        with recommendation_spinner():
            response = recommend(prediction_id)
        if not response["success"]:
            show_error(response["error"])
            st.stop()
        recommendation_success()
        st.session_state.recommendations = response["data"]["recommendations"]

    recommendations = st.session_state.recommendations

    stat_strip([
        {"label": "Matches Found", "value": len(recommendations)},
        {"label": "Reference", "value": prediction_id},
    ])

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)
    section_header("Laptops Like This One")
    recommendation_grid(recommendations)

    with st.expander("Full details"):
        st.json(recommendations)

    st.divider()
    st.info("Continue to **Understand the Price** to see what shaped this price, plus a report you can download.")


# =====================================================
# EXPLAIN PAGE
# =====================================================

elif current_page == "explain":

    from api.client import explain
    from components.cards import (
        prediction_card, laptop_summary_card,
        section_header, workflow_crumb, empty_state,
    )
    from components.metrics import (
        explainability_spinner, explainability_success,
        show_error, shap_metrics, lime_metrics,
    )
    from components.charts import (
        shap_feature_importance, shap_positive_chart, shap_negative_chart,
        lime_feature_importance, lime_positive_chart, lime_negative_chart,
        show_plot,
    )

    workflow_crumb(["Get a Price", "Similar Laptops", "Understand the Price"], active_index=2)

    section_header("Understand the Price", "A plain-language look at why we landed on this number.")

    if not st.session_state.get("prediction_complete", False):
        st.divider()
        empty_state("◈", "No price yet",
            "This page breaks down an existing price. Go to Get a Price first, then come back here.")
        st.stop()

    prediction_id = st.session_state.get("prediction_id")

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

    prediction_card(prediction["predicted_price"], prediction["predicted_category"])
    st.divider()

    # --- Details ---
    laptop_summary_card(input_information, title="What You Told Us")
    st.divider()

    # --- SHAP ---
    section_header("What Shaped This Price", "The main factors behind this number.")
    shap_metrics(shap_result)
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    show_plot(shap_feature_importance(shap_result))
    show_plot(shap_positive_chart(shap_result))
    show_plot(shap_negative_chart(shap_result))
    st.divider()

    # --- LIME ---
    section_header("A Second Opinion", "We checked our reasoning a different way — here's what that found.")
    lime_metrics(lime_result)
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    show_plot(lime_feature_importance(lime_result))
    show_plot(lime_positive_chart(lime_result))
    show_plot(lime_negative_chart(lime_result))
    st.divider()

    with st.expander("Raw Developer Data", expanded=False):
        st.json(result)
