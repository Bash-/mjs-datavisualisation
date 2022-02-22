import streamlit as st
import pandas as pd
from mjs_plots import mjs_plot
import datetime
import functools
import streamlit_parameters
import pydeck as pdk
from pydeck.types import String

import requests

# can only set this once, first thing to set
st.set_page_config(layout="wide")

with st.container():
    st.title("Meet Je Stad Data Visualisatie")
    st.header(
        "Op deze pagina kan je experimenteren met de data van Meet Je Stad meetkastjes"
    )

plot_types = (
    "Line",
    "Scatter",
    "Histogram",
    "Bar",
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
  "716", "717", "718", "719", "720", "721", "722", "723", "724", "725", "726", "727", "728", "729", "730", "733", "739", "740", "741", "742", "743", "744", "745", "746", "747", "748", "762", "763", "765", "766", "767", "768", "769", "770", "771", "772", "774", "775", "776", "777", "778", "779", "780", "781", "782", "873", "784", "785", "786", "787", "788", "789", "790", "791", "792", "793", "794", "795", "796", "832", "833", "834", "835", "838", "839", "840", "841", "842", "843", "864", "865", "866", "867", "868", "869", "870", "871", "872", "880", "881", "875", "877", "68", "2008", "2028",
]

parameters = streamlit_parameters.parameters.Parameters()

parameters.register_string_parameter(key="plot_type", default_value="Line")
parameters.register_string_list_parameter(key="sensor_ids", default_value="725")

parameters.register_date_parameter(
    key="start_date", default_value=datetime.datetime(2020, 1, 1)
)
parameters.register_date_parameter(
    key="end_date", default_value=datetime.datetime(2021, 12, 1)
)

chart_type = st.selectbox(
    label="Grafiek type",
    options=plot_types,
    index=plot_types.index(parameters.plot_type.value),
    key=parameters.plot_type.key,
    on_change=functools.partial(
        parameters.update_parameter_from_session_state,
        key=parameters.plot_type.key,
    ),
)


# sensor_id = st.text_input("Meetkastje id", value="742")
sensors_input = st.multiselect(
    label="Meetkastje ids",
    options=sensor_ids,
    default=parameters.sensor_ids.default,
    key=parameters.sensor_ids.key,
    on_change=functools.partial(
        parameters.update_parameter_from_session_state, key=parameters.sensor_ids.key
    ),
)

date_begin_input = st.date_input(
    "Startdatum",
    value=parameters.start_date.value,
    key=parameters.end_date.key,
    on_change=functools.partial(
        parameters.update_parameter_from_session_state, key=parameters.end_date.key
    ),
)
date_end_input = st.date_input(
    "Einddatum",
    value=parameters.end_date.value,
    key=parameters.end_date.key,
    on_change=functools.partial(
        parameters.update_parameter_from_session_state, key=parameters.end_date.key
    ),
)

date_begin = date_begin_input.strftime("%Y-%m-%d, %H:%M")
date_end = date_end_input.strftime("%Y-%m-%d, %H:%M")

# begin_date = "2020-01-01,00:00"
# end_date = "2020-12-01,00:00"
# sensor_ids_utrecht = ['745','725','742','464','740','744','743','746','718','728','733','739','747','724','719','768','769','770','772','773','775','774','716','727']
# sensors = ','.join(sensor_ids_utrecht)
sensors = ",".join(sensors_input)

link = f"https://meetjestad.net/data/?type=sensors&ids={sensors}&begin={date_begin}&end={date_end}&format=json"


def load_data():
    r = requests.get(link)
    df = pd.DataFrame(r.json())

    locationdf = df[df.columns.intersection(set(["id", "longitude", "latitude"]))]
    load_data.locationdf = locationdf.groupby(["id"], as_index=False).first()

    df = df[
        df.columns.intersection(
            set(["id", "timestamp", "temperature", "humidity", "pm2.5", "pm10"])
        )
    ]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # df.columns = ["id", "ts", "tmp", "hum", "pm2.5", "pm10"]
    df = (
        df.groupby(["id", pd.Grouper(key="timestamp", freq="D")])
        .agg(["min", "max", "mean"])
        .round(2)
    )
    return df


def prepare_chart_data(df):
    df.columns = [f"{i}_{j}" for i, j in df.columns]
    df = df.reset_index()
    df["timestamp"] = df["timestamp"].astype(str)
    return df


mjsdf = prepare_chart_data(load_data())
copymjsdf = mjsdf.copy()

# output plots
with st.container():
    plot = mjs_plot(chart_type, copymjsdf)
    parameters.set_url_fields()
    st.plotly_chart(plot, use_container_width=True)

TEXT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"  # noqa
extradf = pd.read_json(TEXT_LAYER_DATA)

load_data.locationdf["id"] = load_data.locationdf.id.apply(str)

computed_view = pdk.data_utils.compute_view(load_data.locationdf[["longitude", "latitude"]])

if (computed_view.zoom > 12):
    computed_view.zoom = 12

with st.container():
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-streets-v11",
            initial_view_state=computed_view,
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=load_data.locationdf,
                    get_position="[longitude, latitude]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    load_data.locationdf,
                    pickable=True,
                    get_position="[longitude, latitude]",
                    get_text="id",
                    get_size=14,
                    get_color=[0, 0, 0],
                    get_angle=0,
                    # Note that string constants in pydeck are explicitly passed as strings
                    # This distinguishes them from columns in a data set
                    get_text_anchor=String("middle"),
                    get_alignment_baseline=String("center"),
                ),
            ],
            tooltip={"html": "<b>Meetkastje: {id}</b>", "style": {"color": "white"}},
        )
    )

# notes
# st.subheader("Notes")
st.subheader("Ruwe data")
copymjsdf
