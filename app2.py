import pandas as pd
import streamlit as st
import datetime as dt
import pydeck as pdk
import numpy as np
from pydeck.types import String

df = pd.read_csv('db_pi.csv').drop(['Unnamed: 0'], axis=1)
df['data'] = pd.to_datetime(df['data']).dt.date
primeiro = df['data'].min()
ultimo = df['data'].max()

st.set_page_config(layout='wide')
st.title('Histórico de chuva em São Paulo')

left_column, right_column = st.columns([2,1])

def df_Tabela(dtselect):
    tabela = df
    tabela = tabela[(tabela['data']>=dtselect[0]) & (tabela['data']<=dtselect[1])]
    tabela = tabela.drop(['ano', 'mes', 'latitude', 'longitude', 'base'], axis=1)    
    tabela = tabela.groupby(['nomeEstacao', 'codEstacao', 'data']).sum()
    tabela.rename(columns={'valorMedida':'Precipitação (mm)', 'nomeEstacao':'Nome Estação'}, inplace=True)
    return tabela

def df_Pontos(dtselect):
    tabela2 = df
    tabela2 = tabela2[(tabela2['data']>=dtselect[0]) & (tabela2['data']<=dtselect[1])]
    tabela2 = tabela2.drop(['ano', 'mes','data', 'codEstacao', 'base'], axis=1)    
    tabela2 = tabela2.groupby(['nomeEstacao', 'latitude', 'longitude']).sum().reset_index()
    return tabela2.head(10)

with right_column:
    dtselect = st.date_input("Escolha o período: ", value=(primeiro,ultimo), min_value=primeiro, max_value=ultimo)
    st.dataframe(df_Tabela(dtselect))

Ponto = pdk.Layer(
                "ScatterplotLayer",
                data=df_Pontos(dtselect),
                pickable=True,
                opacity=1,
                stroked=False,
                filled=True,
                radius_scale=1,
                radius_min_pixels=5,
                radius_max_pixels=20,
                line_width_min_pixels=1,
                get_position=['longitude','latitude'],
                get_radius=20,
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
            layers=[Ponto],
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

st.dataframe(df_Pontos(dtselect))