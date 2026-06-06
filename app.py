import streamlit as st

from libreria_funciones import (
    page_inicio,
    page_visualizaciones,
    page_analisis,
    page_conclusiones
)

st.set_page_config(
    page_title="Lactancia Materna Ecuador",
    page_icon="🍼",
    layout="wide"
)

st.sidebar.title("Menú")

menu = st.sidebar.radio(
    "Seleccione una opción",
    [
        "Inicio",
        "Visualizaciones",
        "Análisis",
        "Conclusiones"
    ]
)

if menu == "Inicio":
    page_inicio()

elif menu == "Visualizaciones":
    page_visualizaciones()

elif menu == "Análisis":
    page_analisis()

elif menu == "Conclusiones":
    page_conclusiones()
