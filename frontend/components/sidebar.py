import streamlit as st

from pathlib import Path

from config import (
    PROJECT_NAME,
    PRIMARY_COLOR,
    LOGO_PATH,
    CSS_PATH,
    SESSION_DEFAULTS
)


# =====================================================
# SESSION STATE
# Initialized here (not just app.py) for the same reason CSS is
# loaded here: Streamlit runs each page in a multipage app as its
# own script, and a user can land directly on pages/1, 2, or 3
# (via URL, refresh, or the sidebar) without app.py ever running
# in that session. Every page calls render_sidebar() first thing,
# so this guarantees session keys always exist before a page reads
# them - this init is idempotent, so re-running it on every page
# has no effect once the keys are already set.
# =====================================================

def initialize_session():

    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =====================================================
# GLOBAL CSS
# Loaded from here (not app.py) because every page in this
# multipage app calls render_sidebar() first thing, and Streamlit
# runs each page as its own script - a CSS load in app.py only
# never reaches pages/1, 2, or 3. Centralizing it here is what
# guarantees fonts and styling are identical on every page.
# =====================================================

def load_css():

    css_file = Path(CSS_PATH)

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =====================================================
# LOGO
# =====================================================

def render_logo():

    if Path(LOGO_PATH).exists():

        st.sidebar.image(
            str(LOGO_PATH),
            use_container_width=True
        )

    else:

        st.sidebar.markdown(
            f"""
            <div style="
                width: 40px; height: 40px;
                border: 1px solid {PRIMARY_COLOR};
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 18px;
                color: {PRIMARY_COLOR};
                font-family: 'Space Mono', monospace;
                margin: 0 auto;
                background: rgba(201,124,61,0.08);
            ">◈</div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# PROJECT HEADER
# =====================================================

def render_header():

    render_logo()

    st.sidebar.markdown(
        f"""
        <div style="text-align:center; margin-top:14px;">
            <div style="
                font-family:'Space Mono',monospace;
                font-size:10px;
                font-weight:600;
                letter-spacing:0.14em;
                text-transform:uppercase;
                color:#8A8F98;
                margin-bottom:4px;
            ">Laptop Pricing Assistant</div>
            <h2 style="
                color:#EDEAE4;
                margin:0;
                font-size:17px;
                font-weight:600;
                line-height:1.3;
                font-family:'Fraunces',serif;
            ">{PROJECT_NAME}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()


# =====================================================
# PROGRESS TRACKER
# Replaces the old separate "current prediction" + "session
# progress" blocks with one compact stepper. Each step shows its
# state at a glance: done (filled, checked), current (outlined,
# active color), upcoming (dim). This is the sidebar's real job -
# telling the person where they are in the 3-step flow - so it's
# given the most visual weight, right under the project header.
# =====================================================

# =====================================================
# PROGRESS TRACKER
# =====================================================

# =====================================================
# PROGRESS TRACKER
# =====================================================

def progress_tracker():

    prediction_done = st.session_state.get("prediction_complete", False)
    recommendations_done = st.session_state.get("recommendations") is not None
    explainability_done = st.session_state.get("explainability") is not None

    steps = [
        ("Get a Price", prediction_done),
        ("Similar Laptops", recommendations_done),
        ("Understand the Price", explainability_done),
    ]

    current = next((i for i, (_, done) in enumerate(steps) if not done), len(steps))

    html_parts = []

    for i, (label, done) in enumerate(steps):
        if done:
            marker = "✓"
            marker_style = f"background:{PRIMARY_COLOR}; color:#0A0C0E; border-color:{PRIMARY_COLOR};"
            text_style = "color:#EDEAE4;"
        elif i == current:
            marker = str(i + 1)
            marker_style = f"background:transparent; color:{PRIMARY_COLOR}; border-color:{PRIMARY_COLOR};"
            text_style = f"color:{PRIMARY_COLOR}; font-weight:600;"
        else:
            marker = str(i + 1)
            marker_style = "background:transparent; color:#5A5F66; border-color:#2A2E33;"
            text_style = "color:#5A5F66;"

        connector = f'<div style="width:1px; height:16px; margin:2px 0 2px 11px; background:{"rgba(201,124,61,0.5)" if done else "#2A2E33"};"></div>' if i < len(steps) - 1 else ""

        html_parts.append(f'<div style="display:flex; align-items:center; gap:10px;"><div style="width:23px; height:23px; border-radius:50%; border:1px solid; {marker_style} display:flex; align-items:center; justify-content:center; font-family:\'Space Mono\',monospace; font-size:11px; font-weight:600; flex-shrink:0;">{marker}</div><div style="font-size:13px; {text_style}">{label}</div></div>{connector}')

    # Wrap the parts and forcefully strip any sneaky newlines before Streamlit sees it
    raw_html_string = f'<div style="margin:4px 0 14px 0;">{"".join(html_parts)}</div>'
    bulletproof_html = raw_html_string.replace("\n", "").replace("\r", "")

    # In newer versions of Streamlit, st.html() bypasses the markdown parser entirely.
    # We will try that first, and fall back to markdown if you are on an older version.
    try:
        st.sidebar.html(bulletproof_html)
    except AttributeError:
        st.sidebar.markdown(bulletproof_html, unsafe_allow_html=True)
# =====================================================
# LATEST RESULT
# Only shown once a price exists - keeps the sidebar quiet and
# uncluttered for a first-time visitor, and useful once there's
# something to show.
# =====================================================

def latest_result():

    prediction = st.session_state.get("prediction")

    if prediction is None:
        return

    st.sidebar.markdown(
        """
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; font-weight:600; letter-spacing:0.1em;
            text-transform:uppercase; color:#8A8F98; margin-bottom:8px;
        ">Latest Result</div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.metric("Price", f"₹{prediction['predicted_price']:,.0f}")

    with col2:
        st.metric("Category", prediction["predicted_category"])

    st.sidebar.markdown("<div style='margin-top:2px'></div>", unsafe_allow_html=True)


# =====================================================
# QUICK ACTIONS
# =====================================================

def quick_actions():

    st.sidebar.divider()

    if st.sidebar.button("↺  Start Over", use_container_width=True):

        keys = [
            "prediction",
            "prediction_id",
            "recommendations",
            "explainability",
            "prediction_complete",
            "laptop_information",
        ]

        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()


# =====================================================
# ABOUT
# =====================================================

def about():

    st.sidebar.divider()

    with st.sidebar.expander("What this can do", expanded=False):

        st.markdown(
            """
- Estimate a laptop's price
- Tell you what category it falls into
- Show you similar laptops
- Explain what shaped the price
- Give you a downloadable report
            """
        )


# =====================================================
# COMPLETE SIDEBAR
# =====================================================

def render_sidebar():

    initialize_session()
    load_css()
    render_header()
    progress_tracker()
    latest_result()
    quick_actions()
    about()
