import streamlit as st


# =====================================================
# PREDICTION CARD (the "quote strip" signature element)
# =====================================================

def prediction_card(
    predicted_price: float,
    predicted_category: str
):

    st.markdown(
        f"""
        <div class="lmi-quote">
            <div class="lmi-quote-cell">
                <div class="lmi-quote-label">◈ Estimated Price</div>
                <div class="lmi-quote-value">₹{predicted_price:,.0f}</div>
                <div class="lmi-quote-sub">Our best estimate, in rupees</div>
            </div>
            <div class="lmi-quote-cell">
                <div class="lmi-quote-label">Category</div>
                <div class="lmi-quote-value secondary">{predicted_category}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# RECOMMENDATION CARD
# =====================================================

def recommendation_card(
    brand,
    processor,
    gpu,
    category,
    rank=None
):

    rank_html = f'<span class="lmi-card-rank">#{rank:02d}</span>' if rank is not None else ""

    st.markdown(
        f"""
        <div class="lmi-card">
            <div class="lmi-card-title">
                <span>{brand}</span>
                {rank_html}
            </div>
            <div class="lmi-card-row">
                <span class="lmi-card-row-label">Processor</span>
                <span class="lmi-card-row-value">{processor}</span>
            </div>
            <div class="lmi-card-row">
                <span class="lmi-card-row-label">Graphics</span>
                <span class="lmi-card-row-value">{gpu}</span>
            </div>
            <div class="lmi-tag">{category}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# RECOMMENDATION GRID
# =====================================================

def recommendation_grid(
    recommendations
):

    cols = st.columns(2)

    for index, recommendation in enumerate(recommendations):

        with cols[index % 2]:

            recommendation_card(
                recommendation["brand"],
                recommendation["processor"],
                recommendation["graphic_processor"],
                recommendation["category"],
                rank=index + 1
            )
# =====================================================
# AMBIENT BANNER
# =====================================================

def ambient_banner(title, text, icon="✨"):
    
    import streamlit as st
    
    st.markdown(
        f"""
        <div style="
            border: 1px solid var(--cyan-dim);
            border-radius: var(--radius-lg);
            padding: 24px 32px;
            background: linear-gradient(135deg, var(--cyan-glow), transparent 60%), var(--surface);
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 28px 0 8px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 28px; color: var(--cyan); opacity: 0.9;">{icon}</div>
            <div>
                <div style="font-family: var(--heading); font-size: 16.5px; color: var(--text); font-weight: 600; margin-bottom: 4px;">{title}</div>
                <div style="font-family: var(--sans); font-size: 14px; color: var(--text-muted); line-height: 1.5;">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# =====================================================
# INFO CARD
# =====================================================

def info_card(
    title,
    value,
    color="var(--copper)"
):

    st.markdown(
        f"""
        <div class="lmi-card" style="text-align:center;">
            <div class="lmi-quote-label" style="justify-content:center;">{title}</div>
            <div class="lmi-quote-value" style="color:{color};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# INPUT SUMMARY CARD
# =====================================================

def laptop_summary_card(
    laptop_information,
    title="Laptop Details"
):

    if title:
        section_header(title)

    items = list(laptop_information.items())

    midpoint = (len(items) + 1) // 2

    left = items[:midpoint]
    right = items[midpoint:]

    col1, col2 = st.columns(2)

    def _render_column(pairs):
        # Flattened into a single line to prevent Streamlit from breaking on newlines
        rows = "".join(
            f'<div class="lmi-card-row"><span class="lmi-card-row-label">{str(key).replace("_", " ")}</span><span class="lmi-card-row-value">{value}</span></div>'
            for key, value in pairs
        )

        import streamlit as st
        st.markdown(f'<div class="lmi-card">{rows}</div>', unsafe_allow_html=True)

    with col1:
        _render_column(left)

    with col2:
        _render_column(right)

# =====================================================
# SECTION HEADER
# =====================================================

def section_header(
    title,
    subtitle="",
    right=""
):

    subtitle_html = (
        f'<div class="lmi-section-subtitle">{subtitle}</div>'
        if subtitle else ""
    )

    right_html = (
        f'<div class="lmi-section-subtitle">{right}</div>'
        if right else ""
    )

    # Packed into a single string so the Markdown parser cannot break on empty lines
    html_str = f'<div class="lmi-section"><div><div class="lmi-section-title">{title}</div>{subtitle_html}</div>{right_html}</div>'

    import streamlit as st
    st.markdown(html_str, unsafe_allow_html=True)

# =====================================================
# STATUS CARD
# =====================================================

def status_card(
    text,
    success=True
):

    if success:
        st.success(text)
    else:
        st.error(text)


# =====================================================
# STAT STRIP
# A row of ruled ticker cells - used under the hero and for
# quick session summaries. `tone` colors the value: "on" (sage),
# "off" (brick), or default (plain text).
# =====================================================

# =====================================================
# STAT STRIP
# =====================================================

def stat_strip(stats):
    """
    stats: list of dicts, each with keys: label, value, and
    optional tone ("on" | "off" | None).
    """

    cells = "".join(
        f'<div class="lmi-stat"><div class="lmi-stat-label">{s["label"]}</div><div class="lmi-stat-value {s.get("tone", "") or ""}">{s["value"]}</div></div>'
        for s in stats
    )

    st.markdown(
        f'<div class="lmi-stat-strip">{cells}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# STEP LIST
# =====================================================

def step_list(steps):
    """
    steps: list of dicts with keys: title, desc
    """

    rows = "".join(
        f'<div class="lmi-step"><div class="lmi-step-index">{i:02d}</div><div><div class="lmi-step-body-title">{s["title"]}</div><div class="lmi-step-body-desc">{s["desc"]}</div></div></div>'
        for i, s in enumerate(steps, start=1)
    )

    st.markdown(
        f'<div class="lmi-steps">{rows}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# EMPTY STATE
# =====================================================

def empty_state(icon, title, desc):

    st.markdown(
        f"""
        <div class="lmi-empty">
            <div class="lmi-empty-icon">{icon}</div>
            <div class="lmi-empty-title">{title}</div>
            <div class="lmi-empty-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# BREADCRUMB / WORKFLOW POSITION
# =====================================================

def workflow_crumb(steps, active_index):
    """
    steps: list of short strings, e.g. ["Prediction", "Recommendations", "Explainability"]
    active_index: 0-based index of the current step
    """

    parts = []

    for i, step in enumerate(steps):

        cls = "active" if i == active_index else ""

        parts.append(f'<span class="{cls}">{step}</span>')

        if i < len(steps) - 1:
            parts.append('<span class="sep">→</span>')

    st.markdown(
        f'<div class="lmi-crumb">{"".join(parts)}</div>',
        unsafe_allow_html=True
    )
