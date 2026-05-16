# src/application/repositories/employee_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.employee import Employee # Assuming model exists

class EmployeeRepository(ABC):
    """Abstract Port for Employee data persistence."""

    @abstractmethod
    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieves a full Employee aggregate by ID."""
        pass

    @abstractmethod
    def find_active_all(self) -> List[Employee]:
        """Finds all currently active employees."""
        pass

    @abstractmethod
    def save(self, employee: Employee) -> Employee:
        """Persists or updates an Employee aggregate. Returns the saved entity."""
        pass

    @abstractmethod
    def deactivate(self, employee_id: int) -> bool:
        """Soft deletes/deactivates an employee."""
        pass