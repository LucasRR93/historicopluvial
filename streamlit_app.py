import pandas as pd
import streamlit as st
import datetime as dt
import pydeck as pdk
import numpy as np
from pydeck.types import String

df = pd.read_csv('inmet_filter.csv')
df['data'] = pd.to_datetime(df['datahora']).dt.date
primeiro = df['data'].min()
ultimo = df['data'].max()


def TabMedias (dtselect):
    dfMean = df[(df['data']>=dtselect[0]) & (df['data']<=dtselect[1])].drop(['codEstacao', 'datahora', 'data'], axis=1).groupby(['nomeEstacao', 'latitude', 'longitude']).sum().reset_index()
    dfMean['valorGrafico'] = (dfMean['nomeEstacao'] + "\n" + dfMean['valorMedida'].round(2).astype(str))
    return dfMean

st.set_page_config(layout='wide')
st.title('Histórico de chuva em São Paulo')

left_column, right_column = st.columns([2,1])

with right_column:
    dtselect = st.date_input("Escolha o período: ", value=(primeiro,ultimo), min_value=primeiro, max_value=ultimo)
    NewTable = TabMedias(dtselect)
    NewTable.rename(columns={'valorMedida':'Precipitação (mm)', 'nomeEstacao':'Nome Estação', 'latitude':'Latitude', 'longitude':'Longitude'}, inplace=True)
    st.dataframe(NewTable.drop(["valorGrafico"], axis=1), use_container_width=True)

TextLayer_ = pdk.Layer(
                "TextLayer",
                data=TabMedias(dtselect)[['latitude', 'longitude', 'nomeEstacao', 'valorGrafico']],
                get_position=['longitude','latitude'],
                get_text='valorGrafico',
                get_size=13,
                get_color=[0,0,0],
                background=True,
                get_background_color=[21, 124, 179],
                background_padding=[5,5,5,5]
            )

with left_column:
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=-22.5,
                longitude=-48.50,
                zoom=5.5,
                #pitch=50,
            ),
            layers=[TextLayer_],
            tooltip={"html": "<b>Elevation Value:</b> {elevationValue} <br/> <b>Color Value:</b> {colorValue}","style": {"backgroundColor": "steelblue", "color": "white"}}            
        )
    )