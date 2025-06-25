import pandas as pd
import streamlit as st
import datetime as dt
import pydeck as pdk
import numpy as np
from pydeck.types import String

df = pd.read_csv('inmet.csv')
df['data'] = pd.to_datetime(df['data']).dt.date
primeiro = df['data'].min()
ultimo = df['data'].max()

st.set_page_config(layout='wide')
st.title('Histórico de chuva em São Paulo')

left_column, right_column = st.columns([2,1])

def df_Tabela(dtselect):
    tabela = df.drop(['ano', 'mes', 'latitude', 'longitude'], axis=1)
    tabela = tabela[(tabela['data']>=dtselect[0]) & (tabela['data']<=dtselect[1])]
    tabela = tabela.groupby(['nomeEstacao', 'codEstacao', 'coordenadas', 'data']).sum()
    tabela.rename(columns={'valorMedida':'Precipitação (mm)', 'nomeEstacao':'Nome Estação', 'coordenadas':'Coordenadas'}, inplace=True)
    return tabela

def df_Pontos(dtselect):
    tabela2 = df.drop(['ano', 'mes', 'coordenadas'], axis=1)
    tabela2 = tabela2[(tabela2['data']>=dtselect[0]) & (tabela2['data']<=dtselect[1])].drop(['data'], axis=1)
    tabela2 = tabela2.groupby(['nomeEstacao', 'latitude', 'longitude']).sum().reset_index()
    return tabela2

with right_column:
    dtselect = st.date_input("Escolha o período: ", value=(primeiro,ultimo), min_value=primeiro, max_value=ultimo)
    st.dataframe(df_Tabela(dtselect))

RaioAcao = pdk.Layer(
                "ScatterplotLayer",
                data=df_Pontos(dtselect),
                pickable=True,
                stroked=False,
                filled=True,
                radius_scale=1,
                line_width_min_pixels=1,
                get_position=['longitude','latitude'],
                get_radius=1000,
                get_fill_color=[25, 150, 217, 175],
            )
Ponto = pdk.Layer(
                "ScatterplotLayer",
                data=df_Pontos(dtselect),
                pickable=True,
                opacity=1,
                stroked=False,
                filled=True,
                radius_scale=1,
                radius_min_pixels=5,
                radius_max_pixels=10,
                line_width_min_pixels=1,
                get_position=['longitude','latitude'],
                get_radius=10,
                get_fill_color=[255, 75, 75],
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
            layers=[RaioAcao,Ponto],
            tooltip={"html": "<b>Estação:</b> {nomeEstacao} <br/> <b>Precipitação:</b> {valorMedida}","style": {"backgroundColor": "steelblue", "color": "white"}}            
        )
    )

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                #deckgl-wrapper {
                    height: 85vh !important
                }
        </style>
        """, unsafe_allow_html=True)