# Intenta importar las librerías necesarias para el proyecto.
try:
    import sys # Importa la librería sys
    import pandas as pd  # Importa la librería pandas como pd
    import matplotlib # Importa la librería matplotlib
    import matplotlib.pyplot as plt # Importa la librería matplotlib.pyplot como plt

    matplotlib.use('QtAgg') # Selecciona el backend Qt5Agg para matplotlib

    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Importa la clase FigureCanvasQTAgg de la librería matplotlib.backends.backend_qt5agg
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar # Importa la clase NavigationToolbar2QT de la librería matplotlib.backends.backend_qt5agg
    from matplotlib.figure import Figure # Importa la clase Figure de la librería matplotlib.figure

    from dataclasses import dataclass

    # Importa las clases QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog y QLabel de la librería QtWidgets de PyQt6
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QVBoxLayout,
        QWidget,
        QFileDialog,
        QLabel,
        QToolBar,
        QComboBox,
        QLineEdit, 
        QComboBox, 
        QDialog,
        QHBoxLayout,
        QMessageBox
    )
    from PyQt6.QtGui import QIcon # Importa la clase QIcon de la librería QtGui de PyQt6 para manejar iconos. 

    # Imprime un mensaje si las bibliotecas se importan correctamente
    print("Bibliotecas importadas correctamente.")

except ImportError as e:
    # Imprime el error en caso de que no se pueda importar alguna librería
    print(f"Error al importar las bibliotecas: {e}") 

@dataclass
class Cambiar:
    canal: int
    desplazamiento: float
    amplitud: float

class CanalDialogo(QDialog):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Configuración de Canal")
        self.setMinimumSize(300, 200)
        
        # Layout de la ventana de diálogo
        layout = QVBoxLayout()

        # Menú desplegable para seleccionar canal
        self.label_canal = QLabel("Selecciona el Canal:")
        self.combo_canal = QComboBox()
        self.combo_canal.addItems(["1", "2", "3", "4"])
        
        # Campo de entrada para amplitud
        self.label_amplitud = QLabel("Amplitud:")
        self.input_amplitud = QLineEdit()
        self.input_amplitud.setPlaceholderText("Introduce la amplitud")

        # Campo de entrada para desplazamiento
        self.label_desplazamiento = QLabel("Desplazamiento:")
        self.input_desplazamiento = QLineEdit()
        self.input_desplazamiento.setPlaceholderText("Introduce el desplazamiento")
        
        # Agregar widgets al layout
        layout.addWidget(self.label_canal)
        layout.addWidget(self.combo_canal)
        layout.addWidget(self.label_amplitud)
        layout.addWidget(self.input_amplitud)
        layout.addWidget(self.label_desplazamiento)
        layout.addWidget(self.input_desplazamiento)

        button_layout = QHBoxLayout()

        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.clicked.connect(self.modifica_canal)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.reject)  # Cierra el diálogo sin hacer nada

        button_layout.addWidget(self.boton_aceptar)
        button_layout.addWidget(self.boton_cancelar)

        layout.addLayout(button_layout)

        # Establecer el layout en el diálogo
        self.setLayout(layout)
    
    def modifica_canal(self):
        try:
            # Validar y convertir amplitud
            amplitud_text = self.input_amplitud.text()
            if amplitud_text:  # Si el campo no está vacío
                try:
                    self.ventana_principal.modCanal.amplitud = float(amplitud_text)
                except ValueError:
                    # Si el valor no es un número válido, mostrar un mensaje de error
                    raise ValueError("Ingrese un número válido.")
            else:
                self.ventana_principal.modCanal.amplitud = 1.0  # Valor por defecto si está vacío

            # Validar y convertir desplazamiento
            desplazamiento_text = self.input_desplazamiento.text()
            if desplazamiento_text:  # Si el campo no está vacío
                try:
                    self.ventana_principal.modCanal.desplazamiento = float(desplazamiento_text)
                except ValueError:
                    # Si el valor no es un número válido, mostrar un mensaje de error
                    raise ValueError("Ingrese un número válido.")
            else:
                self.ventana_principal.modCanal.desplazamiento = 0.0  # Valor por defecto si está vacío
            
            # Convertir el canal seleccionado a entero (se asume que siempre habrá un canal válido)
            try:
                self.ventana_principal.modCanal.canal = int(self.combo_canal.currentText())
            except ValueError:
                raise ValueError("El canal debe ser un número válido.")

            # Llamar al método para actualizar el gráfico
            self.ventana_principal.graf()

        except ValueError as e:
            # Si ocurre un error de conversión, mostrar un mensaje de advertencia
            print(f"Error: {e}")
            QMessageBox.warning(self, "Error", str(e))



# Crea una clase Ventana que hereda de QMainWindow
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 500)  # Establece el tamaño mínimo de la ventana
        self.setWindowTitle("Mi gráfico")  # Cambia el título de la ventana
        self.setWindowIcon(QIcon("icono.jpg"))  # Cambia el icono de la ventana

        # Permitir que la ventana acepte archivos arrastrados
        self.setAcceptDrops(True)

        # Crea la barra de herramientas
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)  # Añade la barra de herramientas a la ventana

        # Crea los botones con iconos
        self.boton1 = QPushButton(QIcon("images/cargar archivo.png"), "Cargar archivo")
        self.boton2 = QPushButton(QIcon("images/salir.png"), "Salir")

        # Agrega barra para escalar eje x
        etiqueta_tiempo = QLabel("Tiempo:") # Crea una etiqueta para el desplegable de tiempo
        self.desplegableX = QComboBox() # Crea un desplegable para seleccionar la escala de tiempo
        self.desplegableX.addItems(["s", "ms", "us"]) # Añade las opciones al desplegable

        # Agrega barra para escalar eje y
        etiqueta_tension = QLabel("Tensión:") # Crea una etiqueta para el desplegable de tensión
        self.desplegableY = QComboBox() # Crea un desplegable para seleccionar la escala de tensión
        self.desplegableY.addItems(["V", "mV", "uV"]) # Añade las opciones al desplegable

        self.factor_tiempo = 1 # Factor de escala para el eje x
        self.factor_tension = 1 # Factor de escala para el eje y
        self.pos_label = "upper right" # Posición del Label por default
        self.modCanal = Cambiar(1, 0, 1)

        # Crea el botón para activar/desactivar los cursores
        self.boton_cursor_x = QPushButton("Activar cursor tiempo")
        self.boton_cursor_y = QPushButton("Activar cursor tension") 
        
        # Agrega barra para cambiar de lugar la leyenda
        self.etiqueta_label = QLabel("Label:")
        self.desplegableLabel = QComboBox()
        self.desplegableLabel.addItems(["Arriba derecha",
                                        "Arriba izquierda", "Abajo derecha",
                                        "Abajo izquierda", "Arriba centro",
                                        "Abajo centro", "Centro izquierda",
                                        "Centro derecha", "Centro"])

        # Etiqueta para mostrar la distancia entre los cursores
        self.etiqueta_distancia_tension = QLabel("Tension: -")
        self.etiqueta_distancia_tiempo = QLabel("Tiempo: -")

        # Modificar el canal
        self.boton_abrir_dialogo = QPushButton("Modificar canales")
        self.boton_abrir_dialogo.clicked.connect(self.abrir_dialogo)
        
        # Añade los botones a la barra de herramientas
        toolbar.addWidget(self.boton1)
        toolbar.addWidget(self.boton2)
        toolbar.addWidget(etiqueta_tiempo)
        toolbar.addWidget(self.desplegableX)
        toolbar.addWidget(etiqueta_tension)
        toolbar.addWidget(self.desplegableY)
        toolbar.addWidget(self.boton_cursor_x)
        toolbar.addWidget(self.boton_cursor_y)
        toolbar.addWidget(self.etiqueta_label)
        toolbar.addWidget(self.desplegableLabel)
        toolbar.addWidget(self.etiqueta_distancia_tension)
        toolbar.addWidget(self.etiqueta_distancia_tiempo)
        toolbar.addWidget(self.boton_abrir_dialogo)

        # Conecta los botones a sus funciones correspondientes
        self.boton1.clicked.connect(self.cargar_archivo) 
        self.boton2.clicked.connect(self.salir)
        self.boton_cursor_x.clicked.connect(self.activar_cursores_x)
        self.boton_cursor_y.clicked.connect(self.activar_cursores_y)

        # Conecta la barra desplegable con la funcion
        # Conectar los cambios en los desplegables a la función de actualización de escala
        self.desplegableX.currentIndexChanged.connect(self.actualizar_escala)
        self.desplegableY.currentIndexChanged.connect(self.actualizar_escala)
        
        # Conecta los cambios en el desplegable del label con la función
        self.desplegableLabel.currentIndexChanged.connect(self.actualizar_label)

        # Inicializa variables para los cursores y su estado
        self.cursor_activado_x = False
        self.cursor_activado_y = False
        self.cursor1_x = None
        self.cursor2_x = None
        self.cursor1_y = None
        self.cursor2_y = None

        # Crea la figura y el lienzo para el gráfico
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)  # Define el canvas primero

        # Crea la barra de herramientas de navegación para el gráfico
        self.toolbar = NavigationToolbar(self.canvas, self)  # Luego crea la toolbar

        # Disposición de los widgets en la ventana
        layout = QVBoxLayout() # Crea un layout vertical
        layout.addWidget(self.toolbar)  # Añade la barra de herramientas de navegación
        layout.addWidget(self.canvas)   # Añade el lienzo para el gráfico

        container = QWidget() # Crea un contenedor para los widgets
        container.setLayout(layout) # Establece el layout en el contenedor
        self.setCentralWidget(container) # Establece el contenedor como widget central
        
        # Conecta el evento de clic en el lienzo a la función onclick
        self.canvas.mpl_connect("button_press_event", self.onclick)


    def abrir_dialogo(self):
        # Crear una instancia del diálogo de configuración de canal y mostrarlo
        dialogo = CanalDialogo(self)
        dialogo.exec()
    
    # Método para activar/desactivar los cursores
    def activar_cursores_x(self):
        # Cambia el estado de activación de los cursores
        self.cursor_activado_x = not self.cursor_activado_x
        if self.cursor_activado_x:
            self.boton_cursor_x.setText("Desactivar Cursor Tiempo")
            self.canvas.mpl_connect("button_press_event", self.onclick)
        else:
            self.boton_cursor_x.setText("Activar Cursor Tiempo")
            self.limpiar_cursores_x()
                # Método para activar/desactivar los cursores

    # Método para limpiar los cursores
    def limpiar_cursores_x(self):
        # Limpia los cursores y la etiqueta de distancia
        self.cursor1_x = None
        self.cursor2_x = None
        self.etiqueta_distancia_tiempo.setText("Tiempo: -")
        self.graf()  # Redibuja sin los cursores

    # Método para activar/desactivar los cursores
    def activar_cursores_y(self):
        # Cambia el estado de activación de los cursores
        self.cursor_activado_y = not self.cursor_activado_y
        if self.cursor_activado_y:
            self.boton_cursor_y.setText("Desactivar cursor tension")
            self.canvas.mpl_connect("button_press_event", self.onclick)
        else:
            self.boton_cursor_y.setText("Activar cursor tension")
            self.limpiar_cursores_y()

    # Método para limpiar los cursores
    def limpiar_cursores_y(self):
        # Limpia los cursores y la etiqueta de distancia
        self.cursor1_y = None
        self.cursor2_y = None
        self.etiqueta_distancia_tension.setText("Tension: -")
        self.graf()  # Redibuja sin los cursores

    # Método para manejar el evento de clic en el lienzo
    def onclick(self, event):
        if event.inaxes != self.figure.axes[0]:
            return

        # Si los cursores están activados, maneja el evento de clic
        if self.cursor_activado_x:
            if self.cursor1_x is None:
                self.cursor1_x = event.xdata
            elif self.cursor2_x is None:
                self.cursor2_x = event.xdata
                distancia = abs(self.cursor2_x - self.cursor1_x) 
                self.etiqueta_distancia_tiempo.setText(f"Tiempo: {distancia:.8f} {self.desplegableX.currentText()}")
            self.graf()

        # Si los cursores están activados, maneja el evento de clic
        if self.cursor_activado_y:
            if self.cursor1_y is None:
                self.cursor1_y = event.ydata
            elif self.cursor2_y is None:
                self.cursor2_y = event.ydata
                distancia = abs(self.cursor2_y - self.cursor1_y)
                self.etiqueta_distancia_tension.setText(f"Tensión: {distancia:.8f} {self.desplegableY.currentText()}")
            self.graf()


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

    # Función para cargar el archivo arrastrado
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            archivo = event.mimeData().urls()[0].toLocalFile()
            if archivo.endswith('.csv'):
                try:
                    self.grafico = pd.read_csv(archivo, header=0)
                    print(self.grafico)
                    print(f"Archivo cargado: {archivo}")
                    self.graf()
                except Exception as e:
                    print(f"Error al cargar el archivo: {e}")
            else:
                print("El archivo debe ser un archivo CSV.")

    # Función para cargar un archivo
    def cargar_archivo(self):
        print("Cargue su archivo .csv")  # Imprime un mensaje en la consola
        # Abre un cuadro de diálogo para seleccionar el archivo
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar archivo .csv", "", "CSV Files (*.csv);;All Files (*)")
        if archivo and archivo.endswith('.csv'):  # Si se selecciona un archivo y es csv
            try:
                self.grafico = pd.read_csv(archivo, header=0)  # Usamos header=0 para que la primera fila sea el encabezado
                print(self.grafico)  # Muestra el DataFrame en la consola
                self.graf()
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")  # Manejo de errores
    
    def actualizar_escala(self):
        # Definir los factores de escala según las unidades seleccionadas
        escala_tiempo = {'s': 1, 'ms': 1e3, 'us': 1e6} # Escalas de tiempo
        escala_tension = {'V': 1, 'mV': 1e3, 'uV': 1e6} # Escalas de tensión

        # Obtener las unidades seleccionadas
        unidad_tiempo = self.desplegableX.currentText() 
        unidad_tension = self.desplegableY.currentText()

        # Definir los factores de escala en función de las unidades seleccionadas
        self.factor_tiempo = escala_tiempo[unidad_tiempo]
        self.factor_tension = escala_tension[unidad_tension]

        # Actualizar el gráfico con las nuevas escalas
        self.graf()

    def actualizar_label(self):
        posLabel = {"Arriba derecha": "upper right",
            "Arriba izquierda": "upper left",
            "Abajo derecha": "lower right",
            "Abajo izquierda": "lower left",
            "Arriba centro": "upper center",
            "Abajo centro": "lower center",
            "Centro izquierda": "center left",
            "Centro derecha": "center right",
            "Centro": "center"}
        
        posDeseada = self.desplegableLabel.currentText()
        self.pos_label = posLabel[posDeseada]
        
        self.graf()

    # Función para generar un gráfico
    def graf(self):
        print("Generando gráfico...")  # Imprime un mensaje en la consola
        if hasattr(self, "grafico"):
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


    # Función para salir
    def salir(self):
        print("Saliendo...")  # Imprime un mensaje en la consola
        self.close()  # Cierra la ventana
    

# Crea una aplicación y una ventana principal
app = QApplication([])  
window = VentanaPrincipal()

# Muestra la ventana 
window.show()
app.exec()
