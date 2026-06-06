import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ======================================
# CLASE DATASET (POO)
# ======================================

class DatasetLactancia:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    @st.cache_data(show_spinner=False)
    def cargar_datos(_self):

        try:

            df_loaded = pd.read_excel(
                _self.filepath
            )

            _self.df = df_loaded

            return df_loaded

        except Exception as e:

            st.error(
                f"Error al cargar datos: {e}"
            )

            return None

    def dimensiones(self):

        if self.df is not None:
            return self.df.shape

        return None


# ======================================
# PATRON FACTORY
# ======================================

class GraficoFactory:

    @staticmethod
    def crear_grafico(
        tipo_grafico,
        df,
        x=None,
        y=None,
        color=None,
        title=""
    ):

        if tipo_grafico == "histograma":

            return px.histogram(
                df,
                x=x,
                color=color,
                title=title
            )

        elif tipo_grafico == "boxplot":

            return px.box(
                df,
                x=x,
                y=y,
                color=color,
                title=title
            )

        elif tipo_grafico == "barras":

            return px.bar(
                df,
                x=x,
                y=y,
                color=color,
                title=title
            )

        return None


# ======================================
# DATASET GLOBAL
# ======================================

DATA_PATH = "lactancia_analisis.xlsx"

dataset_instance = DatasetLactancia(
    DATA_PATH
)

df = dataset_instance.cargar_datos()


# ======================================
# PAGINA INICIO
# ======================================

def page_inicio():

    st.image(
        "ENDI_LOGO.png",
        width=250
    )

    st.title(
        "Factores asociados a la Lactancia Materna Exclusiva en Ecuador"
    )

    st.markdown("""
    La lactancia materna exclusiva constituye una práctica fundamental para la salud infantil y el desarrollo adecuado durante los primeros meses de vida.

    Este proyecto utiliza información proveniente de la Encuesta Nacional sobre Desnutrición Infantil (ENDI) para analizar factores asociados a la lactancia materna exclusiva en Ecuador.

    La aplicación fue desarrollada mediante Python y Streamlit, integrando conceptos de Ciencia de Datos, Programación Orientada a Objetos y visualización interactiva.
    """)

    st.subheader(
        "Objetivo del Proyecto"
    )

    st.info("""
    Analizar los factores asociados a la lactancia materna exclusiva en Ecuador mediante técnicas de análisis exploratorio de datos y visualización interactiva.
    """)

    st.subheader(
        "Información del Dataset"
    )

    st.write(
        f"Registros: {df.shape[0]}"
    )

    st.write(
        f"Variables: {df.shape[1]}"
    )

    st.dataframe(
        df.head()
    )


# ======================================
# PAGINA VISUALIZACIONES
# ======================================

def page_visualizaciones():

    st.title(
        "📈 Visualizaciones"
    )

    st.subheader(
        "Distribución de Lactancia Materna Exclusiva"
    )

    fig1 = GraficoFactory.crear_grafico(
        "histograma",
        df=df,
        x="meses_lactancia_exclusiva",
        title="Distribución de Meses de Lactancia"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader(
        "Lactancia por Región"
    )

    fig2 = GraficoFactory.crear_grafico(
        "boxplot",
        df=df,
        x="region",
        y="meses_lactancia_exclusiva",
        color="region",
        title="Lactancia según Región"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader(
        "Lactancia por Área"
    )

    fig3 = GraficoFactory.crear_grafico(
        "boxplot",
        df=df,
        x="area_residencia",
        y="meses_lactancia_exclusiva",
        color="area_residencia",
        title="Lactancia según Área"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.subheader(
        "Uso de Fórmula"
    )

    fig4 = GraficoFactory.crear_grafico(
        "boxplot",
        df=df,
        x="consume_formula",
        y="meses_lactancia_exclusiva",
        color="consume_formula",
        title="Lactancia según Consumo de Fórmula"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# ======================================
# PAGINA ANALISIS
# ======================================

def page_analisis():

    st.title(
        "📊 Análisis de Resultados"
    )

    promedio = round(
        df["meses_lactancia_exclusiva"].mean(),
        2
    )

    st.metric(
        "Promedio de meses de lactancia exclusiva",
        promedio
    )

    st.subheader(
        "Promedio por Región"
    )

    region_promedio = (
        df.groupby("region")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        region_promedio
    )

    st.subheader(
        "Promedio por Área"
    )

    area_promedio = (
        df.groupby("area_residencia")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        area_promedio
    )

    st.subheader(
        "Interpretación"
    )

    st.write("""
    Los resultados permiten identificar diferencias en la duración de la lactancia materna exclusiva entre regiones y áreas de residencia. Estas diferencias pueden estar asociadas a factores sociales, económicos y de acceso a servicios de salud.
    """)


# ======================================
# PAGINA CONCLUSIONES
# ======================================

def page_conclusiones():

    st.title(
        "📝 Conclusiones"
    )

    st.markdown("""
    ### Principales Hallazgos

    - La duración de la lactancia materna exclusiva presenta diferencias entre regiones del Ecuador.

    - El entorno geográfico y las características sociales pueden influir en la duración de la lactancia.

    - Variables como el uso de fórmula infantil y las condiciones laborales de la madre muestran patrones relevantes para futuras investigaciones.

    - La Ciencia de Datos permite transformar información estadística en conocimiento útil para la toma de decisiones.

    ### Recomendaciones

    - Fortalecer programas de promoción de lactancia materna.

    - Impulsar políticas de apoyo a madres trabajadoras.

    - Continuar desarrollando estudios basados en evidencia utilizando herramientas de Ciencia de Datos.
    """)
