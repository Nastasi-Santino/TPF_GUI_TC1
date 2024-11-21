# GUI TP Final TCI - Graficador para Osciloscopio
Este proyecto implementa una interfaz gráfica de usuario (GUI) diseñada para visualizar datos obtenidos de un osciloscopio. Permite cargar archivos CSV, manipular canales, agregar cursores y ajustar parámetros de escala y etiquetas de gráficos.

## Características principales
* Visualización de datos: Grafica señales contenidas en archivos CSV.
* Personalización: Ajuste de escala temporal y de tensión, desplazamiento y amplitud de canales.
* Cursores: Activación de cursores para medición de tiempos y tensiones.
* Interfaz amigable: Ventanas y menús intuitivos construidos con PyQt6 y Matplotlib.


## Requisitos:
Para ejecutar este programa, asegúrese de tener instalados los siguientes paquetes:
* PyQt6
* Matplotlib
* Pandas

## Uso
1. Ejecute el programa principal main.py.
2. En la ventana principal:
    * Cargue un archivo CSV desde el menú "Archivo" o arrastrándolo al área principal.
    * Active los cursores desde el menú "Cursores" para realizar mediciones.
    * Ajuste escalas de tiempo y tensión o posición de las etiquetas desde la barra de herramientas.
    * Modifique las propiedades de los canales seleccionando "Modificar canales".
3. Los gráficos se actualizan automáticamente con cada cambio realizado.

## Organización del código
El proyecto está dividido en varios módulos:
* main.py: Contiene la ventana principal y la configuración de la GUI.
* backPrincipal.py: Gestiona la lógica del gráfico principal, incluida la carga de archivos CSV y la actualización de datos.
* backCursores.py: Controla la lógica de los cursores de tiempo y tensión.
* ventanaEditarCanales.py: Implementa una ventana modal para configurar propiedades de los canales.