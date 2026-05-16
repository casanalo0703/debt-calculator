from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QDialogButtonBox,
)
from models.provider import Provider


class ProviderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nuevo Proveedor")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de entrada
        self.name_input = QLineEdit()
        self.contact_info_input = QLineEdit()
        self.type_of_service_input = QLineEdit()

        # Agregar campos al formulario
        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Información de Contacto:", self.contact_info_input)
        form_layout.addRow("Giro de la empresa:", self.type_of_service_input)

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
            contact_info = self.contact_info_input.text().strip()
            type_of_service = self.type_of_service_input.text().strip()
            self.provider = Provider(
                name=name, contact_info=contact_info, type_of_service=type_of_service
            )
            return True
        except ValueError as e:
            QMessageBox.critical(self, "Error de Validación", str(e))
            return False

    def accept(self) -> None:
        """Se llama cuando se presiona el botón Aceptar"""
        if self.validate_data():
            super().accept()

    def get_data(self) -> Provider:
        """Devuelve los datos del empleado ingresados"""
        return self.provider
