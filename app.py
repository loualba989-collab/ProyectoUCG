import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Lactancia Materna Ecuador",
    layout="wide"
)

# Cargar dataset una sola vez
@st.cache_data
def cargar_datos():
    return pd.read_excel("lactancia_analisis.xlsx")

df = cargar_datos()

# Menú lateral
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

# =========================
# PÁGINA INICIO
# =========================
if menu == "Inicio":

    st.title(
        "Factores asociados a la lactancia materna exclusiva en Ecuador"
    )

    st.image("ENDI_LOGO.png", width=250)

    st.write("""
    Proyecto final de Ciencia de Datos utilizando información de la
    Encuesta Nacional sobre Desnutrición Infantil (ENDI).
    """)

# =========================
# PÁGINA CARGA DE DATOS
# =========================
elif menu == "Carga de datos":

    st.header("Dataset utilizado")

    st.success("Dataset cargado correctamente")

    st.write("Número de registros:", df.shape[0])
    st.write("Número de variables:", df.shape[1])

    st.dataframe(df.head())

# =========================
# PÁGINA VISUALIZACIONES
# =========================
elif menu == "Visualizaciones":

    st.header("Visualizaciones")

    st.info(
        "Aquí agregaremos los gráficos de lactancia materna exclusiva."
    )

# =========================
# PÁGINA CONCLUSIONES
# =========================
elif menu == "Conclusiones":

    st.header("Conclusiones")

    st.write(
        "Aquí se presentarán las conclusiones obtenidas del análisis."
    )
