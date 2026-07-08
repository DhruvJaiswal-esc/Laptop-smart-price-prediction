import streamlit as st
from pathlib import Path

from config import (
    PROJECT_NAME,
    PRIMARY_COLOR,
    PRIMARY_COLOR_BRIGHT,
    SECONDARY_COLOR,
    CSS_PATH,
    SESSION_DEFAULTS,
)

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False


# =====================================================
# SESSION STATE
# =====================================================

def initialize_session():
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =====================================================
# CSS LOADER
# =====================================================

def load_css():
    css_file = Path(CSS_PATH)
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =====================================================
# BRAND HEADER (sidebar)
# =====================================================

def render_brand():
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; margin-bottom:6px;">
            <div class="sb-logo">◈</div>
        </div>
        <div style="text-align:center; margin-top:14px;">
            <div class="sb-brand-name">{PROJECT_NAME}</div>
            <div class="sb-brand-tag">Smart pricing, clear answers</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.divider()


# =====================================================
# NAVIGATION (sidebar)
# =====================================================

def render_navigation():
    """Renders sidebar nav and returns the current page key."""

    current = st.session_state.get("current_page", "home")

    pages = [
        ("home", "Home", "house-door"),
        ("predict", "Get a Price", "tag"),
        ("recommend", "Similar Laptops", "laptop"),
        ("explain", "Understand Price", "bar-chart-line"),
    ]

    page_keys = [p[0] for p in pages]
    page_labels = [p[1] for p in pages]
    page_icons = [p[2] for p in pages]

    if HAS_OPTION_MENU:
        default_idx = page_keys.index(current) if current in page_keys else 0

        selected_label = option_menu(
            menu_title=None,
            options=page_labels,
            icons=page_icons,
            default_index=default_idx,
            orientation="vertical",
            manual_select=default_idx,
            styles={
                "container": {
                    "padding": "0 !important",
                    "background-color": "transparent",
                    "border-radius": "0 !important",
                },
                "icon": {
                    "color": "#94A3B8",
                    "font-size": "15px",
                },
                "nav-link": {
                    "font-size": "14px",
                    "font-weight": "600",
                    "text-align": "left",
                    "margin": "0 0 6px 0",
                    "border-radius": "10px",
                    "padding": "10px 14px",
                    "color": "#94A3B8",
                    "background-color": "rgba(255,255,255,0.05)",
                    "backdrop-filter": "blur(12px)",
                    "-webkit-backdrop-filter": "blur(12px)",
                    "border": "1px solid rgba(255,255,255,0.08)",
                    "transition": "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
                },
                "nav-link-hover": {
                    "color": "#A78BFA",
                    "background-color": "rgba(255,255,255,0.08)",
                    "border-color": "rgba(255,255,255,0.14)",
                    "transform": "translateX(3px)",
                },
                "nav-link-selected": {
                    "background-image": "linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)",
                    "color": "#FFFFFF",
                    "font-weight": "700",
                    "border": "1px solid rgba(255,255,255,0.15)",
                    "box-shadow": "0 4px 16px rgba(139,92,246,0.30), inset 0 1px 1px rgba(255,255,255,0.15)",
                },
            },
        )

        label_to_key = {p[1]: p[0] for p in pages}
        selected_page = label_to_key.get(selected_label, "home")

        if selected_page != current:
            st.session_state.current_page = selected_page
            current = selected_page

    else:
        # Fallback: radio buttons
        label_to_key = {p[1]: p[0] for p in pages}
        key_to_label = {p[0]: p[1] for p in pages}
        selected_label = st.sidebar.radio(
            "Navigate",
            options=page_labels,
            label_visibility="collapsed",
        )
        selected_page = label_to_key.get(selected_label, "home")
        if selected_page != current:
            st.session_state.current_page = selected_page
            st.rerun()

    return current


# =====================================================
# PROGRESS TRACKER (sidebar)
# =====================================================

def render_progress():
    prediction_done = st.session_state.get("prediction_complete", False)
    recommendations_done = st.session_state.get("recommendations") is not None
    explainability_done = st.session_state.get("explainability") is not None

    completed = sum([prediction_done, recommendations_done, explainability_done])
    percent = int((completed / 3) * 100)

    steps = [
        ("Get a Price", prediction_done),
        ("Similar Laptops", recommendations_done),
        ("Understand Price", explainability_done),
    ]

    current_step = next((i for i, (_, done) in enumerate(steps) if not done), len(steps))

    # Progress bar
    st.sidebar.markdown(
        f"""
        <div class="sb-progress-label">Progress</div>
        <div class="sb-progress-track">
            <div class="sb-progress-fill" style="width:{percent}%"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Step dots
    html_parts = []
    for i, (label, done) in enumerate(steps):
        if done:
            dot_class = "done"
            text_class = "done"
            marker = "✓"
        elif i == current_step:
            dot_class = "current"
            text_class = "current"
            marker = str(i + 1)
        else:
            dot_class = "pending"
            text_class = ""
            marker = str(i + 1)

        connector_class = "done" if done else "pending"
        connector = f'<div class="sb-step-connector {connector_class}"></div>' if i < len(steps) - 1 else ""

        html_parts.append(
            f'<div class="sb-step-row">'
            f'<div class="sb-step-dot {dot_class}">{marker}</div>'
            f'<div class="sb-step-text {text_class}">{label}</div>'
            f'</div>'
            f'{connector}'
        )

    st.sidebar.markdown(
        f'<div style="margin:14px 0 4px 0;">{"".join(html_parts)}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# LATEST RESULT (sidebar)
# =====================================================

def render_latest_result():
    prediction = st.session_state.get("prediction")
    if prediction is None:
        return

    st.sidebar.divider()
    st.sidebar.markdown(
        '<div class="sb-result-label">Latest Result</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Price", f"₹{prediction['predicted_price']:,.0f}")
    with col2:
        st.metric("Category", prediction["predicted_category"])


# =====================================================
# QUICK ACTIONS (sidebar)
# =====================================================

def render_quick_actions():
    st.sidebar.divider()
    if st.sidebar.button("↺  Start Over", use_container_width=True):
        keys = [
            "prediction", "prediction_id", "recommendations",
            "explainability", "prediction_complete", "laptop_information",
        ]
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_page = "home"
        st.rerun()


# =====================================================
# ABOUT (sidebar)
# =====================================================

def render_about():
    st.sidebar.divider()
    with st.sidebar.expander("What this can do", expanded=False):
        st.markdown("""
- Estimate a laptop's price
- Tell you what category it falls into
- Show you similar laptops
- Explain what shaped the price
- Give you a downloadable report
        """)


# =====================================================
# COMPLETE SIDEBAR
# =====================================================

def render_sidebar():
    """Renders the full glassmorphic sidebar and returns the current page key."""

    initialize_session()
    load_css()

    render_brand()
    current_page = render_navigation()
    st.sidebar.divider()
    render_progress()
    render_latest_result()
    render_quick_actions()
    render_about()

    return current_page
