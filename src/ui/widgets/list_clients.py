from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from database.db import Database
from ui.widgets.client_dialog import ClientDialog
from .client_details import ClientDetailsDialog


class ClientListDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, db: Database | None = None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Clientes")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.clients_table = QTableWidget()
        buttons_layout = QHBoxLayout()

        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(4)
        self.clients_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Teléfono", "Email"]
        )
        self.clients_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.clients_table.setSortingEnabled(True)
        self.clients_table.horizontalHeader().setSectionsClickable(True)
        self.clients_table.sortItems(1, Qt.SortOrder.AscendingOrder)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_client)

        details_button = QPushButton("Ver Detalles")
        details_button.clicked.connect(self.show_client_details)

        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(details_button)

        layout.addWidget(self.clients_table)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_clients(self):
        print("Cargando clientes...")
        clients = self.db.get_all_clients()
        self.clients_table.setSortingEnabled(False)
        self.clients_table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            id_item = QTableWidgetItem(str(client.id))
            id_item.setData(Qt.ItemDataRole.DisplayRole, client.id)
            name_item = QTableWidgetItem(client.name)
            phone_item = QTableWidgetItem(client.phone)
            email_item = QTableWidgetItem(client.email)
            self.clients_table.setItem(i, 0, id_item)
            self.clients_table.setItem(i, 1, name_item)
            self.clients_table.setItem(i, 2, phone_item)
            self.clients_table.setItem(i, 3, email_item)
        self.clients_table.setSortingEnabled(True)

    def edit_client(self):
        current_row = self.clients_table.currentRow()
        if current_row >= 0:
            client_id = int(self.clients_table.item(current_row, 0).text())
            client_data = self.db.get_client(client_id)

            dialog = ClientDialog(self)
            dialog.name_input.setText(client_data.name)
            dialog.phone_input.setText(client_data.phone.replace("+52", ""))
            dialog.email_input.setText(client_data.email)

            if dialog.exec():
                try:
                    updated_client = dialog.get_data()
                    self.db.update_client(client_id, updated_client)
                    self.load_clients()
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Error al actualizar cliente: {str(e)}"
                    )

    def show_client_details(self):
        current_row = self.clients_table.currentRow()
        if current_row >= 0:
            client_id = int(self.clients_table.item(current_row, 0).text())
            dialog = ClientDetailsDialog(self, self.db, client_id)
            dialog.exec()
