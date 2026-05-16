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
from models.employee import Employee, Position
from ui.widgets.employees.add_employee import EmployeeDialog


class ManageEmployees(QDialog):

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
        add_employee_btn = QPushButton("Agregar Empleado")
        edit_employee_btn = QPushButton("Editar Empleado")
        remove_employee_btn = QPushButton("Eliminar Empleado")
        buttons_layout.addWidget(add_employee_btn)
        buttons_layout.addWidget(edit_employee_btn)
        buttons_layout.addWidget(remove_employee_btn)
        buttons_group.setLayout(buttons_layout)
        add_employee_btn.clicked.connect(self.add_employee)
        edit_employee_btn.clicked.connect(self.edit_employee)
        remove_employee_btn.clicked.connect(self.remove_employee)

        tables_layout = QHBoxLayout()
        employees_group = QGroupBox("Empleados")
        employees_layout = QVBoxLayout()
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(3)
        self.employees_table.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto"])
        employees_layout.addWidget(self.employees_table)
        employees_group.setLayout(employees_layout)
        tables_layout.addWidget(employees_group)
        main_layout.addWidget(buttons_group)
        main_layout.addLayout(tables_layout)
        self.employees_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.employees_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self.employees_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.employees_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.setLayout(main_layout)
        self.load_employees()

    def load_employees(self) -> None:
        employees = self.db.get_all_employees()
        self.employees_table.setRowCount(len(employees))
        for i, employee in enumerate(employees):
            for j, value in enumerate(employee):
                self.employees_table.setItem(i, j, QTableWidgetItem(str(value)))

    def add_employee(self) -> None:
        dialog = EmployeeDialog(self)
        if dialog.exec():
            try:
                employee = dialog.get_data()
                self.db.add_employee(employee)
                QMessageBox.information(
                    self, "Éxito", "Empleado registrado correctamente"
                )
                self.load_employees()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al registrar empleado: {str(e)}"
                )

    def edit_employee(self) -> None:
        selected_items = self.employees_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Advertencia", "Seleccione un empleado para editar"
            )
            return

        row = selected_items[0].row()
        employee_id = int(self.employees_table.item(row, 0).text())
        employee_name = self.employees_table.item(row, 1).text()
        position_text = self.employees_table.item(row, 2).text()

        try:
            position = Position(position_text)
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Puesto de empleado inválido.")
            return

        employee = Employee(id=employee_id, name=employee_name, position=position)
        dialog = EmployeeDialog(self, employee=employee)
        if dialog.exec():
            try:
                updated_employee = dialog.get_data()
                self.db.update_employee(employee_id, updated_employee)
                QMessageBox.information(
                    self, "Éxito", "Empleado actualizado correctamente"
                )
                self.load_employees()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al actualizar empleado: {str(e)}"
                )

    def remove_employee(self) -> None:
        selected_items = self.employees_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Advertencia", "Seleccione un empleado para eliminar"
            )
            return
        row = selected_items[0].row()
        employee_id = self.employees_table.item(row, 0).text()
        try:
            self.db.remove_employee_by_id(int(employee_id))
            QMessageBox.information(self, "Éxito", "Empleado eliminado correctamente")
            self.load_employees()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar empleado: {str(e)}")
