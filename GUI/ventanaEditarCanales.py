from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
from dataclasses import dataclass
from backPrincipal import graf
@dataclass
class Cambiar:
    canal: int
    desplazamiento: float
    amplitud: float

class VentanaEditarCanal(QDialog):
    def __init__(self, ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Configuración de Canal")
        
        layout = QVBoxLayout()
        self.label_canal, self.combo_canal = QLabel("Selecciona el Canal:"), QComboBox()
        self.combo_canal.addItems(["1", "2", "3", "4"])

        self.label_amplitud, self.input_amplitud = QLabel("Amplitud:"), QLineEdit()
        self.label_desplazamiento, self.input_desplazamiento = QLabel("Desplazamiento:"), QLineEdit()
        
        layout.addWidget(self.label_canal)
        layout.addWidget(self.combo_canal)
        layout.addWidget(self.label_amplitud)
        layout.addWidget(self.input_amplitud)
        layout.addWidget(self.label_desplazamiento)
        layout.addWidget(self.input_desplazamiento)

        button_layout = QHBoxLayout()
        boton_aceptar = QPushButton("Aceptar")
        boton_aceptar.clicked.connect(self.modifica_canal)
        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.clicked.connect(self.reject)

        button_layout.addWidget(boton_aceptar)
        button_layout.addWidget(boton_cancelar)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def modifica_canal(self):
        try:
            self.ventana_principal.modCanal.amplitud = float(self.input_amplitud.text() or 1.0)
            self.ventana_principal.modCanal.desplazamiento = float(self.input_desplazamiento.text() or 0.0)
            self.ventana_principal.modCanal.canal = int(self.combo_canal.currentText())

            if self.ventana_principal.modCanal.amplitud != 1.0 or self.ventana_principal.modCanal.desplazamiento != 0.0:
                graf(self.ventana_principal)
                self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", "Ingrese un número válido.")
