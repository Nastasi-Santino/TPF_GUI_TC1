# Intenta importar las librerías necesarias para el proyecto.
try:
    import sys # Importa la librería sys
    import pandas as pd  # Importa la librería pandas como pd
    import matplotlib.pyplot as plt # Importa la librería matplotlib.pyplot como plt
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

        # Crea la barra de herramientas
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)  # Añade la barra de herramientas a la ventana

        # Crea los botones con iconos
        self.boton1 = QPushButton(QIcon("images/cargar archivo.png"), "Cargar archivo")
        self.boton2 = QPushButton(QIcon("images/graf.png"), "Generar gráfico")
        self.boton3 = QPushButton(QIcon("images/guardar archivo.png"), "Guardar gráfico")
        self.boton4 = QPushButton(QIcon("images/borrar.png"), "Limpiar gráfico")
        self.boton5 = QPushButton(QIcon("images/atras.png"), "Atrás")
        self.boton6 = QPushButton(QIcon("images/adelante.png"), "Adelante")
        self.boton7 = QPushButton(QIcon("images/salir.png"), "Salir")

        # Añade los botones a la barra de herramientas
        toolbar.addWidget(self.boton1)
        toolbar.addWidget(self.boton2)
        toolbar.addWidget(self.boton3)
        toolbar.addWidget(self.boton4)
        toolbar.addWidget(self.boton5)
        toolbar.addWidget(self.boton6)
        toolbar.addWidget(self.boton7)

        # Conecta los botones a sus funciones correspondientes
        self.boton1.clicked.connect(self.cargar_archivo) 
        self.boton2.clicked.connect(self.graf)
        self.boton3.clicked.connect(self.guardar_archivo)
        self.boton4.clicked.connect(self.borrar)
        self.boton5.clicked.connect(self.atras)
        self.boton6.clicked.connect(self.adelante)
        self.boton7.clicked.connect(self.salir) 
    
    # Función para cargar un archivo
    def cargar_archivo(self):
        print("Cargue su archivo .csv")  # Imprime un mensaje en la consola
        # Abre un cuadro de diálogo para seleccionar el archivo
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar archivo .csv", "", "CSV Files (*.csv);;All Files (*)")
        if archivo:  # Si se selecciona un archivo
            try:
                self.grafico = pd.read_csv(archivo, header=0)  # Usamos header=0 para que la primera fila sea el encabezado
                print(self.grafico)  # Muestra el DataFrame en la consola
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")  # Manejo de errores
    
    # Función para generar un gráfico
    def graf(self):
        print("Generando gráfico...")  # Imprime un mensaje en la consola
       # if hasattr(self, "grafico"):
            #ACA grafico 
        #else:
          #  print("No se ha cargado ningún archivo CSV.")  # Mensaje si no hay datos


    # Función para salir
    def salir(self):
        print("Saliendo...")  # Imprime un mensaje en la consola
        self.close()  # Cierra la ventana

    #DE ACA PARA ABAJO NO ESTA IMPLEMENTADO
    #CHEQUEAR SI ES NECESARIO DADO QUE MATPLOT TIENE ESTAS FUNCIONES
    # Función para guardar un archivo
    def guardar_archivo(self):
        print("Guardando archivo...")  # Imprime un mensaje en la consola
    
    # Función para limpiar un gráfico
    def borrar(self):
        print("Limpiando gráfico...")  # Imprime un mensaje en la consola
    
    # Función para retroceder
    def atras(self):
        print("Retrocediendo...")  # Imprime un mensaje en la consola

    # Función para avanzar
    def adelante(self):
        print("Avanzando...")  # Imprime un mensaje en la consola



    

# Crea una aplicación y una ventana principal
app = QApplication([])  
window = Ventana()

# Muestra la ventana 
window.show()
app.exec()
