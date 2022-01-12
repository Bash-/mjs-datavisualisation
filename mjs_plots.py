import plotly.express as px
import streamlit as st

data_fields = [
    "id",
    "ts",
    "tmp_min",
    "tmp_max",
    "tmp_mean",
    "hum_min",
    "hum_max",
    "hum_mean",
]


def mjs_plot(chart_type: str, df):
    """return plotly plots"""

    if chart_type == "Scatter":
        x_axis = st.selectbox("x-as", data_fields)
        y_axis = st.selectbox("y-as", data_fields, index=1)
        color = st.selectbox("Kleur", data_fields, index=2)

        fig = px.scatter(
            data_frame=df,
            x=x_axis,
            y=y_axis,
            color=color,
            title="Scatter plot",
        )
    elif chart_type == "Histogram":
        x_axis = st.selectbox("x-as", data_fields)

        fig = px.histogram(
            data_frame=df,
            x=x_axis,
            title="Histogram",
        )
    elif chart_type == "Bar":
        x_axis = st.selectbox("x-as", data_fields)
        y_axis = st.selectbox("y-as", data_fields, index=1)

        fig = px.histogram(data_frame=df, x=x_axis, y=y_axis, title="Bar chart")
        # by default shows stacked bar chart (sum) with individual hover values
    elif chart_type == "Boxplot":
        x_axis = st.selectbox("x-as", data_fields)
        y_axis = st.selectbox("y-as", data_fields, index=1)
        fig = px.box(data_frame=df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        x_axis = st.selectbox("x-as", data_fields, index=1)
        y_axis = st.selectbox("y-as", data_fields, index=2)
        color = st.selectbox("Kleur", data_fields, index=0)
        fig = px.line(
            data_frame=df,
            x=x_axis,
            y=y_axis,
            color=color,
            title="Line chart",

        )
    elif chart_type == "3D Scatter":
        x_axis = st.selectbox("x-as", data_fields)
        y_axis = st.selectbox("y-as", data_fields, index=1)
        z_axis = st.selectbox("y-as", data_fields, index=2)
        color = st.selectbox("kleur", data_fields, index=3)

        fig = px.scatter_3d(
            data_frame=df,
            x=x_axis,
            y=y_axis,
            z=z_axis,
            color=color,
            title="Interactive 3D Scatterplot!",
        )

    return fig
