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
# PROGRESS BAR
# =====================================================

def render_progress():
    prediction_done = st.session_state.get("prediction_complete", False)
    recommendations_done = st.session_state.get("recommendations") is not None
    explainability_done = st.session_state.get("explainability") is not None

    completed = sum([prediction_done, recommendations_done, explainability_done])
    percent = int((completed / 3) * 100)

    st.markdown(
        f'<div class="progress-track"><div class="progress-fill" style="width:{percent}%"></div></div>',
        unsafe_allow_html=True
    )


# =====================================================
# NAVBAR
# =====================================================

def render_navbar():
    """Renders the top navbar and returns the current page key."""

    initialize_session()
    load_css()

    # --- Brand bar ---
    st.markdown(
        f"""
        <div class="nav-brand">
            <div class="nav-logo">◈</div>
            <div>
                <div class="nav-title">{PROJECT_NAME}</div>
                <div class="nav-tag">Smart pricing, clear answers</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Nav links ---
    pages = [
        ("home", "Home", "house-door"),
        ("predict", "Get a Price", "tag"),
        ("recommend", "Similar Laptops", "laptop"),
        ("explain", "Understand Price", "bar-chart-line"),
    ]

    page_keys = [p[0] for p in pages]
    page_labels = [p[1] for p in pages]
    page_icons = [p[2] for p in pages]

    current = st.session_state.get("current_page", "home")

    if HAS_OPTION_MENU:
        default_idx = page_keys.index(current) if current in page_keys else 0

        selected_label = option_menu(
            menu_title=None,
            options=page_labels,
            icons=page_icons,
            default_index=default_idx,
            orientation="horizontal",
            manual_select=default_idx,
            styles={
                "container": {
                    "padding": "0 !important",
                    "background-color": "transparent",
                    "border-radius": "0 !important",
                },
                "icon": {
                    "color": "#64748B",
                    "font-size": "15px",
                },
                "nav-link": {
                    "font-size": "14px",
                    "font-weight": "600",
                    "text-align": "center",
                    "margin": "0 6px",
                    "border-radius": "10px",
                    "padding": "10px 16px",
                    "color": "#64748B",
                    "background-color": "rgba(255,255,255,0.35)",
                    "backdrop-filter": "blur(12px)",
                    "-webkit-backdrop-filter": "blur(12px)",
                    "border": "1px solid rgba(255,255,255,0.60)",
                    "transition": "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
                },
                "nav-link-hover": {
                    "color": "#2563EB",
                    "background-color": "rgba(255,255,255,0.55)",
                },
                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "color": "#FFFFFF",
                    "font-weight": "700",
                    "box-shadow": "0 4px 16px rgba(37,99,235,0.25), inset 0 1px 2px rgba(255,255,255,0.30)",
                },
            },
        )

        label_to_key = {p[1]: p[0] for p in pages}
        selected_page = label_to_key.get(selected_label, "home")

        if selected_page != current:
            st.session_state.current_page = selected_page
            current = selected_page

    else:
        # Fallback: use buttons in columns
        cols = st.columns(len(pages))
        for i, (key, label) in enumerate(zip(page_keys, page_labels)):
            with cols[i]:
                is_active = (key == current)
                if st.button(
                    label,
                    key=f"nav_{key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.current_page = key
                    st.rerun()

    # --- Progress bar ---
    render_progress()

    return current


# =====================================================
# QUICK ACTIONS
# =====================================================

def render_reset_button():
    if st.button("↺  Start Over", use_container_width=True):
        keys = [
            "prediction", "prediction_id", "recommendations",
            "explainability", "prediction_complete", "laptop_information",
        ]
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_page = "home"
        st.rerun()
