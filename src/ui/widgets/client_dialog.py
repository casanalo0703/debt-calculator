from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QDialogButtonBox,
)
from models.client import Client


class ClientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nuevo Cliente")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de entrada
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Agregar campos al formulario
        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        # Botones de aceptar y cancelar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def validate_data(self) -> bool:
        try:
            name = self.name_input.text().strip()
            phone = self.phone_input.text().strip()
            email = self.email_input.text().strip()
            Client(name=name, phone=f"+52{phone}", email=email)
            return True
        except ValueError as e:
            QMessageBox.critical(self, "Error de Validación", str(e))
            return False

    def accept(self) -> None:
        """Se llama cuando se presiona el botón Aceptar"""
        if self.validate_data():
            super().accept()

    def get_data(self) -> Client:
        """Devuelve los datos del cliente ingresados"""
        return Client(
            name=self.name_input.text().strip(),
            phone=f"+52{self.phone_input.text().strip()}",
            email=self.email_input.text().strip(),
        )
