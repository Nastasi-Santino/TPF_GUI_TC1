# Intenta importar las librerías necesarias para el proyecto.
try:
    import sys # Importa la librería sys
    import pandas as pd  # Importa la librería pandas como pd
    import matplotlib
    import matplotlib.pyplot as plt # Importa la librería matplotlib.pyplot como plt

    matplotlib.use('QtAgg')

    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure

    # Importa las clases QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog y QLabel de la librería QtWidgets de PyQt6
    from PyQt6.QtWidgets import (
        QApplication,  # Maneja la aplicación y su ciclo de eventos.
        QMainWindow,  # Proporciona una ventana principal para la aplicación.
        QPushButton,  # Crea un botón que puede ser presionado.
        QVBoxLayout,  # Administra el diseño vertical de widgets.
        QWidget,  # Base para todos los widgets de interfaz de usuario.
        QFileDialog,  # Proporciona un diálogo para abrir y guardar archivos.
        QLabel,  # Muestra texto o imágenes.
        QToolBar,  # Proporciona una barra de herramientas para acciones rápidas.
        QComboBox,  # Proporciona un cuadro combinado que permite seleccionar un elemento de una lista desplegable.
    )
    from PyQt6.QtGui import QIcon # Importa la clase QIcon de la librería QtGui de PyQt6 para manejar iconos. 

    # Imprime un mensaje si las bibliotecas se importan correctamente
    print("Bibliotecas importadas correctamente.")

except ImportError as e:
    # Imprime el error en caso de que no se pueda importar alguna librería
    print(f"Error al importar las bibliotecas: {e}") 

# Crea una clase Ventana que hereda de QMainWindow
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)  # Establece el tamaño mínimo de la ventana
        self.setWindowTitle("Mi gráfico")  # Cambia el título de la ventana
        self.setWindowIcon(QIcon("icono.jpg"))  # Cambia el icono de la ventana

        # Permitir que la ventana acepte archivos arrastrados
        self.setAcceptDrops(True)

        # Crea la barra de herramientas
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)  # Añade la barra de herramientas a la ventana

        # Crea los botones con iconos
        self.boton1 = QPushButton(QIcon("images/cargar archivo.png"), "Cargar archivo (Puede arrastrarlo hacia la GUI)")
        self.boton7 = QPushButton(QIcon("images/salir.png"), "Salir")

        # Añade los botones a la barra de herramientas
        toolbar.addWidget(self.boton1)
        toolbar.addWidget(self.boton7)

        # Conecta los botones a sus funciones correspondientes
        self.boton1.clicked.connect(self.cargar_archivo) 
        self.boton7.clicked.connect(self.salir)
        
        # Crea la figura y el lienzo para el gráfico
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)  # Define el canvas primero

        # Crea la barra de herramientas de navegación para el gráfico
        self.toolbar = NavigationToolbar(self.canvas, self)  # Luego crea la toolbar

        # Disposición de los widgets en la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)  # Añade la barra de herramientas de navegación
        layout.addWidget(self.canvas)   # Añade el lienzo para el gráfico

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    
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
    
    # Función para generar un gráfico
    def graf(self):
        print("Generando gráfico...")  # Imprime un mensaje en la consola
        if hasattr(self, "grafico"):
            eje_x = pd.to_numeric(self.grafico.iloc[:, 0], errors='coerce')  # Selecciona la primera columna como eje x
            
            canales = []  # Lista para almacenar los canales

            # Selecciona las columnas de los canales
            for i in range(1, 5):
                if i<self.grafico.shape[1]: # Si hay más columnas
                    canal = pd.to_numeric(self.grafico.iloc[:, i], errors='coerce')  # Selecciona la columna i
                    canales.append(canal)  # Añade el canal a la lista
                

            # Eliminar valores NaN de eje_x y canales
            eje_x = eje_x.dropna() * 1e6
            canales = [canal.dropna() for canal in canales] 

            # Asegurarse de que todos los canales tengan la misma longitud
            min_length = min(len(eje_x), *[len(canal) for canal in canales])
            eje_x = eje_x[:min_length]
            canales = [canal[:min_length] for canal in canales]

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            for index, canal in enumerate(canales):
                ax.plot(eje_x, canal, label=f'Canal {index + 1}', linestyle='-', linewidth=2, alpha=0.8)

            ax.set_title('', fontsize=16)
            ax.set_xlabel('Tiempo (us)', fontsize=14)
            ax.set_ylabel('Tensión (V)', fontsize=14)
            ax.legend(fontsize=12, loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.7)

            self.canvas.draw()
        else:
            print("No se ha cargado ningún archivo CSV.")  # Mensaje si no hay datos


    # Función para salir
    def salir(self):
        print("Saliendo...")  # Imprime un mensaje en la consola
        self.close()  # Cierra la ventana
    

# Crea una aplicación y una ventana principal
app = QApplication([])  
window = Ventana()

# Muestra la ventana 
window.show()
app.exec()
