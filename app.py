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

    st.header("Carga del dataset")

    archivo = st.file_uploader(
        "Seleccione un archivo Excel",
        type=["xlsx"]
    )

    if archivo is not None:

        df = pd.read_excel(archivo)

        st.success("Archivo cargado correctamente")

        st.dataframe(df.head())
