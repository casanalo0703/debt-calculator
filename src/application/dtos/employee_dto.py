# src/application/dtos/employee_dto.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeDTO(BaseModel):
    id: int | None = None
    name: str
    position: str
    is_active: bool
    hired_at: datetime

class ListEmployeesDTO(BaseModel):
    employee_id: int
    name: str
    position: str