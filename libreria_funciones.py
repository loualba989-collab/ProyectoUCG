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

    st.title("📈 Visualizaciones e Interpretación de Resultados")

    # =====================================================
    # HISTOGRAMA
    # =====================================================

    st.subheader(
        "Distribución de la Lactancia Materna Exclusiva"
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

    st.info("""
    Interpretación:
    Este gráfico muestra cómo se distribuyen los meses de lactancia materna exclusiva en la población analizada.
    Permite identificar los valores más frecuentes y observar si existen concentraciones o dispersión en la duración de la lactancia.
    """)

    # =====================================================
    # REGION
    # =====================================================

    st.subheader(
        "Lactancia Materna Exclusiva por Región"
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

    region_prom = (
        df.groupby("region")
        ["meses_lactancia_exclusiva"]
        .mean()
    )

    region_max = region_prom.idxmax()

    st.info(
        f"""
        Interpretación:
        El gráfico permite comparar la distribución de la lactancia materna exclusiva entre regiones.
        La región con mayor promedio de lactancia es: {region_max}.
        """
    )

    # =====================================================
    # AREA
    # =====================================================

    st.subheader(
        "Lactancia Materna Exclusiva por Área de Residencia"
    )

    fig3 = GraficoFactory.crear_grafico(
        "boxplot",
        df=df,
        x="area_residencia",
        y="meses_lactancia_exclusiva",
        color="area_residencia",
        title="Lactancia según Área de Residencia"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.info("""
    Interpretación:
    Este gráfico permite identificar diferencias entre áreas urbanas y rurales respecto a la duración de la lactancia materna exclusiva.
    Las diferencias observadas pueden estar asociadas a factores sociales, económicos o culturales.
    """)

    # =====================================================
    # FORMULA
    # =====================================================

    st.subheader(
        "Lactancia Materna según Consumo de Fórmula"
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

    st.info("""
    Interpretación:
    Este gráfico explora la relación entre el uso de fórmula infantil y la duración de la lactancia materna exclusiva.
    Los resultados muestran asociaciones descriptivas y no implican causalidad directa.
    """)

    # =====================================================
    # MADRES QUE TRABAJAN - PASTEL
    # =====================================================

    st.subheader(
        "Distribución de Madres que Trabajan"
    )

    trabajo_df = (
        df["madre_trabaja"]
        .value_counts()
        .reset_index()
    )

    trabajo_df.columns = [
        "madre_trabaja",
        "cantidad"
    ]

    fig5 = px.pie(
        trabajo_df,
        names="madre_trabaja",
        values="cantidad",
        title="Proporción de Madres que Trabajan"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.info("""
    Interpretación:
    Este gráfico muestra la proporción de madres que trabajan y aquellas que no trabajan dentro de la muestra analizada.
    Permite conocer la composición de la población estudiada.
    """)

    # =====================================================
    # COMPARACION TRABAJO VS LACTANCIA
    # =====================================================

    st.subheader(
        "Promedio de Lactancia según Condición Laboral"
    )

    promedio_trabajo = (
        df.groupby("madre_trabaja")
        ["meses_lactancia_exclusiva"]
        .mean()
        .reset_index()
    )

    fig6 = px.bar(
        promedio_trabajo,
        x="madre_trabaja",
        y="meses_lactancia_exclusiva",
        color="madre_trabaja",
        title="Promedio de Meses de Lactancia según Condición Laboral"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    grupo_mayor = promedio_trabajo.loc[
        promedio_trabajo[
            "meses_lactancia_exclusiva"
        ].idxmax()
    ]

    st.success(
        f"El grupo con mayor promedio de lactancia materna exclusiva es: "
        f"{grupo_mayor['madre_trabaja']} "
        f"con {round(grupo_mayor['meses_lactancia_exclusiva'],2)} meses."
    )

    st.info("""
    Interpretación:
    La comparación permite evaluar si la condición laboral de la madre está asociada con diferencias en la duración promedio de la lactancia materna exclusiva.
    Este resultado constituye un análisis exploratorio y puede servir como base para estudios más profundos.
    """)

# ======================================
# PAGINA ANALISIS
# ======================================

def page_analisis():

    st.title("📊 Análisis de Resultados")

    st.markdown("""
    En esta sección se presentan indicadores descriptivos y hallazgos obtenidos a partir del análisis exploratorio del dataset relacionado con la lactancia materna exclusiva en Ecuador.
    """)

    # =====================================================
    # INDICADORES PRINCIPALES
    # =====================================================

    promedio_lme = round(
        df["meses_lactancia_exclusiva"].mean(),
        2
    )

    max_lme = round(
        df["meses_lactancia_exclusiva"].max(),
        2
    )

    min_lme = round(
        df["meses_lactancia_exclusiva"].min(),
        2
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Promedio",
            promedio_lme
        )

    with col2:

        st.metric(
            "Máximo",
            max_lme
        )

    with col3:

        st.metric(
            "Mínimo",
            min_lme
        )

    st.info("""
    Interpretación:
    Los indicadores resumen permiten conocer el comportamiento general de la lactancia materna exclusiva dentro de la población analizada.
    """)

    # =====================================================
    # ANALISIS POR REGION
    # =====================================================

    st.subheader(
        "Análisis por Región"
    )

    region_prom = (
        df.groupby("region")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        region_prom
    )

    region_max = region_prom.idxmax()

    st.success(
        f"La región con mayor promedio de lactancia materna exclusiva es: {region_max}"
    )

    st.info("""
    Interpretación:
    Las diferencias entre regiones pueden estar asociadas a factores culturales, económicos, sociales y de acceso a servicios de salud.
    """)

    # =====================================================
    # ANALISIS POR AREA
    # =====================================================

    st.subheader(
        "Análisis por Área de Residencia"
    )

    area_prom = (
        df.groupby("area_residencia")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        area_prom
    )

    area_max = area_prom.idxmax()

    st.success(
        f"El área con mayor promedio de lactancia materna exclusiva es: {area_max}"
    )

    st.info("""
    Interpretación:
    El área de residencia puede influir en las prácticas de alimentación infantil debido a diferencias en estilos de vida y acceso a información.
    """)

    # =====================================================
    # ANALISIS MADRE TRABAJA
    # =====================================================

    st.subheader(
        "Análisis según Condición Laboral"
    )

    trabajo_prom = (
        df.groupby("madre_trabaja")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        trabajo_prom
    )

    trabajo_max = trabajo_prom.idxmax()

    st.success(
        f"El grupo con mayor promedio de lactancia corresponde a: {trabajo_max} la madre trabaja"
    )

    st.info("""
    Interpretación:
    La condición laboral de la madre puede influir en la continuidad de la lactancia materna exclusiva.
    Este análisis permite observar diferencias descriptivas entre grupos.
    """)

    # =====================================================
    # ANALISIS FORMULA INFANTIL
    # =====================================================

    st.subheader(
        "Análisis según Consumo de Fórmula"
    )

    formula_prom = (
        df.groupby("consume_formula")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        formula_prom
    )

    formula_max = formula_prom.idxmax()

    st.success(
        f"El grupo con mayor promedio de consumo de leche de formula se da a los 42.22 meses"
    )

    st.info("""
    Interpretación:
    El consumo de fórmula infantil puede estar relacionado con cambios en las prácticas de lactancia.
    Los resultados presentados son exploratorios y descriptivos.
    """)

    # =====================================================
    # RANKING PROVINCIAS
    # =====================================================

    st.subheader(
        "Ranking de Provincias"
    )

    ranking = (
        df.groupby("provincia")
        ["meses_lactancia_exclusiva"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        ranking
    )

    st.info("""
    Interpretación:
    El ranking provincial permite identificar territorios con mayores y menores promedios de lactancia materna exclusiva.
    """)

    # =====================================================
    # HALLAZGOS PRINCIPALES
    # =====================================================

    st.subheader(
        "Hallazgos Principales"
    )

    st.markdown(f"""
    
# ======================================
# PAGINA CONCLUSIONES
# ======================================

def page_conclusiones():

    st.title(
        "📝 Conclusiones"
    )

    st.markdown("""
    ### Conclusiones

    - Duración de Lactancia Materna Exclusiva: El promedio de meses de lactancia materna exclusiva es de aproximadamente 33.18 meses.

    - Factores Geográficos: La región `Costa` y el área `Urbana` muestran un promedio de LME más alto en comparación con 
      `Sierra` y `Amazonía`, y el área `Rural` respectivamente.

    - Madres Trabajadoras: Contrario a algunas percepciones, las madres que trabajan muestran un promedio de Lactancia Materna Exclusiva más alto. 
      Esto podría deberse a diversos factores, como un mayor nivel educativo, acceso a información o la posibilidad de permiso de lactancia y licencias 
      de maternidad (en los casos donde estos datos están completos).
      
    - Licencia de Maternidad: Las madres con licencia de maternidad tienen una duración de Lactancia Materna Exclusiva significativamente mayor, 
      lo que subraya la importancia de estas políticas de apoyo.

    - Uso de Fórmula: El análisis exploratorio sugiere que el uso de fórmula no está asociado con una menor Lactancia Materna Exclusiva.
      

    ### Recomendaciones

    - Fortalecer programas de promoción de lactancia materna.

    - Impulsar políticas de apoyo a madres trabajadoras.

    - Continuar desarrollando estudios basados en evidencia utilizando herramientas de Ciencia de Datos.
    """)
