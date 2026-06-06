import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Clase DatasetLactancia (POO) ---
class DatasetLactancia:
    """Clase para encapsular la carga y operaciones básicas de un dataset de lactancia."""
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    @st.cache_data(show_spinner=False)
    def cargar_datos(_self):
        """Carga el dataset desde la ruta especificada al DataFrame, usando caché de Streamlit."""
        try:
            df_loaded = pd.read_excel(_self.filepath)
            # Opcional: Estandarizar nombres de columnas o codificar si es necesario
            _self.df = df_loaded
            return df_loaded
        except FileNotFoundError:
            st.error(f"Error: El archivo '{_self.filepath}' no fue encontrado. Asegúrate de que esté en la ubicación correcta.")
            return None
        except Exception as e:
            st.error(f"Ocurrió un error al cargar el archivo: {e}")
            return None

    def dimensiones(self):
        if self.df is not None:
            return self.df.shape
        return None

    def resumen(self):
        if self.df is not None:
            return self.df.info()
        return None

    def calcular_nulos_porcentaje(self):
        if self.df is not None:
            null_counts = self.df.isnull().sum()
            null_percentages = (self.df.isnull().sum() / len(self.df)) * 100
            null_summary = pd.DataFrame({
                'Conteo de Nulos': null_counts,
                'Porcentaje de Nulos (%)': null_percentages
            })
            return null_summary[null_summary['Conteo de Nulos'] > 0].sort_values(by='Porcentaje de Nulos (%)', ascending=False)
        return pd.DataFrame()

    def estadisticas_descriptivas_numericas(self):
        if self.df is not None:
            numerical_cols = self.df.select_dtypes(include=np.number).columns
            if not numerical_cols.empty:
                return self.df[numerical_cols].describe()
        return pd.DataFrame()

    def frecuencias_categoricas(self):
        if self.df is not None:
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            frequencies = {}
            for col in categorical_cols:
                frequencies[col] = self.df[col].value_counts(dropna=False)
            return frequencies
        return {}

# --- Patrón Factory para Gráficos ---
class GraficoFactory:
    """Clase Factory para crear diferentes tipos de gráficos usando Plotly Express."""

    @staticmethod
    def crear_grafico(tipo_grafico, df, x=None, y=None, color=None, title="", labels=None, **kwargs):
        if labels is None:
            labels = {}

        # Para asegurar que los DataFrames de conteo se manejen correctamente
        temp_df = df.copy()
        if (tipo_grafico == 'barras' or tipo_grafico == 'pastel') and y == 'Conteo' and x in temp_df.columns:
            counts_df = temp_df[x].value_counts().reset_index()
            counts_df.columns = [x, 'Conteo']
            temp_df = counts_df

        base_labels = {k: k.replace('_', ' ').title() for k in [x, y, color] if k is not None}
        final_labels = {**base_labels, **labels}

        if tipo_grafico == 'barras':
            if x is None or y is None:
                st.error("Para gráfico de barras se requieren 'x' y 'y'.")
                return None
            return px.bar(temp_df, x=x, y=y, color=color, title=title, labels=final_labels, template='plotly_white', **kwargs)

        elif tipo_grafico == 'pastel':
            if x is None or y is None:
                st.error("Para gráfico de pastel se requieren 'x' (nombres) y 'y' (valores).")
                return None
            return px.pie(temp_df, names=x, values=y, title=title, labels=final_labels, template='plotly_white', **kwargs)

        elif tipo_grafico == 'histograma':
            if x is None:
                st.error("Para histograma se requiere 'x'.")
                return None
            return px.histogram(df, x=x, color=color, title=title, labels=final_labels, template='plotly_white', **kwargs)

        elif tipo_grafico == 'boxplot':
            if x is None or y is None:
                st.error("Para boxplot se requieren 'x' y 'y'.")
                return None
            return px.box(df, x=x, y=y, color=color, title=title, labels=final_labels, template='plotly_white', **kwargs)

        else:
            st.warning(f"Tipo de gráfico no reconocido: {tipo_grafico}")
            return None

# --- Configuración de la aplicación Streamlit ---
st.set_page_config(
    page_title="Factores Lactancia Materna Exclusiva Ecuador",
    page_icon="🍼",
    layout="wide"
)

DATA_PATH = '/content/Dataset Lactancia materna exclusiva ENDI.xlsx'

@st.cache_resource
def get_dataset_instance(path):
    return DatasetLactancia(path)

dataset_instance = get_dataset_instance(DATA_PATH)
df = dataset_instance.cargar_datos()

# --- Funciones para cada página de la aplicación ---

def page_inicio():
    st.title("🍼 Factores asociados a la Lactancia Materna Exclusiva en Ecuador")
    st.header("Análisis Exploratorio y Visualización Interactiva")
    st.markdown("""
    Bienvenido a este proyecto universitario enfocado en identificar y visualizar los factores asociados a la lactancia materna exclusiva (LME) en Ecuador, utilizando datos de la Encuesta Nacional sobre Desnutrición Infantil (ENDI).

    **Objetivo:** Realizar un Análisis Exploratorio de Datos (EDA) para entender mejor el fenómeno de la LME y presentar los hallazgos de manera interactiva. Este proyecto integra conceptos de programación imperativa, funcional, orientada a objetos y patrones de diseño.

    Utiliza el menú de la izquierda para navegar por las diferentes secciones de la aplicación.
    """)

    st.subheader("Datos de Origen")
    st.write(f"El análisis se basa en el dataset: `{DATA_PATH}`")
    if df is not None:
        st.write(f"Dimensiones del dataset: {df.shape[0]} filas y {df.shape[1]} columnas.")
        st.dataframe(df.head())

def page_exploracion():
    st.title("🔍 Exploración del Dataset")
    st.markdown("En esta sección, podrás obtener una visión general de la estructura del dataset, sus dimensiones y los tipos de variables.")

    if df is not None:
        st.subheader("Dimensiones del DataFrame")
        st.write(f"El DataFrame tiene **{df.shape[0]} filas** (registros) y **{df.shape[1]} columnas** (variables).")

        st.subheader("Tipos de Variables")
        st.dataframe(df.dtypes.rename('Tipo de Dato'))

        st.subheader("Primeros y Últimos Registros")
        st.write("**Primeros 5 registros:**")
        st.dataframe(df.head())
        st.write("**Últimos 5 registros:**")
        st.dataframe(df.tail())

        st.subheader("Estadísticas Descriptivas para Variables Numéricas")
        st.dataframe(dataset_instance.estadisticas_descriptivas_numericas())

        st.subheader("Frecuencias de Variables Categóricas")
        st.markdown("A continuación se muestran las frecuencias de las categorías para cada variable categórica.")
        categorical_frequencies = dataset_instance.frecuencias_categoricas()
        for col, freq_series in categorical_frequencies.items():
            st.write(f"**Columna: {col}**")
            st.dataframe(freq_series)

def page_calidad_datos():
    st.title("📊 Calidad de Datos")
    st.markdown("En esta sección, evaluaremos la calidad del dataset, prestando especial atención a los valores nulos.")

    if df is not None:
        st.subheader("Valores Nulos por Columna")
        null_summary = dataset_instance.calcular_nulos_porcentaje()
        if not null_summary.empty:
            st.dataframe(null_summary)
            st.write("\n--- Interpretación ---")
            for index, row in null_summary.iterrows():
                st.write(f"La columna `**{index}**` tiene un **{row['Porcentaje de Nulos (%)']:.2f}%** de valores nulos.")
        else:
            st.info("¡Excelente! No se encontraron valores nulos en el dataset.")

def page_visualizaciones():
    st.title("📈 Visualizaciones Interactivas")
    st.markdown("Explora las relaciones y distribuciones clave a través de diferentes gráficos interactivos.")

    if df is not None:
        st.subheader("Distribución de la Lactancia Materna Exclusiva (LME)")
        fig_hist_lme = GraficoFactory.crear_grafico(
            'histograma',
            df=df,
            x='meses_lactancia_exclusiva',
            nbins=30,
            title='Distribución de Meses de Lactancia Materna Exclusiva',
            labels={'meses_lactancia_exclusiva': 'Meses de LME', 'count': 'Número de Casos'}
        )
        if fig_hist_lme: st.plotly_chart(fig_hist_lme, use_container_width=True)

        st.subheader("LME por Región y Área de Residencia")
        col1, col2 = st.columns(2)
        with col1:
            fig_box_region = GraficoFactory.crear_grafico(
                'boxplot',
                df=df,
                x='region',
                y='meses_lactancia_exclusiva',
                color='region',
                title='LME por Región',
                labels={'region': 'Región', 'meses_lactancia_exclusiva': 'Meses de LME'}
            )
            if fig_box_region: st.plotly_chart(fig_box_region, use_container_width=True)
        with col2:
            fig_box_area = GraficoFactory.crear_grafico(
                'boxplot',
                df=df,
                x='area_residencia',
                y='meses_lactancia_exclusiva',
                color='area_residencia',
                title='LME por Área de Residencia',
                labels={'area_residencia': 'Área', 'meses_lactancia_exclusiva': 'Meses de LME'}
            )
            if fig_box_area: st.plotly_chart(fig_box_area, use_container_width=True)

        st.subheader("Factores Sociodemográficos y LME")
        col3, col4 = st.columns(2)
        with col3:
            fig_box_trabajo = GraficoFactory.crear_grafico(
                'boxplot',
                df=df,
                x='madre_trabaja',
                y='meses_lactancia_exclusiva',
                color='madre_trabaja',
                title='LME si la Madre Trabaja',
                labels={'madre_trabaja': 'Madre Trabaja', 'meses_lactancia_exclusiva': 'Meses de LME'}
            )
            if fig_box_trabajo: st.plotly_chart(fig_box_trabajo, use_container_width=True)
        with col4:
            # Gráfico de barras para el uso de biberón
            fig_pie_biberon = GraficoFactory.crear_grafico(
                'pastel',
                df=df,
                x='uso_biberon',
                y='Conteo', 
                title='Proporción de Uso de Biberón',
                labels={'uso_biberon': 'Uso de Biberón'}
            )
            if fig_pie_biberon: st.plotly_chart(fig_pie_biberon, use_container_width=True)

        st.subheader("Asociación entre Uso de Fórmula y LME")
        fig_box_formula = GraficoFactory.crear_grafico(
            'boxplot',
            df=df,
            x='consume_formula',
            y='meses_lactancia_exclusiva',
            color='consume_formula',
            title='LME según Consumo de Fórmula',
            labels={'consume_formula': 'Consume Fórmula', 'meses_lactancia_exclusiva': 'Meses de LME'}
        )
        if fig_box_formula: st.plotly_chart(fig_box_formula, use_container_width=True)

def page_conclusiones():
    st.title("📝 Conclusiones y Recomendaciones")
    st.markdown("""
    Esta sección presenta las principales conclusiones extraídas del análisis exploratorio de datos y posibles recomendaciones.

    ### Conclusiones Clave:
    *   **Duración de LME:** El promedio de meses de lactancia materna exclusiva es de aproximadamente 33.18 meses.
    *   **Valores Nulos:** Columnas como `permiso_lactancia`, `licencia_maternidad` y `dispone_lactario` presentan un alto porcentaje de valores nulos, lo que sugiere que estas variables podrían requerir un tratamiento especial o no son aplicables a la mayoría de la población estudiada.
    *   **Factores Geográficos:** La región `Costa` y el área `Urbana` muestran un promedio de LME más alto en comparación con `Sierra` y `Amazonía`, y el área `Rural` respectivamente.
    *   **Madres Trabajadoras:** Contrario a algunas percepciones, las madres que trabajan muestran un promedio de LME más alto en este dataset. Esto podría deberse a diversos factores, como un mayor nivel educativo, acceso a información o la posibilidad de permiso de lactancia y licencias de maternidad (en los casos donde estos datos están completos).
    *   **Licencia de Maternidad:** Las madres con licencia de maternidad tienen una duración de LME significativamente mayor, lo que subraya la importancia de estas políticas de apoyo.
    *   **Uso de Fórmula:** El análisis exploratorio sugiere que el uso de fórmula no está asociado con una menor LME; de hecho, los grupos que reportan usar fórmula también muestran promedios más altos de LME. Este es un hallazgo que merece una investigación más profunda, ya que podría indicar que la fórmula se introduce en contextos de LME prolongada, o que la pregunta captura a un grupo con características distintas. No implica causalidad directa y requiere análisis multivariado.

    ### Recomendaciones:
    1.  **Investigación Profunda:** Los hallazgos sobre madres trabajadoras y uso de fórmula requieren un análisis causal y multivariado para descartar variables de confusión.
    2.  **Manejo de Nulos:** Para `permiso_lactancia`, `licencia_maternidad`, `dispone_lactario`, se recomienda imputación con categorías como 'No aplica' o 'Desconocido', o considerar la eliminación si el impacto en el análisis es mínimo.
    3.  **Políticas de Apoyo:** Reforzar las políticas de licencia de maternidad y crear programas de apoyo en el lugar de trabajo, especialmente en las regiones y áreas con menor promedio de LME.
    4.  **Concientización:** Campañas de concientización sobre los beneficios de la LME y cómo superar barreras comunes.
    """
)

# --- Lógica de navegación de Streamlit ---
# Usar un sidebar para la navegación
st.sidebar.title("Menú de Navegación")
selection = st.sidebar.radio(
    "Ir a:",
    ["Inicio", "Exploración del Dataset", "Calidad de Datos", "Visualizaciones", "Conclusiones"]
)

# Llamar a la función de la página seleccionada
if selection == "Inicio":
    page_inicio()
elif selection == "Exploración del Dataset":
    page_exploracion()
elif selection == "Calidad de Datos":
    page_calidad_datos()
elif selection == "Visualizaciones":
    page_visualizaciones()
elif selection == "Conclusiones":
    page_conclusiones()
