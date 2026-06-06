import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ======================================
# CLASE DATASET (POO)
# ======================================

@st.cache_data(show_spinner=False)
def cargar_datos(_self):

    try:

        df_loaded = pd.read_excel(
            _self.filepath
        )

        # Imputación de valores nulos

        df_loaded["permiso_lactancia"] = (
            df_loaded["permiso_lactancia"]
            .fillna("Sin información")
        )

        df_loaded["licencia_maternidad"] = (
            df_loaded["licencia_maternidad"]
            .fillna("Sin información")
        )

        df_loaded["dispone_lactario"] = (
            df_loaded["dispone_lactario"]
            .fillna("Sin información")
        )

        _self.df = df_loaded

        return df_loaded

    except Exception as e:

        st.error(
            f"Error al cargar datos: {e}"
        )

        return None
        
# ======================================
# PATRÓN FACTORY
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
# CARGA DATASET
# ======================================

DATA_PATH = "lactancia_analisis.xlsx"

dataset_instance = DatasetLactancia(
    DATA_PATH
)

df_original = dataset_instance.cargar_datos()

# ======================================
# FILTROS
# ======================================

st.sidebar.header(
    "Filtros"
)

region = st.sidebar.selectbox(
    "Seleccione Región",
    ["Todas"] +
    sorted(
        df_original["region"]
        .dropna()
        .unique()
        .tolist()
    )
)

if region == "Todas":

    df = df_original.copy()

else:

    df = df_original[
        df_original["region"] == region
    ]

# ======================================
# PAGINA INICIO
# ======================================

def page_inicio():

    st.image(
        "ENDI_LOGO.png",
        width=250
    )

    st.title(
        "🍼 Factores asociados a la Lactancia Materna Exclusiva en Ecuador"
    )

    st.markdown("""
    Esta aplicación presenta un análisis exploratorio de datos basado en la Encuesta Nacional sobre Desnutrición Infantil (ENDI).

    El objetivo es identificar factores asociados a la duración de la lactancia materna exclusiva en Ecuador mediante técnicas de Ciencia de Datos, Programación Orientada a Objetos y visualización interactiva.
    """)

    st.subheader(
        "Indicadores Generales"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Registros",
            len(df)
        )

    with col2:

        st.metric(
            "Variables",
            len(df.columns)
        )

    with col3:

        st.metric(
            "Promedio LME",
            round(
                df["meses_lactancia_exclusiva"].mean(),
                2
            )
        )

    st.success(
        f"Filtro activo: {region}"
    )

    st.subheader(
        "Vista previa del Dataset"
    )

    st.dataframe(
        df.head()
    )

    st.subheader(
        "Variables Analizadas"
    )

    st.write(
        list(df.columns)
    )

# ======================================
# PAGINA VISUALIZACIONES
# ======================================

def page_visualizaciones():

    st.title(
        "📈 Visualizaciones Interactivas"
    )

    st.success(
        f"Filtro activo: {region}"
    )

    # ======================================
    # HISTOGRAMA
    # ======================================

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

    promedio_lme = round(
        df["meses_lactancia_exclusiva"].mean(),
        2
    )

    st.info(
        f"""
        Interpretación:

        La duración promedio de la lactancia materna exclusiva es de {promedio_lme} meses.

        Este gráfico permite observar cómo se distribuyen los registros y detectar concentraciones de casos.
        """
    )

    # ======================================
    # REGION
    # ======================================

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
        .sort_values(
            ascending=False
        )
    )

    region_max = region_prom.idxmax()

    st.info(
        f"""
        Interpretación:

        La región con mayor promedio de lactancia materna exclusiva es:

        {region_max}
        """
    )

    # ======================================
    # AREA
    # ======================================

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

    st.info(
        """
        Interpretación:

        Este gráfico permite comparar los meses de lactancia entre zonas urbanas y rurales.
        """
    )

    # ======================================
    # FORMULA
    # ======================================

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

    st.info(
        """
        Interpretación:

        Este análisis explora la relación entre el consumo de fórmula infantil y la duración de la lactancia materna exclusiva.
        """
    )

    # ======================================
    # USO BIBERON
    # ======================================

    st.subheader(
        "Uso de Biberón"
    )

    biberon_df = (
        df["uso_biberon"]
        .value_counts()
        .reset_index()
    )

    biberon_df.columns = [
        "uso_biberon",
        "cantidad"
    ]

    fig_biberon = px.pie(
        biberon_df,
        names="uso_biberon",
        values="cantidad",
        title="Proporción de Uso de Biberón"
    )

    st.plotly_chart(
        fig_biberon,
        use_container_width=True
    )

    st.info(
        """
        Interpretación:

        El gráfico muestra la proporción de niños que utilizan biberón dentro de la población analizada.
        """
    )

    # ======================================
    # MADRES TRABAJADORAS
    # ======================================

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

    st.info(
        """
        Interpretación:

        Permite identificar la composición laboral de las madres incluidas en el estudio.
        """
    )

    # ======================================
    # TRABAJO VS LACTANCIA
    # ======================================

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
        title="Promedio de Lactancia según Condición Laboral"
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
        f"""
        El grupo con mayor promedio de lactancia corresponde a:

        {grupo_mayor['madre_trabaja']}

        con

        {round(grupo_mayor['meses_lactancia_exclusiva'],2)}

        meses.
        """
    )

    # ======================================
    # EXPLORADOR DINAMICO
    # ======================================

    st.subheader(
        "Explorador Interactivo"
    )

    variable = st.selectbox(
        "Seleccione una variable",
        [
            "region",
            "area_residencia",
            "madre_trabaja",
            "consume_formula",
            "uso_biberon"
        ]
    )

    resumen = (
        df.groupby(variable)
        ["meses_lactancia_exclusiva"]
        .mean()
        .reset_index()
    )

    fig_dynamic = px.bar(
        resumen,
        x=variable,
        y="meses_lactancia_exclusiva",
        color=variable,
        title=f"Promedio de Lactancia según {variable}"
    )

    st.plotly_chart(
        fig_dynamic,
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

    minimo = round(
        df["meses_lactancia_exclusiva"].min(),
        2
    )

    maximo = round(
        df["meses_lactancia_exclusiva"].max(),
        2
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Promedio",
            promedio
        )

    with col2:
        st.metric(
            "Mínimo",
            minimo
        )

    with col3:
        st.metric(
            "Máximo",
            maximo
        )

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

    provincia_max = ranking.idxmax()

    st.success(
        f"La provincia con mejor promedio es: {provincia_max}"
    )

    st.subheader(
        "Hallazgos Principales"
    )

    st.success(
        f"Promedio general de lactancia: {promedio} meses."
    )

    st.success(
        f"Provincia líder: {provincia_max}."
    )

    st.success(
        "Existen diferencias entre regiones y áreas de residencia."
    )

    st.success(
        "La condición laboral de la madre muestra diferencias en la duración promedio de lactancia."
    )

# ======================================
# PAGINA CONCLUSIONES
# ======================================

def page_conclusiones():

    st.title(
        "📝 Conclusiones"
    )

    promedio = round(
        df["meses_lactancia_exclusiva"].mean(),
        2
    )

    st.markdown(
        f"""

### Conclusiones

- El promedio general de lactancia materna exclusiva fue de **{promedio} meses**.

- Factores Geográficos: La región `Costa` y el área `Urbana` muestran un promedio de Lactancia Materna Exclusiva más alto en comparación con `Sierra` y `Amazonía`, y el área `Rural` respectivamente.

- Madres Trabajadoras: Contrario a algunas percepciones, las madres que trabajan muestran un promedio de Lactancia Materna Exclusiva más alto en este dataset. Esto podría deberse a diversos factores, como un mayor nivel educativo, acceso a información o la posibilidad de permiso de lactancia y licencias de maternidad (en los casos donde estos datos están completos).

- Licencia de Maternidad: Las madres con licencia de maternidad tienen una duración de Lactancia Materna Exclusiva significativamente mayor, lo que subraya la importancia de estas políticas de apoyo.

- Uso de Fórmula: El análisis exploratorio sugiere que el uso de fórmula no está asociado con una menor Lactancia Materna Exclusiva


### Recomendaciones

- Fortalecer programas de promoción de lactancia materna.

- Impulsar políticas de apoyo para madres trabajadoras.

- Continuar desarrollando análisis de Ciencia de Datos aplicados al área de salud pública.

- Incorporar modelos predictivos en futuras investigaciones.
"""
    )
