from turtle import width
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")
st.title('Incendios en Ucrania 2022',anchor='Incendios')
st.write('Esta app es un ejercicio en el que se representan los incendios en ucrania en el 2022 desde el 1 de enero hasta 9 de junio de 2022')
datos=pd.read_csv('.\datos\data.csv')
datos['Z']=0
datos['fecha']=pd.to_datetime(datos['ACQ_DATE'])
ancho=1800
fechas=st.sidebar.date_input(label='Rango de fechas',value=(datos['fecha'].min(),datos['fecha'].max()),
                            min_value=datos['fecha'].min(),max_value=datos['fecha'].max())
fechas=list(fechas)
if len(fechas)==1:
    fechas+=fechas

filtrado=datos.loc[(fechas[0]<=datos['fecha'].dt.date)&(datos['fecha'].dt.date<=fechas[1])]

fig = px.density_mapbox(filtrado, lat='LATITUDE', lon='LONGITUDE', z='Z', radius=10,
                        center=dict(lat=49, lon=31.8), zoom=5,
                        mapbox_style="stamen-terrain",animation_frame='ACQ_DATE',width=800,height=600)
fig.update_layout(height=900,width=ancho)
st.plotly_chart(fig,)
conteo=filtrado[['ACQ_DATE','LATITUDE','LONGITUDE']]
conteo=conteo.groupby('ACQ_DATE').count()
conteo.reset_index(inplace=True)
conteo.rename(columns={'LATITUDE':'Nº DE INCENDIOS'}, inplace = True)
fig2=px.line(data_frame=conteo, x='ACQ_DATE',y= 'Nº DE INCENDIOS',width=800,height=600)
fig2.update_layout(height=300,width=ancho)
st.plotly_chart(fig2,)
st.dataframe(filtrado[['ACQ_DATE','LATITUDE','LONGITUDE']])