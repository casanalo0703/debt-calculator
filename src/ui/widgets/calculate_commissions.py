from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QLineEdit,
    QDateEdit,
    QGroupBox,
    QMessageBox,
    QHeaderView,
)
from PySide6.QtPrintSupport import (
    QPrinter,
    QPrintPreviewDialog,
)
from PySide6.QtCore import QPoint, Qt, QDate, QMarginsF, QRectF
from PySide6.QtGui import QFont, QPainter, QPageLayout, QPageSize, QPen, QColor

# ...resto del código...
from PySide6.QtCore import Qt, QDate
from database.db import Database
from models.employee import Employee
from models.provider import Provider

DEFAULT_COMMISION_RATE = 0.01
DEFAULT_COMMISION = 200.00


class CalculateComissionsDialog(QDialog):
    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Calcular Comisiones")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        # Configuración de fechas
        date_layout = QHBoxLayout()
        # Fecha inicial (una semana atrás por defecto)
        start_date_label = QLabel("Fecha inicial:")
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))

        # Fecha final (hoy por defecto)
        end_date_label = QLabel("Fecha final:")
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addDays(-1))

        commission_rate_label = QLabel("Porcentaje de Comisión:")
        self.commission_rate_input = QLineEdit()
        self.commission_rate_input.setText(f"{DEFAULT_COMMISION_RATE * 100:.1f}%")
        self.commission_rate_input.setMaximumWidth(100)
        self.commission_rate_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Botón para actualizar
        update_button = QPushButton("Actualizar")
        update_button.clicked.connect(self.update_table)
        print_button = QPushButton("Imprimir")
        print_button.clicked.connect(self.print_preview)
        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date)
        date_layout.addWidget(commission_rate_label)
        date_layout.addWidget(self.commission_rate_input)
        date_layout.addWidget(update_button)
        date_layout.addWidget(print_button)
        date_layout.addStretch()

        # Tabla
        self.comissions_table = QTableWidget()
        self.comissions_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.comissions_table.verticalHeader().setVisible(True)
        self.comissions_table.horizontalHeader().setVisible(True)
        self.comissions_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.comissions_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        # ... inside setup_ui ...
        self.comissions_table = QTableWidget()
        # Enable word wrapping for the whole table
        self.comissions_table.setWordWrap(True)

        # Allow the horizontal header (employee names) to wrap
        self.comissions_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.comissions_table.horizontalHeader().setMinimumSectionSize(
            100
        )  # Prevents columns from being too tiny
        # Resumen
        summary_group = QGroupBox("Resumen:")
        summary_layout = QHBoxLayout()
        self.total_sells = QLabel("Total Vendido: $0.00")
        self.total_comissions = QLabel("Total Comisiones: $0.00")
        summary_layout.addWidget(self.total_sells)
        summary_layout.addWidget(self.total_comissions)
        summary_group.setLayout(summary_layout)

        layout.addLayout(date_layout)
        layout.addWidget(self.comissions_table)
        layout.addWidget(summary_group)
        self.setLayout(layout)

    def load_data(self):
        # Obtener proveedores y empleados
        providers = [
            Provider(
                id=provider[0],
                name=provider[1],
                contact_info=provider[2],
                type_of_service=provider[3],
            )
            for provider in self.db.get_all_providers()
        ]
        employees = [
            Employee(id=employee[0], name=employee[1], position=employee[2])
            for employee in self.db.get_all_employees()
        ]

        # Configurar tabla
        self.comissions_table.setRowCount(len(providers) + 1)
        self.comissions_table.setColumnCount(len(employees) + 1)

        # Establecer encabezados
        provider_headers = [provider.name for provider in providers]
        employee_headers = [employee.name for employee in employees]
        provider_headers.append("Total Comisiones")
        employee_headers.append("Total Vendido")

        self.comissions_table.setVerticalHeaderLabels(provider_headers)
        self.comissions_table.setHorizontalHeaderLabels(employee_headers)

        # Llenar la tabla
        # En el método load_data, reemplaza el bucle por:
        for i in range(len(providers) + 1):
            for j in range(
                len(employees) + 1
            ):  # Iteramos también por la columna de total vendido
                item = QTableWidgetItem()
                is_total_column = j == len(employees)  # Última columna (Total Vendido)
                if not is_total_column:
                    is_bodeguero = employees[j].position.lower() == "bodeguero"
                else:
                    is_bodeguero = False
                is_total_row = i == len(providers)  # Última fila (Total Comisiones)

                # Caso 1: Es bodeguero y es la fila de total comisiones
                if is_bodeguero and is_total_row:
                    item.setText(f"{DEFAULT_COMMISION:.2f}")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # Caso 2: Es bodeguero pero no es la fila de total comisiones
                elif is_bodeguero and not is_total_row:
                    item.setText("0.00")
                    item.setBackground(Qt.GlobalColor.lightGray)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # Caso 3: Cualquier otro empleado
                elif (
                    (is_total_row and not is_total_column)
                    or (is_total_column and not is_total_row)
                    or (is_total_column and is_total_row)
                ):
                    item.setText("0.00")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:
                    item.setText("0.00")
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                self.comissions_table.setItem(i, j, item)

        # Ajustar tamaño de columnas y filas para que se adapten al contenido
        self.comissions_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.comissions_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Force the table to recalculate its visual layout
        self.comissions_table.resizeColumnsToContents()
        self.comissions_table.resizeRowsToContents()

    def update_table(self) -> None:
        """
        Calculates totals and updates the table.
        The bottom-right cell will now show Total Commissions.
        """
        try:
            # 1. Get the commission rate from the input
            raw_rate = self.commission_rate_input.text().replace("%", "").strip()
            commission_rate = float(raw_rate) / 100

            rows = self.comissions_table.rowCount()
            cols = self.comissions_table.columnCount()

            total_general_sales = 0.0
            total_general_commission = 0.0

            # 2. Iterate through columns (Employees) to calculate their commissions
            for j in range(cols - 1):
                employee_total_sales = 0.0

                # Identify if employee is a "Bodeguero" based on the initial setup
                is_fixed_commission = False
                # Check the bottom row for the fixed value assigned in load_data
                current_val_in_total_cell = float(
                    self.comissions_table.item(rows - 1, j).text()
                )
                if current_val_in_total_cell == DEFAULT_COMMISION:
                    is_fixed_commission = True

                # Sum sales for this specific employee
                for i in range(rows - 1):
                    cell_item = self.comissions_table.item(i, j)
                    try:
                        val = float(cell_item.text()) if cell_item else 0.0
                    except ValueError:
                        val = 0.0
                    employee_total_sales += val

                # Apply logic: Fixed rate for Bodegueros, percentage for others
                if is_fixed_commission:
                    current_emp_commission = DEFAULT_COMMISION
                else:
                    current_emp_commission = employee_total_sales * commission_rate

                # Update the bottom cell for this employee
                self.comissions_table.item(rows - 1, j).setText(
                    f"{current_emp_commission:.2f}"
                )

                total_general_sales += employee_total_sales
                total_general_commission += current_emp_commission

            # 3. Update "Total Vendido" per Provider (Rightmost Column)
            for i in range(rows - 1):
                row_sales = 0.0
                for j in range(cols - 1):
                    try:
                        row_sales += float(self.comissions_table.item(i, j).text())
                    except:
                        pass
                self.comissions_table.item(i, cols - 1).setText(f"{row_sales:.2f}")

            # 4. FIXED: Update the bottom-right corner with Total COMMISSIONS
            # Previously this showed total_general_sales
            self.comissions_table.item(rows - 1, cols - 1).setText(
                f"{total_general_commission:.2f}"
            )
            # Optional: Change the background or text color to make it stand out
            self.comissions_table.item(rows - 1, cols - 1).setForeground(QColor("blue"))

            # 5. Update the UI Summary Labels
            self.total_sells.setText(f"Total Vendido: ${total_general_sales:.2f}")
            self.total_comissions.setText(
                f"Total Comisiones: ${total_general_commission:.2f}"
            )

        except ValueError:
            QMessageBox.warning(
                self, "Entrada Inválida", "Por favor ingrese un porcentaje válido."
            )

    def print_preview(self):
        """Abre la vista previa de impresión en formato carta horizontal."""
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        page_layout = QPageLayout(
            QPageSize(QPageSize.PageSizeId.Letter),
            QPageLayout.Orientation.Landscape,
            QMarginsF(12.7, 12.7, 12.7, 12.7),  # márgenes de media pulgada (12.7 mm)
        )
        printer.setPageLayout(page_layout)

        # Abrir vista previa
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Vista previa de impresión - Comisiones")
        preview.paintRequested.connect(self.print_document)
        preview.exec_()

    def print_document(self, printer):
        """Prints the report with the title drawn LAST to ensure visibility."""
        painter = QPainter()
        if not painter.begin(printer):
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        try:
            # 1. Get Page Dimensions
            page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
            w = page_rect.width()
            h = page_rect.height()

            # Header height: 0.8 inches worth of pixels
            header_h = int(printer.resolution() * 0.8)

            # --- 2. PREPARE TABLE ---
            original_size = self.comissions_table.size()
            h_header = self.comissions_table.horizontalHeader()
            v_header = self.comissions_table.verticalHeader()

            # Hide the vertical header (removes the ghost rectangle)
            v_header.setVisible(False)

            # Measure content
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.comissions_table.setWordWrap(True)
            self.comissions_table.resizeColumnsToContents()
            self.comissions_table.resizeRowsToContents()

            content_w = h_header.length() + 20
            content_h = v_header.length() + h_header.height() + 20
            self.comissions_table.setFixedSize(content_w, content_h)

            # --- 3. RENDER TABLE FIRST ---
            target_w = w * 0.95
            target_h = (h - header_h) * 0.90
            scale = min(target_w / content_w, target_h / content_h)

            painter.save()
            # Position table below the reserved header space
            x_off = page_rect.x() + (w - (content_w * scale)) / 2
            y_off = page_rect.y() + header_h

            painter.translate(x_off, y_off)
            painter.scale(scale, scale)
            self.comissions_table.render(painter, QPoint(0, 0))
            painter.restore()

            # --- 4. DRAW TITLE LAST (Forces it on top of any table styling) ---
            painter.save()
            # Force a solid black pen and no brush interference
            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)

            # Use 28pt font (Absolute size)
            font = QFont("Arial", 28, QFont.Weight.Bold)
            painter.setFont(font)

            start_str = self.start_date.date().toString("dd/MM/yyyy")
            end_str = self.end_date.date().toString("dd/MM/yyyy")
            title_text = f"Comisiones del {start_str} al {end_str}"

            # Draw in the reserved space at the top
            title_rect = QRectF(page_rect.x(), page_rect.y(), w, header_h)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, title_text)
            painter.restore()

            # --- 5. CLEANUP ---
            v_header.setVisible(True)
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.comissions_table.setMinimumSize(800, 600)
            self.comissions_table.setMaximumSize(16777215, 16777215)
            self.comissions_table.resize(original_size)

        finally:
            painter.end()
