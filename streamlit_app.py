import pandas as pd
import streamlit as st
import datetime as dt
import pydeck as pdk
import numpy as np

df = pd.read_csv('inmet_filter.csv')
df['datahora'] = pd.to_datetime(df['datahora'])


primerio = df['datahora'].min().to_pydatetime()
ultimo = df['datahora'].max().to_pydatetime()

st.write()

st.pydeck_chart(
    pdk.Deck(        
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=-22.06981255406641,
            longitude=-48.433487601512546,
            zoom=6
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                auto_highlight=True,    
                get_color=[200,20,20],
                radius_scale=6000
            ),
            pdk.Layer(
                "TextLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_text="valorMedida",
                get_size=10000,
                get_color=[0,0,0],
            )
        ],
        tooltip={"text": "Elevation:"}
    )
)