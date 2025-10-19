from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QGroupBox,
    QTableWidgetItem,
)
from database.db import Database
from ui.widgets.add_payments import PaymentDialog
from ui.widgets.client_dialog import ClientDialog
from ui.widgets.list_clients import ClientListDialog
from ui.widgets.add_debt import DebtDialog


class MainWindow(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.setWindowTitle("Administrador de Deudas")
        self.setGeometry(100, 100, 1000, 800)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Sección de botones principales
        buttons_group = QGroupBox("Acciones")
        buttons_layout = QHBoxLayout()

        add_client_btn = QPushButton("Agregar Cliente")
        add_debt_btn = QPushButton("Agregar Deuda")
        add_payment_btn = QPushButton("Registrar Pago")

        add_client_btn.clicked.connect(self.add_client)
        add_debt_btn.clicked.connect(self.add_debt)
        add_payment_btn.clicked.connect(self.add_payment)

        buttons_layout.addWidget(add_client_btn)
        buttons_layout.addWidget(add_debt_btn)
        buttons_layout.addWidget(add_payment_btn)
        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)

        # Tablas de registros
        tables_layout = QHBoxLayout()

        # Tabla de deudas recientes
        debts_group = QGroupBox("Deudas Recientes")
        debts_layout = QVBoxLayout()
        self.debts_table = QTableWidget()
        self.debts_table.setColumnCount(4)
        self.debts_table.setHorizontalHeaderLabels(
            ["Cliente", "Deuda", "Fecha", "Descripción"]
        )
        debts_layout.addWidget(self.debts_table)
        debts_group.setLayout(debts_layout)
        tables_layout.addWidget(debts_group)

        view_clients_btn = QPushButton("Ver Clientes")
        view_clients_btn.clicked.connect(self.show_clients)
        buttons_layout.addWidget(view_clients_btn)

        # Tabla de pagos recientes
        payments_group = QGroupBox("Pagos Recientes")
        payments_layout = QVBoxLayout()
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels(
            ["Cliente", "Pago", "Fecha", "Descripción"]
        )
        payments_layout.addWidget(self.payments_table)
        payments_group.setLayout(payments_layout)
        tables_layout.addWidget(payments_group)

        main_layout.addLayout(tables_layout)
        self.load_data()

    def load_data(self):
        # Cargar deudas
        debts = self.db.get_all_debts()
        self.debts_table.setRowCount(len(debts))
        for i, debt in enumerate(debts):
            for j, value in enumerate(debt):
                self.debts_table.setItem(i, j, QTableWidgetItem(str(value)))

        # Cargar pagos
        payments = self.db.get_all_payments()
        self.payments_table.setRowCount(len(payments))
        for i, payment in enumerate(payments):
            for j, value in enumerate(payment):
                self.payments_table.setItem(i, j, QTableWidgetItem(str(value)))

    def add_client(self):
        dialog = ClientDialog(self)
        if dialog.exec():
            client_data = dialog.get_data()
            try:
                client_id = self.db.add_client(client_data)
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Cliente registrado correctamente con ID: {client_id}",
                )
                self.load_data()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al registrar cliente: {str(e)}"
                )

    def add_debt(self):
        dialog = DebtDialog(self, self.db)
        if dialog.exec():
            try:
                debt_data = dialog.get_data()
                self.db.add_debt(debt_data)
                QMessageBox.information(self, "Éxito", "Deuda registrada correctamente")
                self.load_data()  # Actualizar las tablas
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al registrar deuda: {str(e)}"
                )

    def add_payment(self):
        dialog = PaymentDialog(self, self.db)
        if dialog.exec():
            try:
                payment_data = dialog.get_data()
                self.db.add_payment(payment_data)
                QMessageBox.information(self, "Éxito", "Pago registrado correctamente")
                self.load_data()  # Actualizar las tablas
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al registrar pago: {str(e)}"
                )

    def show_clients(self):
        dialog = ClientListDialog(self, self.db)
        dialog.exec()
