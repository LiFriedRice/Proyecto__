import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis App")

        # Crear widgets
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Seleccione un archivo CSV:").pack(pady=5)
        self.file_button = tk.Button(self.root, text="Seleccionar Archivo", command=self.select_file)
        self.file_button.pack(pady=5)
        
        self.file_path_label = tk.Label(self.root, text="Ningún archivo seleccionado")
        self.file_path_label.pack(pady=5)
        
        tk.Label(self.root, text="Fila de inicio (0-indexado):").pack(pady=5)
        self.start_row_entry = tk.Entry(self.root)
        self.start_row_entry.pack(pady=5)
        
        tk.Label(self.root, text="Fila de fin (0-indexado):").pack(pady=5)
        self.end_row_entry = tk.Entry(self.root)
        self.end_row_entry.pack(pady=5)
        
        self.process_button = tk.Button(self.root, text="Procesar Datos", command=self.process_data)
        self.process_button.pack(pady=20)
        
        # Crear contenedor para los gráficos
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Inicializar variables
        self.file_path = None
        self.figures = []
        self.current_figure_index = -1
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_path_label.config(text=self.file_path)
        else:
            self.file_path_label.config(text="Ningún archivo seleccionado")

    def process_data(self):
        if not self.file_path:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
            return
        
        try:
            df = pd.read_csv(self.file_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo CSV: {e}")
            return
        
        try:
            start_row_str = self.start_row_entry.get().strip()
            end_row_str = self.end_row_entry.get().strip()

            if start_row_str and end_row_str:
                start_row = int(start_row_str)
                end_row = int(end_row_str)
                if start_row < 0 or end_row < start_row:
                    raise ValueError("Las filas de inicio y fin no son válidas.")
            else:
                start_row = 0
                end_row = len(df) - 1

        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida para las filas: {ve}")
            return

        self.generate_plots(df, start_row, end_row)
        self.show_next_plot()

    def generate_plots(self, df, start_row, end_row):
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
        self.figures.append(fig1)

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
        self.figures.append(fig2)

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
        self.figures.append(fig3)

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
        self.figures.append(fig4)

    def show_next_plot(self):
        if self.figures:
            if self.current_figure_index >= 0:
                self.figures[self.current_figure_index].canvas.get_tk_widget().pack_forget()
            self.current_figure_index = (self.current_figure_index + 1) % len(self.figures)
            fig = self.figures[self.current_figure_index]
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            # Programar la actualización del gráfico después de 3 segundos
            self.root.after(3000, self.show_next_plot)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()