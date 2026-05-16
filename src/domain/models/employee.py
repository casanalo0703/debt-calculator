# src/domain/models/employee.py
from datetime import datetime
from typing import Optional

class Employee:
    """Aggregate Root representing an employee."""
    def __init__(self, id: int | None = None, name: str = "", position: str = "", is_active: bool = True, hired_at: datetime = None):
        self.id: int | None = id
        self.name: str = name
        self.position: str = position # Should ideally be a Value Object if complex
        self.is_active: bool = is_active
        self.hired_at: datetime = hired_at if hired_at else datetime.now()

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', active={self.is_active})>"