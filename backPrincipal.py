import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt6.QtWidgets import  QFileDialog

def cargar_archivo(ventana):
    archivo, _ = QFileDialog.getOpenFileName(ventana, "Cargar archivo .csv", "", "CSV Files (*.csv);;All Files (*)")
    if archivo.endswith('.csv'):
        ventana.grafico = pd.read_csv(archivo, header=0)
        graf(ventana)

# Función para generar un gráfico
def graf(self):
    print("Generando gráfico...")  # Imprime un mensaje en la consola
    if hasattr(self, "grafico"):

        self.background_label.hide()

        titulo_actual = self.figure.axes[0].get_title() if self.figure.axes else "Gráfico"

        # Selecciona el eje x y aplica el factor de escala
        eje_x = pd.to_numeric(self.grafico.iloc[:, 0], errors='coerce') * self.factor_tiempo

        canales = []  # Lista para almacenar los canales
        # Selecciona las columnas de los canales y aplica el factor de escala
        for i in range(1, 5):
            if i == self.modCanal.canal:
                if i < self.grafico.shape[1]:  # Si hay más columnas
                    canal = pd.to_numeric(self.grafico.iloc[:, i], errors='coerce') * self.modCanal.amplitud  * self.factor_tension + self.modCanal.desplazamiento
                    canales.append(canal)

            elif i < self.grafico.shape[1] :  # Si hay más columnas
                canal = pd.to_numeric(self.grafico.iloc[:, i], errors='coerce') * self.factor_tension
                canales.append(canal)

        # Elimina valores NaN
        eje_x = eje_x.dropna()
        canales = [canal.dropna() for canal in canales]
        
        # Asegura que todos los canales tengan la misma longitud
        min_length = min(len(eje_x), *[len(canal) for canal in canales])
        eje_x = eje_x[:min_length]
        canales = [canal[:min_length] for canal in canales]

        # Limpia y vuelve a dibujar el gráfico
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for index, canal in enumerate(canales):
            ax.plot(eje_x, canal, label=f'Canal {index + 1}', linestyle='-', linewidth=2, alpha=0.8)

        # Etiquetas del gráfico
        ax.set_title(f"{titulo_actual}", fontsize=14)
        ax.set_xlabel(f"Tiempo ({self.desplegableX.currentText()})", fontsize=14)
        ax.set_ylabel(f"Tensión ({self.desplegableY.currentText()})", fontsize=14)
        ax.legend(fontsize=12, loc=self.pos_label)
        ax.grid(True, linestyle='--', alpha=0.7)

        if self.cursor1_x is not None:
            ax.axvline(x=self.cursor1_x, color='red', linestyle='--', label="Cursor")
        if self.cursor2_x is not None:
            ax.axvline(x=self.cursor2_x, color='red', linestyle='--', label="Cursor")
        if self.cursor1_y is not None:
            ax.axhline(y=self.cursor1_y, color='blue', linestyle='--', label="Cursor")
        if self.cursor2_y is not None:
            ax.axhline(y=self.cursor2_y, color='blue', linestyle='--', label="Cursor")               

        # Dibuja el gráfico actualizado
        self.figure.tight_layout()
        self.canvas.draw()
    else:
        print("No se ha cargado ningún archivo CSV.")  # Mensaje si no hay datos