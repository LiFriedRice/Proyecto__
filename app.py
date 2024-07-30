import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Configuración de Streamlit
st.title('Análisis de Datos de Videojuegos')

# Cargar el archivo CSV usando el cargador de archivos de Streamlit
archivo_csv = st.file_uploader("Sube tu archivo CSV", type="csv")

if archivo_csv:
    try:
        # Cargar los datos
        data = pd.read_csv(archivo_csv)

        # Mostrar las primeras filas del dataset
        st.write(data.head())

        # Función para graficar y mostrar gráficos en Streamlit
        def plot_and_show(data, x, y, title, xlabel, ylabel, plot_type='line', color='blue'):
            plt.figure(figsize=(10, 6))
            if plot_type == 'line':
                sns.lineplot(x=x, y=y, data=data, color=color)
            elif plot_type == 'bar':
                sns.barplot(x=x, y=y, data=data, color=color)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True)
            st.pyplot(plt.gcf())
            plt.close()

        # Visualización de datos generales
        plot_and_show(data, 'Genre', 'Global_Sales', 'Ventas Globales por Género', 'Género', 'Ventas Globales', 'bar', 'teal')
        plot_and_show(data, 'Publisher', 'Global_Sales', 'Ventas Globales por Publicadora', 'Publicadora', 'Ventas Globales', 'bar', 'coral')
        plot_and_show(data, 'Critic_Score', 'Global_Sales', 'Ventas Globales vs Puntuación de Críticos', 'Puntuación de Críticos', 'Ventas Globales', 'line', 'green')
        plot_and_show(data, 'User_Score', 'Global_Sales', 'Ventas Globales vs Puntuación de Usuarios', 'Puntuación de Usuarios', 'Ventas Globales', 'line', 'orange')

        # Seleccionar una publicadora para el análisis de regresión lineal
        publicadoras = data['Publisher'].unique()
        publicadora_seleccionada = st.selectbox("Selecciona una publicadora", publicadoras)

        # Filtrar datos para la publicadora seleccionada
        data_publicadora = data[data['Publisher'] == publicadora_seleccionada]

        if not data_publicadora.empty:
            # Realizar la regresión lineal
            X = data_publicadora[['Critic_Score', 'User_Score']].fillna(0).values
            y = data_publicadora['Global_Sales'].values

            # Ajustar modelo de regresión lineal
            model = LinearRegression()
            model.fit(X, y)
            predictions = model.predict(X)
            r2 = r2_score(y, predictions)

            # Graficar la regresión lineal
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='Critic_Score', y='Global_Sales', data=data_publicadora, color='blue', label='Datos Reales')
            sns.lineplot(x=data_publicadora['Critic_Score'], y=predictions, color='red', label='Predicción')
            plt.title(f'Regresión Lineal: Ventas Globales en {publicadora_seleccionada}')
            plt.xlabel('Puntuación de Críticos')
            plt.ylabel('Ventas Globales')
            plt.grid(True)
            st.pyplot(plt.gcf())
            plt.close()

            # Mostrar el valor de R²
            st.write(f'Precisión de la regresión lineal (R²) para {publicadora_seleccionada}: {r2:.2f}')
        else:
            st.warning("No hay suficientes datos para realizar la regresión lineal.")

    except pd.errors.EmptyDataError:
        st.error("El archivo está vacío. Por favor, verifique el contenido del archivo.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
