import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from PyQt6.QtWidgets import QLabel

from backPrincipal import graf

# Método para activar/desactivar los cursores de tiempo
def activar_cursores_x(self):
    self.cursor_activado_x = not self.cursor_activado_x
    if self.cursor_activado_x:
        self.accion_activar_cursor_x.setText("Desactivar cursor tiempo")
    else:
        self.accion_activar_cursor_x.setText("Activar cursor tiempo")
        limpiar_cursores_x(self)

# Método para limpiar los cursores de tiempo
def limpiar_cursores_x(self):
    self.cursor1_x = None
    self.cursor2_x = None
    self.etiqueta_distancia_tiempo.setText("Tiempo: -")
    graf(self)  # Redibuja sin los cursores

# Método para activar/desactivar los cursores de tensión
def activar_cursores_y(self):
    self.cursor_activado_y = not self.cursor_activado_y
    if self.cursor_activado_y:
        self.accion_activar_cursor_y.setText("Desactivar cursor tensión")
    else:
        self.accion_activar_cursor_y.setText("Activar cursor tensión")
        limpiar_cursores_y(self)

# Método para limpiar los cursores de tensión
def limpiar_cursores_y(self):
    self.cursor1_y = None
    self.cursor2_y = None
    self.etiqueta_distancia_tension.setText("Tensión: -")
    graf(self)

# Método para manejar el evento de clic en el lienzo
def onClick(self, event):
    if event.inaxes != self.figure.axes[0]:
        return

    # Si los cursores de tiempo están activados, maneja el evento de clic
    if self.cursor_activado_x:
        if self.cursor1_x is None:
            self.cursor1_x = event.xdata
        elif self.cursor2_x is None:
            self.cursor2_x = event.xdata
            distancia = abs(self.cursor2_x - self.cursor1_x)
            self.etiqueta_distancia_tiempo.setText(f"Tiempo: {distancia:.4f} {self.desplegableX.currentText()}")
        graf(self)

    # Si los cursores de tensión están activados, maneja el evento de clic
    if self.cursor_activado_y:
        if self.cursor1_y is None:
            self.cursor1_y = event.ydata
        elif self.cursor2_y is None:
            self.cursor2_y = event.ydata
            distancia = abs(self.cursor2_y - self.cursor1_y)
            self.etiqueta_distancia_tension.setText(f"Tensión: {distancia:.4f} {self.desplegableY.currentText()}")
        graf(self)