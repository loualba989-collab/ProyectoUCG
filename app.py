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
