from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QLabel,
    QPushButton,
    QGroupBox,
)
from datetime import datetime
import calendar

from database.db import Database


class ClientDetailsDialog(QDialog):
    def __init__(
        self,
        parent: None = None,
        db: Database | None = None,
        client_id: int | None = None,
    ):
        super().__init__(parent)
        self.db = db
        self.client_id = client_id
        self.client = self.db.get_client(client_id)
        self.setWindowTitle(f"Detalles de Cliente: {self.client.name}")
        self.setMinimumSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Selector de mes y año
        filter_layout = QHBoxLayout()

        self.month_combo = QComboBox()
        self.month_combo.addItems(calendar.month_name[1:])
        current_month = datetime.now().month
        self.month_combo.setCurrentIndex(current_month - 1)

        self.year_combo = QComboBox()
        current_year = datetime.now().year
        self.year_combo.addItems(
            [str(year) for year in range(current_year - 5, current_year + 1)]
        )
        self.year_combo.setCurrentText(str(current_year))

        filter_layout.addWidget(QLabel("Mes:"))
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(QLabel("Año:"))
        filter_layout.addWidget(self.year_combo)

        update_btn = QPushButton("Filtrar por Fecha")
        update_btn.clicked.connect(self.filter_transactions)
        filter_layout.addWidget(update_btn)

        # Agregar botón para mostrar todo
        show_all_btn = QPushButton("Mostrar Todo")
        show_all_btn.clicked.connect(self.load_all_transactions)
        filter_layout.addWidget(show_all_btn)

        layout.addLayout(filter_layout)

        # Tablas de deudas y pagos
        tables_layout = QHBoxLayout()

        # Tabla de deudas
        debts_group = QGroupBox("Deudas del Mes")
        debts_layout = QVBoxLayout()
        self.debts_table = QTableWidget()
        self.debts_table.setColumnCount(4)
        self.debts_table.setHorizontalHeaderLabels(
            [
                "Monto",
                "Fecha de Creación",
                "Descripción",
                "Número de Ticket/Factura",
            ]
        )
        debts_layout.addWidget(self.debts_table)
        debts_group.setLayout(debts_layout)
        tables_layout.addWidget(debts_group)

        # Tabla de pagos
        payments_group = QGroupBox("Pagos del Mes")
        payments_layout = QVBoxLayout()
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels(
            ["Monto", "Fecha de Pago", "Descripción", "Número de Ticket/Factura"]
        )
        payments_layout.addWidget(self.payments_table)
        payments_group.setLayout(payments_layout)
        tables_layout.addWidget(payments_group)

        layout.addLayout(tables_layout)

        # Resumen del mes
        summary_group = QGroupBox("Resumen del Mes")
        summary_layout = QHBoxLayout()
        self.total_debts_label = QLabel("Total Deudas: $0.00")
        self.total_payments_label = QLabel("Total Pagos: $0.00")
        self.balance_label = QLabel("Balance: $0.00")
        summary_layout.addWidget(self.total_debts_label)
        summary_layout.addWidget(self.total_payments_label)
        summary_layout.addWidget(self.balance_label)
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)

        self.setLayout(layout)
        # Cargar todas las transacciones al inicio
        self.load_all_transactions()

    def load_all_transactions(self) -> None:
        """Carga todas las transacciones sin filtro de fecha"""
        try:
            total_debts = 0.0
            total_payments = 0.0

            # Cargar todas las deudas
            debts = self.db.get_all_debts_by_client(self.client_id)
            self.debts_table.setRowCount(len(debts))

            print(f"Deudas encontradas: {len(debts)}")

            for i, debt in enumerate(debts):
                self.debts_table.setItem(i, 0, QTableWidgetItem(f"${debt.amount:.2f}"))
                self.debts_table.setItem(
                    i, 1, QTableWidgetItem(debt.created_at.strftime("%d/%m/%Y"))
                )
                self.debts_table.setItem(
                    i, 2, QTableWidgetItem(str(debt.description or ""))
                )
                self.debts_table.setItem(
                    i, 3, QTableWidgetItem(str(debt.ticket_number or ""))
                )
                total_debts += debt.amount

            # Cargar todos los pagos
            payments = self.db.get_all_payments_by_client(self.client_id)
            self.payments_table.setRowCount(len(payments))

            print(f"Pagos encontrados: {len(payments)}")

            for i, payment in enumerate(payments):
                self.payments_table.setItem(
                    i, 0, QTableWidgetItem(f"${payment.amount:.2f}")
                )
                self.payments_table.setItem(
                    i, 1, QTableWidgetItem(payment.date.strftime("%d/%m/%Y"))
                )
                self.payments_table.setItem(
                    i, 2, QTableWidgetItem(payment.description or "")
                )
                self.payments_table.setItem(
                    i, 3, QTableWidgetItem(payment.ticket_number or "")
                )
                total_payments += payment.amount

            self.update_summary(total_debts, total_payments)

        except Exception as e:
            print(f"Error al cargar todas las transacciones: {str(e)}")
            raise e

    def filter_transactions(self) -> None:
        """Filtra las transacciones por mes y año seleccionados"""
        try:
            self.load_filtered_transactions()
        except Exception as e:
            print(f"Error al filtrar transacciones: {str(e)}")
            raise e

    def update_summary(self, total_debts: float, total_payments: float) -> None:
        """Actualiza las etiquetas de resumen"""
        self.total_debts_label.setText(f"Total Deudas: ${total_debts:.2f}")
        self.total_payments_label.setText(f"Total Pagos: ${total_payments:.2f}")
        self.balance_label.setText(f"Balance: ${total_payments - total_debts:.2f}")

        # Ajustar tamaño de columnas
        self.debts_table.resizeColumnsToContents()
        self.payments_table.resizeColumnsToContents()

    def load_filtered_transactions(self) -> None:
        try:
            month = self.month_combo.currentIndex() + 1
            year = int(self.year_combo.currentText())
            total_debts = 0.0
            total_payments = 0.0

            # Cargar deudas
            debts = self.db.get_debts_by_month_and_client(month, year, self.client_id)
            self.debts_table.setRowCount(len(debts))  # Establecer número de filas

            print(f"Deudas encontradas: {len(debts)}")  # Debug

            for i, debt in enumerate(debts):
                # Los índices deben coincidir con el orden de setHorizontalHeaderLabels
                self.debts_table.setItem(i, 0, QTableWidgetItem(f"${debt.amount:.2f}"))
                self.debts_table.setItem(
                    i, 1, QTableWidgetItem(debt.created_at.strftime("%d/%m/%Y"))
                )
                self.debts_table.setItem(
                    i, 2, QTableWidgetItem(str(debt.description or ""))
                )
                self.debts_table.setItem(
                    i, 3, QTableWidgetItem(str(debt.ticket_number or ""))
                )
                total_debts += debt.amount
                print(f"Deuda {i+1}: {debt.amount}")  # Debug

            # Cargar pagos
            payments = self.db.get_payments_by_month_and_client(
                month, year, self.client_id
            )
            self.payments_table.setRowCount(len(payments))

            print(f"Pagos encontrados: {len(payments)}")  # Debug

            for i, payment in enumerate(payments):
                self.payments_table.setItem(
                    i, 0, QTableWidgetItem(f"${payment.amount:.2f}")
                )
                self.payments_table.setItem(
                    i, 1, QTableWidgetItem(payment.date.strftime("%d/%m/%Y"))
                )
                self.payments_table.setItem(
                    i, 2, QTableWidgetItem(payment.description or "")
                )
                self.payments_table.setItem(
                    i, 3, QTableWidgetItem(payment.ticket_number or "")
                )
                total_payments += payment.amount
                print(f"Pago {i+1}: {payment.amount}")  # Debug

            # Actualizar resumen
            self.total_debts_label.setText(f"Total Deudas: ${total_debts:.2f}")
            self.total_payments_label.setText(f"Total Pagos: ${total_payments:.2f}")
            self.balance_label.setText(f"Balance: ${total_payments - total_debts:.2f}")

            # Ajustar tamaño de columnas
            self.debts_table.resizeColumnsToContents()
            self.payments_table.resizeColumnsToContents()

        except Exception as e:
            print(f"Error al cargar transacciones: {str(e)}")
            raise e
