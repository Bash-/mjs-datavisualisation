import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from bokeh.plotting import figure
from make_plots import (
    matplotlib_plot,
    sns_plot,
    pd_plot,
    plotly_plot,
    altair_plot,
    bokeh_plot,
)


# can only set this once, first thing to set
st.set_page_config(layout="wide")

plot_types = (
    "Scatter",
    "Histogram",
    "Bar",
    "Line",
    "3D Scatter",
)  # maybe add 'Boxplot' after fixes
libs = (
    "Matplotlib",
    "Seaborn",
    "Plotly Express",
    "Altair",
    "Pandas Matplotlib",
    "Bokeh",
)

chart_type = st.selectbox("Grafiek type", plot_types)
sensor_id = st.text_input("Meetkastje id", value="742")

import pandas as pd
import requests

begin_date = '2020-01-01,00:00'
end_date = '2020-12-01,00:00'
# sensor_ids_utrecht = ['745','725','742','464','740','744','743','746','718','728','733','739','747','724','719','768','769','770','772','773','775','774','716','727']
# sensors = ','.join(sensor_ids_utrecht)
sensors = '742'

link = f'https://meetjestad.net/data/?type=sensors&ids={sensors}&begin={begin_date}&end={end_date}&format=json'

def load_data():
    r = requests.get(link)
    df = pd.DataFrame(r.json())
    print(df)

    df = df[['id', 'timestamp', 'temperature', 'humidity']]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.columns = ['id', 'ts', 'tmp', 'hum']
    df = df.groupby(['id', pd.Grouper(key='ts', freq='D')]).agg(['min', 'max', 'mean']).round(2)
    return df

def prepare_chart_data(df):
    df.columns = [f'{i}-{j}' for i, j in df.columns]
    df = df.reset_index()
    df['ts'] = df['ts'].astype(str)
    print(df)
    df.to_json('./chartdata.json', orient='records')
    

mjsdf = load_data()
copymjsdf = mjsdf.copy()
copymjsdf

# get data
# @st.cache(allow_output_mutation=True) # maybe source of resource limit issue
def load_penguin_data():
    return sns.load_dataset("penguins")


pens_df = load_penguin_data()
df = pens_df.copy()
df.index = pd.date_range(start="1/1/18", periods=len(df), freq="D")


with st.container():
    st.title("Meet Je Stad Data Visualisatie")
    st.header("Op deze pagina kan je experimenteren met de data van Meet Je Stad meetkastjes")


with st.container():
    st.subheader(f"Grafiek type geselecteerd:  {chart_type}")
    st.subheader(f"Meetkastje:  {sensor_id}")
    st.write("")

two_cols = st.checkbox("2 columns?", True)
if two_cols:
    col1, col2 = st.columns(2)


# create plots
def show_plot(kind: str):
    st.write(kind)
    if kind == "Matplotlib":
        plot = matplotlib_plot(chart_type, df)
        st.pyplot(plot)
    elif kind == "Seaborn":
        plot = sns_plot(chart_type, df)
        st.pyplot(plot)
    elif kind == "Plotly Express":
        plot = plotly_plot(chart_type, df)
        st.plotly_chart(plot, use_container_width=True)
    elif kind == "Altair":
        plot = altair_plot(chart_type, df)
        st.altair_chart(plot, use_container_width=True)
    elif kind == "Pandas Matplotlib":
        plot = pd_plot(chart_type, df)
        st.pyplot(plot)
    elif kind == "Bokeh":
        plot = bokeh_plot(chart_type, df)
        st.bokeh_chart(plot, use_container_width=True)


# output plots
with st.container():
    show_plot(kind="Plotly Express")

# display data
with st.container():
    show_data = st.checkbox("See the raw data?")

    if show_data:
        df

    # notes
    # st.subheader("Notes")
