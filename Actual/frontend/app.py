import streamlit as st
from components.cards import (
    section_header,
    ambient_banner,
)
from config import (
    PAGE_CONFIG,
    PROJECT_TITLE,
    PROJECT_TAGLINE,
)

from components.sidebar import (
    render_sidebar
)

from components.cards import (
    section_header,
    
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(**PAGE_CONFIG)


# =====================================================
# SIDEBAR
# Also initializes session state - see components/sidebar.py for
# why that lives there instead of here.
# =====================================================

render_sidebar()


# =====================================================
# HERO
# =====================================================

st.markdown(
    f"""
    <div class="lmi-hero">
        <div class="lmi-hero-eyebrow">
            <span class="lmi-dot"></span>
            Simple, clear laptop pricing
        </div>
        <h1 class="lmi-hero-title">{PROJECT_TITLE}</h1>
        <p class="lmi-hero-desc">
            Tell us about a laptop and we'll estimate its price, show you similar
            laptops, and explain exactly what shaped that number — in plain language,
            not a marketing page.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Stat strip directly under the hero - a quick readout of where
# this session stands right now.
# =====================================================
# AMBIENT BREATHER
# =====================================================

ambient_banner(
    title="Take your time.",
    text="Pricing hardware can get overwhelming with endless specs and marketing jargon. We built this space to be quiet, clear, and easy on the eyes. No rush.",
    icon="🌿"
)
# =====================================================
# QUICK START
# =====================================================

st.markdown("<div style='margin-top:40px'></div>", unsafe_allow_html=True)

st.divider()

section_header(
    "Getting started",
    subtitle="Use the pages in the sidebar, in this order."
)

st.markdown(
    """
Start by entering a laptop's details on the first page — the other two pages
both build on that result, so nothing else will work until you've done that
first step.
    """
)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("Laptop Price Checker")
