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

st.sidebar.title(
    "Menú de Navegación"
)

selection = st.sidebar.radio(
    "Seleccione una opción",
    [
        "Inicio",
        "Visualizaciones",
        "Análisis",
        "Conclusiones"
    ]
)

if selection == "Inicio":

    page_inicio()

elif selection == "Visualizaciones":

    page_visualizaciones()

elif selection == "Análisis":

    page_analisis()

elif selection == "Conclusiones":

    page_conclusiones()
