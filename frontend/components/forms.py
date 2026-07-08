import streamlit as st

from config import (
    RAM_TYPES,
    SSD_TYPES,
    BATTERY_TYPES,
    WARRANTY_OPTIONS,
    WIFI_OPTIONS,
    BLUETOOTH_OPTIONS
)


# =====================================================
# FORM
# Grouped by what an engineer would actually check, not an
# arbitrary two-column split: identity → compute → memory →
# power/connectivity. Each group gets a small mono eyebrow.
# =====================================================

def laptop_input_form():

    with st.form("prediction_form", clear_on_submit=False):

        st.markdown(
            '<div class="lmi-eyebrow">Laptop Details</div>',
            unsafe_allow_html=True
        )
        st.markdown("### Tell us about the laptop")
        st.caption("Enter the details you'd see on a listing or spec sheet, then get a price.")

        st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

        # -------------------------------------------------
        # BASICS
        # -------------------------------------------------
        st.markdown(
            '<div class="lmi-eyebrow" style="margin-top:4px;">Basics</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            brand = st.text_input("Brand", placeholder="ASUS")

        with col2:
            processor = st.text_input("Processor", placeholder="Intel Core i7-13620H")

        with col3:
            graphic_processor = st.text_input("Graphic Processor", placeholder="RTX 4060")

        st.divider()

        # -------------------------------------------------
        # MEMORY & STORAGE
        # -------------------------------------------------
        st.markdown(
            '<div class="lmi-eyebrow">Memory &amp; Storage</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            capacity = st.number_input("RAM (GB)", min_value=1, max_value=128, value=16, step=4)

        with col2:
            ram_type = st.selectbox("RAM Type", RAM_TYPES)

        with col3:
            ram_speed = st.number_input("RAM Speed (MT/s)", min_value=1600, max_value=9000, value=3200, step=400)

        with col4:
            ssd_capacity = st.number_input("SSD (GB)", min_value=128, max_value=4096, value=512, step=128)

        with col5:
            ssd_type = st.selectbox("SSD Type", SSD_TYPES)

        st.divider()

        # -------------------------------------------------
        # GRAPHICS & BUILD
        # -------------------------------------------------
        st.markdown(
            '<div class="lmi-eyebrow">Graphics &amp; Build</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            graphics_memory = st.number_input("Graphics Memory (GB)", min_value=0, max_value=32, value=6, step=1)

        with col2:
            weight = st.number_input("Weight (kg)", min_value=0.8, max_value=5.0, value=2.1, step=0.1, format="%.1f")

        with col3:
            warranty = st.selectbox("Warranty (Years)", WARRANTY_OPTIONS)

        st.divider()

        # -------------------------------------------------
        # POWER & CONNECTIVITY
        # -------------------------------------------------
        st.markdown(
            '<div class="lmi-eyebrow">Power &amp; Connectivity</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            battery_capacity = st.number_input("Battery (Wh)", min_value=20, max_value=120, value=0)

        with col2:
            battery_type = st.selectbox("Battery Type", BATTERY_TYPES)

        with col3:
            wi_fi_version = st.selectbox("Wi-Fi Version", WIFI_OPTIONS)

        with col4:
            bluetooth_version = st.selectbox("Bluetooth Version", BLUETOOTH_OPTIONS)

        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "Get Price",
            use_container_width=True,
            type="primary"
        )

    laptop_information = {
        "brand": brand,
        "processor": processor,
        "graphic_processor": graphic_processor,
        "capacity": int(capacity),
        "ram_type": ram_type,
        "ram_speed": int(ram_speed),
        "ssd_capacity": int(ssd_capacity),
        "ssd_type": ssd_type,
        "graphics_memory": int(graphics_memory),
        "battery_capacity": int(battery_capacity),
        "battery_type": battery_type,
        "weight": float(weight),
        "warranty": int(warranty),
        "wi_fi_version": wi_fi_version,
        "bluetooth_version": bluetooth_version
    }

    return submitted, laptop_information


# =====================================================
# VALIDATION
# =====================================================

def validate_input(laptop_information):

    required = ["brand", "processor", "graphic_processor"]

    missing = []

    for field in required:
        if not str(laptop_information[field]).strip():
            missing.append(field)

    if missing:
        pretty = ", ".join(f.replace("_", " ").title() for f in missing)
        return False, f"Missing required field(s): {pretty}."

    return True, "OK"
