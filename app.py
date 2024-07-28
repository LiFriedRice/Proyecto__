import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def generate_plots(df, start_row, end_row):
    # Filtrar el DataFrame por el rango de filas
    df_filtered = df.iloc[start_row:end_row + 1]

    # Años y géneros únicos
    x_years = df_filtered['Year_of_Release'].unique()
    x_Genre = df_filtered['Genre'].unique()

    # Ordenar años y géneros
    x_years = np.sort(x_years)
    x_Genre = np.sort(x_Genre)

    # Convertir años y géneros en índices numéricos
    x_years_indices = np.arange(len(x_years))
    x_Genre_indices = np.arange(len(x_Genre))

    # Para el gráfico de barras por año
    fig1, ax1 = plt.subplots(figsize=(14,7))
    bar_width = 0.2
    df_sorted_years = df_filtered.groupby('Year_of_Release').sum().reindex(x_years).fillna(0)
    ax1.bar(x_years_indices - 1.5 * bar_width, df_sorted_years['NA_Sales'], width=bar_width, label='NA Sales')
    ax1.bar(x_years_indices - 0.5 * bar_width, df_sorted_years['EU_Sales'], width=bar_width, label='EU Sales')
    ax1.bar(x_years_indices + 0.5 * bar_width, df_sorted_years['JP_Sales'], width=bar_width, label='JP Sales')
    ax1.bar(x_years_indices + 1.5 * bar_width, df_sorted_years['Other_Sales'], width=bar_width, label='Other Sales')
    ax1.set_title('Ventas por Año (Gráfico de Barras)')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Ventas')
    ax1.set_xticks(x_years_indices)
    ax1.set_xticklabels(x_years)
    ax1.legend()
    
    # Para el gráfico de líneas por año
    fig2, ax2 = plt.subplots(figsize=(14,7))
    ax2.plot(x_years_indices, df_sorted_years['NA_Sales'], label='NA Sales', marker='o')
    ax2.plot(x_years_indices, df_sorted_years['EU_Sales'], label='EU Sales', marker='o')
    ax2.plot(x_years_indices, df_sorted_years['JP_Sales'], label='JP Sales', marker='o')
    ax2.plot(x_years_indices, df_sorted_years['Other_Sales'], label='Other Sales', marker='o')
    ax2.set_title('Ventas por Año (Gráfico de Líneas)')
    ax2.set_xlabel('Año')
    ax2.set_ylabel('Ventas')
    ax2.set_xticks(x_years_indices)
    ax2.set_xticklabels(x_years)
    ax2.legend()

    # Para el gráfico de barras por género
    fig3, ax3 = plt.subplots(figsize=(14,7))
    df_sorted_genre = df_filtered.groupby('Genre').sum().reindex(x_Genre).fillna(0)
    ax3.bar(x_Genre_indices - 1.5 * bar_width, df_sorted_genre['NA_Sales'], width=bar_width, label='NA Sales')
    ax3.bar(x_Genre_indices - 0.5 * bar_width, df_sorted_genre['EU_Sales'], width=bar_width, label='EU Sales')
    ax3.bar(x_Genre_indices + 0.5 * bar_width, df_sorted_genre['JP_Sales'], width=bar_width, label='JP Sales')
    ax3.bar(x_Genre_indices + 1.5 * bar_width, df_sorted_genre['Other_Sales'], width=bar_width, label='Other Sales')
    ax3.set_title('Ventas por Género (Gráfico de Barras)')
    ax3.set_xlabel('Género')
    ax3.set_ylabel('Ventas')
    ax3.set_xticks(x_Genre_indices)
    ax3.set_xticklabels(x_Genre, rotation=90)
    ax3.legend()

    # Para el gráfico de líneas por género
    fig4, ax4 = plt.subplots(figsize=(14,7))
    ax4.plot(x_Genre_indices, df_sorted_genre['NA_Sales'], label='NA Sales', marker='o')
    ax4.plot(x_Genre_indices, df_sorted_genre['EU_Sales'], label='EU Sales', marker='o')
    ax4.plot(x_Genre_indices, df_sorted_genre['JP_Sales'], label='JP Sales', marker='o')
    ax4.plot(x_Genre_indices, df_sorted_genre['Other_Sales'], label='Other Sales', marker='o')
    ax4.set_title('Ventas por Género (Gráfico de Líneas)')
    ax4.set_xlabel('Género')
    ax4.set_ylabel('Ventas')
    ax4.set_xticks(x_Genre_indices)
    ax4.set_xticklabels(x_Genre, rotation=90)
    ax4.legend()

    return fig1, fig2, fig3, fig4

# Aplicación Streamlit
st.title("Aplicación de Análisis de Datos")

uploaded_file = st.file_uploader("Seleccione un archivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Archivo cargado exitosamente.")
    
    start_row = st.number_input("Fila de inicio (0-indexado):", min_value=0, value=0)
    end_row = st.number_input("Fila de fin (0-indexado):", min_value=0, value=len(df)-1)
    
    if st.button("Procesar Datos"):
        if start_row < 0 or end_row < start_row:
            st.error("Las filas de inicio y fin no son válidas.")
        else:
            figs = generate_plots(df, start_row, end_row)
            
            st.pyplot(figs[0])
            st.pyplot(figs[1])
            st.pyplot(figs[2])
            st.pyplot(figs[3])
else:
    st.info("Por favor, cargue un archivo CSV.")
