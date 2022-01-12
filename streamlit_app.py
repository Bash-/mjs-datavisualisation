import streamlit as st
import pandas as pd
from mjs_plots import mjs_plot

# can only set this once, first thing to set
st.set_page_config(layout="wide")

with st.container():
    st.title("Meet Je Stad Data Visualisatie")
    st.header(
        "Op deze pagina kan je experimenteren met de data van Meet Je Stad meetkastjes"
    )

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

sensor_ids = [
    "745",
    "725",
    "742",
    "464",
    "740",
    "744",
    "743",
    "746",
    "718",
    "728",
    "733",
    "739",
    "747",
    "724",
    "719",
    "768",
    "769",
    "770",
    "772",
    "773",
    "775",
    "774",
    "716",
    "727",
]

chart_type = st.selectbox("Grafiek type", plot_types)
# sensor_id = st.text_input("Meetkastje id", value="742")
sensors_input = st.multiselect("Meetkastje ids", options=sensor_ids, default="742")

import pandas as pd
import requests

begin_date = "2020-01-01,00:00"
end_date = "2020-12-01,00:00"
# sensor_ids_utrecht = ['745','725','742','464','740','744','743','746','718','728','733','739','747','724','719','768','769','770','772','773','775','774','716','727']
# sensors = ','.join(sensor_ids_utrecht)
sensors = ",".join(sensors_input)

link = f"https://meetjestad.net/data/?type=sensors&ids={sensors}&begin={begin_date}&end={end_date}&format=json"


def load_data():
    r = requests.get(link)
    df = pd.DataFrame(r.json())

    df = df[["id", "timestamp", "temperature", "humidity"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.columns = ["id", "ts", "tmp", "hum"]
    df = (
        df.groupby(["id", pd.Grouper(key="ts", freq="D")])
        .agg(["min", "max", "mean"])
        .round(2)
    )
    return df


def prepare_chart_data(df):
    df.columns = [f"{i}_{j}" for i, j in df.columns]
    df = df.reset_index()
    df["ts"] = df["ts"].astype(str)
    return df


mjsdf = prepare_chart_data(load_data())
copymjsdf = mjsdf.copy()

# output plots
with st.container():
    plot = mjs_plot(chart_type, copymjsdf)
    st.plotly_chart(plot, use_container_width=True)

# notes
# st.subheader("Notes")
st.subheader("Ruwe data")
copymjsdf
