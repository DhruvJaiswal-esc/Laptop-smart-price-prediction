import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import (
    SURFACE_COLOR, RULE_COLOR, TEXT_COLOR, TEXT_MUTED,
    POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR, GRID_COLOR,
    FONT_MONO, FONT_HEADING,
)

POSITIVE_SCALE = ["#111122", POSITIVE_COLOR]
NEGATIVE_SCALE = ["#111122", NEGATIVE_COLOR]


def _apply_theme(fig, title=None, height=440):
    fig.update_layout(
        title=dict(text=title, font=dict(family=FONT_HEADING, size=16, color=TEXT_COLOR), x=0) if title else None,
        template=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_MONO, size=12, color=TEXT_MUTED),
        height=height,
        margin=dict(r=60, t=52 if title else 24, b=24),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED), title=None),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR), automargin=True, title=None),
        colorway=[NEUTRAL_COLOR, POSITIVE_COLOR, NEGATIVE_COLOR],
        bargap=0.28,
    )
    return fig


def shap_feature_importance(shap_result):
    if not shap_result:
        return None
    df = pd.DataFrame(shap_result["top_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", text="impact", color_discrete_sequence=[NEUTRAL_COLOR])
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", marker_line_width=0, marker_color=NEUTRAL_COLOR, opacity=0.85)
    return _apply_theme(fig, title="What Mattered Most", height=480)


def shap_positive_chart(shap_result):
    if not shap_result:
        return None
    df = pd.DataFrame(shap_result["positive_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", color="impact", color_continuous_scale=POSITIVE_SCALE)
    fig.update_traces(marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return _apply_theme(fig, title="Pushed the Price Up")


def shap_negative_chart(shap_result):
    if not shap_result:
        return None
    df = pd.DataFrame(shap_result["negative_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", color="impact", color_continuous_scale=NEGATIVE_SCALE)
    fig.update_traces(marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return _apply_theme(fig, title="Pushed the Price Down")


def lime_feature_importance(lime_result):
    if not lime_result:
        return None
    df = pd.DataFrame(lime_result["top_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", text="impact", color_discrete_sequence=[NEUTRAL_COLOR])
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", marker_line_width=0, marker_color=NEUTRAL_COLOR, opacity=0.85)
    return _apply_theme(fig, title="What Mattered Most (Double-Check)", height=480)


def lime_positive_chart(lime_result):
    if not lime_result:
        return None
    df = pd.DataFrame(lime_result["positive_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", color="impact", color_continuous_scale=POSITIVE_SCALE)
    fig.update_traces(marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return _apply_theme(fig, title="Pushed the Price Up")


def lime_negative_chart(lime_result):
    if not lime_result:
        return None
    df = pd.DataFrame(lime_result["negative_features"])
    fig = px.bar(df, x="impact", y="feature", orientation="h", color="impact", color_continuous_scale=NEGATIVE_SCALE)
    fig.update_traces(marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return _apply_theme(fig, title="Pushed the Price Down")


def contribution_donut(positive, negative):
    fig = go.Figure(data=[go.Pie(
        labels=["Positive", "Negative"], values=[positive, negative],
        hole=0.72, marker=dict(colors=[POSITIVE_COLOR, NEGATIVE_COLOR]),
        textfont=dict(family=FONT_MONO, color=TEXT_COLOR)
    )])
    return _apply_theme(fig, title="Up vs. Down", height=380)


def waterfall_chart(features, values):
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=["relative"] * len(values),
        x=features, y=values,
        increasing=dict(marker=dict(color=POSITIVE_COLOR)),
        decreasing=dict(marker=dict(color=NEGATIVE_COLOR)),
        connector=dict(line=dict(color=RULE_COLOR))
    ))
    return _apply_theme(fig, title="How Each Detail Changed the Price", height=480)


def show_plot(figure, use_container_width=True):
    if figure is not None:
        import streamlit as st
        st.plotly_chart(figure, use_container_width=use_container_width, config={"displayModeBar": False})
