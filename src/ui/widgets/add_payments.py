from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDateEdit,
    QDialogButtonBox,
)
from PySide6.QtCore import QDate

from database.db import Database
from models.debt import Debt
from models.payment import Payment


class PaymentDialog(QDialog):
    def __init__(self, parent: None = None, db: Database | None = None):
        super().__init__(parent)
        self.db = db
        self.selected_debt_id = None
        self.selected_client_id = None
        self.setWindowTitle("Agregar Nuevo Pago")
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Selector de cliente
        self.client_combo = QComboBox()
        self.client_combo.currentIndexChanged.connect(self.on_client_selected)
        form_layout.addRow("Cliente:", self.client_combo)

        # Selector de deuda
        self.debt_combo = QComboBox()
        self.debt_combo.currentIndexChanged.connect(self.on_debt_selected)
        form_layout.addRow("Deuda:", self.debt_combo)

        # Campo de monto a pagar
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")

        # Campo de descripción del pago
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Descripción del pago (opcional)")

        # Selector de fecha
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)

        form_layout.addRow("Monto:", self.amount_input)
        form_layout.addRow("Fecha:", self.date)
        form_layout.addRow("Descripción:", self.description_input)

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

    def update_client_combo(self, clients: list) -> None:
        """Actualiza el combo box con la lista de clientes"""
        self.client_combo.clear()
        self.client_combo.addItem("Seleccione un cliente", None)
        for client in self.clients:
            self.client_combo.addItem(f"{client.name}", client.id)

    def on_client_selected(self, index: int) -> None:
        """Cuando se selecciona un cliente, carga sus deudas"""
        self.selected_client_id = self.client_combo.currentData()
        if self.selected_client_id:
            self.load_client_debts(self.selected_client_id)
        else:
            self.debt_combo.clear()

    def load_client_debts(self, client_id: int) -> None:
        """Carga las deudas del cliente seleccionado"""
        debts = self.db.get_debts_by_client(client_id)
        self.update_debt_combo(debts)

    def update_debt_combo(self, debts: list[Debt]) -> None:
        """Actualiza el combo box con la lista de deudas del cliente"""
        self.debt_combo.clear()
        self.debt_combo.addItem("Seleccione una deuda", None)
        for debt in debts:
            self.remaining = self.db.get_remaining_debt(debt.id)
            self.debt_combo.addItem(
                f"Deuda #{debt.id} - ${self.remaining:.2f} - {debt.description or 'Sin descripción'}",
                debt.id,
            )

    def on_debt_selected(self, index: int) -> None:
        """Guarda el ID de la deuda seleccionada y actualiza el monto sugerido"""
        self.selected_debt_id = self.debt_combo.currentData()
        if self.selected_debt_id:
            self.remaining = self.db.get_remaining_debt(self.selected_debt_id)
            self.amount_input.setText(f"{self.remaining:.2f}")

    def validate_and_accept(self) -> None:
        """Valida los datos antes de aceptar"""
        if not self.selected_client_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return

        if not self.selected_debt_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar una deuda")
            return

        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                raise ValueError("El monto debe ser mayor a 0")

            if amount > self.remaining:
                raise ValueError(
                    f"El monto excede la deuda restante (${self.remaining:.2f})"
                )

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return

        self.accept()

    def get_data(self) -> Payment:
        """Retorna los datos del pago"""
        return Payment(
            client_id=self.selected_client_id,
            debt_id=self.selected_debt_id,
            amount=float(self.amount_input.text()),
            date=self.date.date().toPython(),
            description=self.description_input.text(),
        )
