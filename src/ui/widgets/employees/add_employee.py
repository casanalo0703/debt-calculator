from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDialogButtonBox,
)
from models.employee import Employee, Position  # Ensure Position is imported


class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee: Employee | None = None):
        super().__init__(parent)
        self.original_employee = employee
        self.setWindowTitle(
            "Editar Empleado" if employee else "Registrar Nuevo Empleado"
        )
        self.setup_ui()
        if employee:
            self.populate_fields(employee)

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 1. Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: Juan Pérez")

        # 2. Position Dropdown (QComboBox)
        self.position_input = QComboBox()
        # Populate the dropdown with the values from your Enum
        for pos in Position:
            self.position_input.addItem(pos.value, pos)

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Puesto:", self.position_input)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def populate_fields(self, employee: Employee) -> None:
        self.name_input.setText(employee.name)
        index = self.position_input.findData(employee.position)
        if index >= 0:
            self.position_input.setCurrentIndex(index)

    def validate_data(self) -> bool:
        try:
            name = self.name_input.text().strip()
            position = self.position_input.currentData()

            if self.original_employee:
                self.employee = Employee(
                    id=self.original_employee.id,
                    name=name,
                    position=position,
                    is_active=self.original_employee.is_active,
                    hired_at=self.original_employee.hired_at,
                    layoff_at=self.original_employee.layoff_at,
                )
            else:
                self.employee = Employee(name=name, position=position)

            return True
        except ValueError as e:
            QMessageBox.critical(self, "Error de Validación", str(e))
            return False

    def accept(self) -> None:
        if self.validate_data():
            super().accept()

    def get_data(self) -> Employee:
        return self.employee
