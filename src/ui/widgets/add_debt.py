from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDateEdit,
    QDialogButtonBox,
)
from PySide6.QtCore import QDate
from database.db import Database
from models.client import Client
from models.debt import Debt


class DebtDialog(QDialog):
    def __init__(self, parent: None = None, db: Database | None = None):
        super().__init__(parent)
        self.db = db
        self.selected_client_id = None
        self.setWindowTitle("Agregar Nueva Deuda")
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        search_layout = QHBoxLayout()
        self.client_search = QLineEdit()
        self.client_search.setPlaceholderText("Buscar cliente...")
        self.client_search.textChanged.connect(self.search_clients)
        search_layout.addWidget(self.client_search)

        self.client_combo = QComboBox()
        self.client_combo.currentIndexChanged.connect(self.on_client_selected)
        form_layout.addRow("Cliente:", search_layout)
        form_layout.addRow("Seleccionar:", self.client_combo)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")

        self.due_date = QDateEdit()
        self.due_date.setDate(QDate.currentDate())
        self.due_date.setCalendarPopup(True)

        self.description = QLineEdit()
        self.ticket_number = QLineEdit()

        form_layout.addRow("Monto:", self.amount_input)
        form_layout.addRow("Fecha aproximada de vencimiento:", self.due_date)
        form_layout.addRow("Descripción:", self.description)
        form_layout.addRow("Número de Ticket/factura:", self.ticket_number)

        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def load_clients(self) -> None:
        """Carga todos los clientes en el combo box"""
        self.clients = self.db.get_all_clients()
        self.update_client_combo(self.clients)

    def update_client_combo(self, clients: list[Client]) -> None:
        """Actualiza el combo box con la lista de clientes filtrada"""
        self.client_combo.clear()
        self.client_combo.addItem("Seleccione un cliente", None)
        for client in clients:
            self.client_combo.addItem(f"{client.name} ({client.phone})", client.id)

    def search_clients(self, text: str) -> None:
        """Filtra los clientes según el texto de búsqueda"""
        if not text:
            filtered_clients = self.clients
        else:
            text = text.lower()
            filtered_clients = [
                client
                for client in self.clients
                if text in client.name.lower() or text in client.phone
            ]
        self.update_client_combo(filtered_clients)

    def on_client_selected(self, index: int) -> None:
        """Guarda el ID del cliente seleccionado"""
        self.selected_client_id = self.client_combo.currentData()

    def validate_and_accept(self) -> None:
        """Valida los datos antes de aceptar"""
        if not self.selected_client_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return

        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                raise ValueError("El monto debe ser mayor a 0")
        except ValueError:
            QMessageBox.warning(self, "Error", "Monto inválido")
            return

        self.accept()

    def get_data(self):
        """Retorna los datos de la deuda"""
        return Debt(
            client_id=self.selected_client_id,
            amount=float(self.amount_input.text()),
            due_date=self.due_date.date().toPython(),
            description=self.description.text(),
            ticket_number=self.ticket_number.text(),
        )
