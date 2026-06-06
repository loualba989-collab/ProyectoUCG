import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Lactancia Materna Ecuador",
    layout="wide"
)

st.sidebar.title("Menú")

menu = st.sidebar.radio(
    "Seleccione una opción",
    [
        "Inicio",
        "Carga de datos",
        "Exploración",
        "Calidad de datos",
        "Visualizaciones",
        "Conclusiones"
    ]
)

# PAGINA INICIO
if menu == "Inicio":

    st.title(
        "Factores asociados a la lactancia materna exclusiva en Ecuador"
    )

    st.write("""
    Proyecto final de Ciencia de Datos utilizando información de la ENDI.
    """)

# PAGINA CARGA DE DATOS
elif menu == "Carga de datos":

    st.header("Dataset utilizado")

    df = pd.read_excel("Dataset Lactancia materna exclusiva ENDI")

    st.success("Dataset cargado correctamente")

    st.write("Número de registros:", df.shape[0])
    st.write("Número de variables:", df.shape[1])

    st.dataframe(df.head())

        df = pd.read_excel(archivo)

        st.success("Archivo cargado correctamente")

        st.dataframe(df.head())
