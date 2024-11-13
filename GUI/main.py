try:
    import sys
    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('QtAgg') 
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    from dataclasses import dataclass
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QVBoxLayout,
        QWidget, QLabel, QToolBar,
        QComboBox,
    )
    from PyQt6.QtGui import QIcon, QAction

    from ventanaEditarCanales import VentanaEditarCanal, Cambiar
    from backPrincipal import cargar_archivo, graf
    from backCursores import activar_cursores_x, activar_cursores_y, onClick

    print("Bibliotecas importadas correctamente.")

except ImportError as e:
    print(f"Error al importar las bibliotecas: {e}")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.setWindowTitle("GUI TP Final TCI - Graficador para Osciloscopio")
        self.setWindowIcon(QIcon("icono.jpg"))

        self.factor_tiempo = 1
        self.factor_tension = 1
        self.pos_label = "upper right"
        self.modCanal = Cambiar(1, 0, 1)

        # Inicializa variables para los cursores y su estado
        self.cursor_activado_x = False
        self.cursor_activado_y = False
        self.cursor1_x = None
        self.cursor2_x = None
        self.cursor1_y = None
        self.cursor2_y = None

        menu_bar = self.menuBar()
        menu_archivo = menu_bar.addMenu("Archivo")
        accion_cargar = QAction("Cargar archivo", self)
        accion_salir = QAction("Salir", self)
        menu_archivo.addAction(accion_cargar)
        menu_archivo.addAction(accion_salir)

        accion_cargar.triggered.connect(lambda: cargar_archivo(self))
        accion_salir.triggered.connect(self.close)

        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)
        
        etiqueta_tiempo = QLabel("Tiempo:")
        self.desplegableX = QComboBox()
        self.desplegableX.addItems(["s", "ms", "us"])

        etiqueta_tension = QLabel("Tensión:")
        self.desplegableY = QComboBox()
        self.desplegableY.addItems(["V", "mV", "uV"])

        self.etiqueta_label = QLabel("Label:")
        self.desplegableLabel = QComboBox()
        self.desplegableLabel.addItems(["Arriba derecha", "Arriba izquierda", "Abajo derecha", "Abajo izquierda", "Arriba centro", "Abajo centro", "Centro izquierda", "Centro derecha", "Centro"])

        self.botonEditarCanales = QPushButton("Modificar canales")
        self.botonEditarCanales.clicked.connect(self.abrirVentanaEditarCanal)
        
        self.etiqueta_distancia_tension = QLabel("Tension: -")
        self.etiqueta_distancia_tiempo = QLabel("Tiempo: -")


        # Menú de opciones para activar/desactivar cursores
        menu_cursores = menu_bar.addMenu("Cursores")
        self.accion_activar_cursor_x = QAction("Activar cursor tiempo", self)
        self.accion_activar_cursor_y = QAction("Activar cursor tensión", self)
        menu_cursores.addAction(self.accion_activar_cursor_x)
        menu_cursores.addAction(self.accion_activar_cursor_y)

        # Conecta las acciones del menú a las funciones correspondientes
        self.accion_activar_cursor_x.triggered.connect(lambda: activar_cursores_x(self))
        self.accion_activar_cursor_y.triggered.connect(lambda: activar_cursores_y(self))

        toolbar.addWidget(etiqueta_tiempo)
        toolbar.addWidget(self.desplegableX)
        toolbar.addWidget(etiqueta_tension)
        toolbar.addWidget(self.desplegableY)
        toolbar.addWidget(self.etiqueta_label)
        toolbar.addWidget(self.desplegableLabel)
        toolbar.addWidget(self.botonEditarCanales)
        toolbar.addSeparator()
        toolbar.addWidget(self.etiqueta_distancia_tension)
        toolbar.addSeparator()
        toolbar.addWidget(self.etiqueta_distancia_tiempo)

        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.desplegableX.currentIndexChanged.connect(self.actualizar_escala)
        self.desplegableY.currentIndexChanged.connect(self.actualizar_escala)
        self.desplegableLabel.currentIndexChanged.connect(self.actualizar_label)

        self.canvas.mpl_connect("button_press_event", lambda event: onClick(self, event))

    # Método para abrir la ventana de edición de canales
    def abrirVentanaEditarCanal(self):
        dialogo = VentanaEditarCanal(self)
        dialogo.exec()
    
    # Método para actualizar la escala del gráfico
    def actualizar_escala(self):
        self.factor_tiempo, self.factor_tension = {'s': 1, 'ms': 1e3, 'us': 1e6}[self.desplegableX.currentText()], {'V': 1, 'mV': 1e3, 'uV': 1e6}[self.desplegableY.currentText()]
        graf(self)
    
    # Método para actualizar la posición de la etiqueta
    def actualizar_label(self):
        posLabel = {"Arriba derecha": "upper right", "Arriba izquierda": "upper left", "Abajo derecha": "lower right", "Abajo izquierda": "lower left", "Arriba centro": "upper center", "Abajo centro": "lower center", "Centro izquierda": "center left", "Centro derecha": "center right", "Centro": "center"}
        self.pos_label = posLabel[self.desplegableLabel.currentText()]
        graf(self)

    # Función para aceptar archivos arrastrados
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith('.csv'):
                event.acceptProposedAction() # Acepta el arrastre
            else:
                event.ignore()
        else:
            event.ignore()

# Crea una aplicación y una ventana principal
app = QApplication([])  
window = VentanaPrincipal()

# Muestra la ventana 
window.show()
app.exec()
