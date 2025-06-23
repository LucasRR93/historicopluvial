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

def TabelaEst (dtselect):
    return df[(df['data']>=dtselect[0]) & (df['data']<=dtselect[1])].drop(['codEstacao', 'datahora'], axis=1).groupby(['nomeEstacao', 'latitude', 'longitude', 'data']).sum().reset_index()

def TabMedias (dtselect):
    dfMean = df[(df['data']>=dtselect[0]) & (df['data']<=dtselect[1])].drop(['codEstacao', 'datahora', 'data'], axis=1).groupby(['nomeEstacao', 'latitude', 'longitude']).mean().reset_index()
    dfMean['valorMedida'] = (dfMean['nomeEstacao'] + "\n" + dfMean['valorMedida'].round(2).astype(str))
    return dfMean


st.title('Histórico de chuva em São Paulo')



dtselect = st.date_input("Escolha o período: ", value=(primeiro,ultimo), min_value=primeiro, max_value=ultimo)


st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=-22.5,
            longitude=-48.50,
            zoom=5.5,
            #pitch=50,
        ),
        layers=[
            pdk.Layer(
                "TextLayer",
                data=TabMedias(dtselect)[['latitude', 'longitude', 'nomeEstacao', 'valorMedida']],
                get_position=['longitude','latitude'],
                get_text='valorMedida',
                get_size=13,
                get_color=[0,0,0],
                background=True,
                get_background_color=[21, 124, 179],
                background_padding=[5,5,5,5],
                tooltip='nomeEstacao'
            )
        ],
        
    )
)

st.dataframe(TabelaEst.rename(columns={'valorMedida':'Precipitação (mm)', 'nomeEstacao':'Nome Estação', 'latitude':'Latitude', 'longitude':'Longitude','data':'Data'}), use_container_width=True)

#ref
# referencia das opções de texto do TextLayer https://rdrr.io/github/anthonynorth/rdeck/man/text_layer.html