import streamlit as st


# =====================================================
# PRICE REVEAL CARD
# =====================================================

def prediction_card(predicted_price, predicted_category):
    st.markdown(
        f"""
        <div class="price-reveal">
            <div class="price-cell">
                <div class="price-label">◈ Estimated Price</div>
                <div class="price-value">₹{predicted_price:,.0f}</div>
                <div class="price-sub">Our best estimate, in rupees</div>
            </div>
            <div class="price-cell">
                <div class="price-label">Category</div>
                <div class="price-value secondary">{predicted_category}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# RECOMMENDATION CARD
# =====================================================

def recommendation_card(brand, processor, gpu, category, rank=None):
    rank_html = f'<span class="rec-card-rank">#{rank:02d}</span>' if rank is not None else ""
    st.markdown(
        f"""
        <div class="rec-card">
            <div class="rec-card-head">
                <span class="rec-card-brand">{brand}</span>
                {rank_html}
            </div>
            <div class="rec-row">
                <span class="rec-row-label">Processor</span>
                <span class="rec-row-value">{processor}</span>
            </div>
            <div class="rec-row">
                <span class="rec-row-label">Graphics</span>
                <span class="rec-row-value">{gpu}</span>
            </div>
            <div class="rec-badge">{category}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# RECOMMENDATION GRID
# =====================================================

def recommendation_grid(recommendations):
    cols = st.columns(2)
    for index, rec in enumerate(recommendations):
        with cols[index % 2]:
            recommendation_card(
                rec["brand"], rec["processor"],
                rec["graphic_processor"], rec["category"],
                rank=index + 1
            )


# =====================================================
# FEATURE CARD (home page)
# =====================================================

def feature_card(icon, title, desc):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# SECTION HEADER
# =====================================================

def section_header(title, subtitle="", right=""):
    subtitle_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    right_html = f'<div class="section-sub">{right}</div>' if right else ""
    st.markdown(
        f'<div class="section-bar"><div><div class="section-title">{title}</div>{subtitle_html}</div>{right_html}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# STAT STRIP
# =====================================================

def stat_strip(stats):
    cells = "".join(
        f'<div class="stat-cell"><div class="stat-label">{s["label"]}</div><div class="stat-value {s.get("tone", "") or ""}">{s["value"]}</div></div>'
        for s in stats
    )
    st.markdown(f'<div class="stat-row">{cells}</div>', unsafe_allow_html=True)


# =====================================================
# STEP LIST
# =====================================================

def step_list(steps):
    rows = "".join(
        f'<div class="step-item"><div class="step-num">{i:02d}</div><div><div class="step-title">{s["title"]}</div><div class="step-desc">{s["desc"]}</div></div></div>'
        for i, s in enumerate(steps, start=1)
    )
    st.markdown(f'<div class="step-list">{rows}</div>', unsafe_allow_html=True)


# =====================================================
# EMPTY STATE
# =====================================================

def empty_state(icon, title, desc):
    st.markdown(
        f"""
        <div class="empty-box">
            <div class="empty-icon">{icon}</div>
            <div class="empty-title">{title}</div>
            <div class="empty-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# BREADCRUMB
# =====================================================

def workflow_crumb(steps, active_index):
    parts = []
    for i, step in enumerate(steps):
        cls = "active" if i == active_index else ""
        parts.append(f'<span class="{cls}">{step}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="sep">→</span>')
    st.markdown(f'<div class="crumb">{"".join(parts)}</div>', unsafe_allow_html=True)


# =====================================================
# LAPTOP SUMMARY CARD
# =====================================================

def laptop_summary_card(laptop_information, title="Laptop Details"):
    if title:
        section_header(title)
    items = list(laptop_information.items())
    midpoint = (len(items) + 1) // 2
    left, right = items[:midpoint], items[midpoint:]
    col1, col2 = st.columns(2)

    def _render_col(pairs):
        rows = "".join(
            f'<div class="rec-row"><span class="rec-row-label">{str(k).replace("_", " ")}</span><span class="rec-row-value">{v}</span></div>'
            for k, v in pairs
        )
        st.markdown(f'<div class="rec-card">{rows}</div>', unsafe_allow_html=True)

    with col1:
        _render_col(left)
    with col2:
        _render_col(right)
