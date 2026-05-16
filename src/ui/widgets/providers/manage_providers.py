from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QPushButton,
    QGroupBox,
    QHeaderView,
)

from database.db import Database
from ui.widgets.providers.add_provider import ProviderDialog


class ManageProviders(QDialog):

    def __init__(
        self,
        db: Database,
        parent: None = None,
    ):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Administrar Empleados")
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        buttons_group = QGroupBox("Acciones")
        buttons_layout = QHBoxLayout()
        add_provider_btn = QPushButton("Agregar Proveedor")
        remove_provider_btn = QPushButton("Eliminar Proveedor")
        buttons_layout.addWidget(add_provider_btn)
        buttons_layout.addWidget(remove_provider_btn)
        buttons_group.setLayout(buttons_layout)
        add_provider_btn.clicked.connect(self.add_provider)
        remove_provider_btn.clicked.connect(self.remove_provider)

        tables_layout = QHBoxLayout()
        providers_group = QGroupBox("Proveedores")
        providers_layout = QVBoxLayout()
        self.providers_table = QTableWidget()
        self.providers_table.setColumnCount(4)
        self.providers_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Información de Contacto", "Giro de la empresa"]
        )
        self.providers_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.providers_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        providers_layout.addWidget(self.providers_table)
        providers_group.setLayout(providers_layout)
        tables_layout.addWidget(providers_group)
        main_layout.addWidget(buttons_group)
        main_layout.addLayout(tables_layout)
        self.setLayout(main_layout)
        self.load_providers()

    def load_providers(self) -> None:
        providers = self.db.get_all_providers()
        self.providers_table.setRowCount(len(providers))
        for i, provider in enumerate(providers):
            for j, value in enumerate(provider):
                self.providers_table.setItem(i, j, QTableWidgetItem(str(value)))

    def add_provider(self) -> None:
        dialog = ProviderDialog(self)
        if dialog.exec():
            try:
                provider = dialog.get_data()
                self.db.add_provider(provider)
                QMessageBox.information(
                    self, "Éxito", "Proveedor registrado correctamente"
                )
                self.load_providers()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al registrar proveedor: {str(e)}"
                )

    def remove_provider(self) -> None:
        selected_items = self.providers_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Advertencia", "Seleccione un proveedor para eliminar"
            )
            return
        row = selected_items[0].row()
        provider_id = self.providers_table.item(row, 0).text()
        try:
            self.db.remove_provider_by_id(int(provider_id))
            QMessageBox.information(self, "Éxito", "Proveedor eliminado correctamente")
            self.load_providers()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al eliminar proveedor: {str(e)}"
            )
