# src/infrastructure/repositories/sqlite_employee_repository.py
from typing import List, Optional
from ..application.repositories.employee_repository import EmployeeRepository
from domain.models.employee import Employee # Assuming model exists
from database.db import Database # Using the existing DB class

class SQLiteEmployeeRepository(EmployeeRepository):
    """Implementation of EmployeeRepository using raw SQLite connections."""
    def __init__(self, db: Database):
        self._db = db

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        # Missing direct fetch by ID in DB layer. Assuming we adapt the logic or keep it simple for now.
        print("Warning: get_by_id for Employee is not explicitly implemented in db.py.")
        return None

    def find_active_all(self) -> List[Employee]:
        # Uses existing db.get_all_employees() method
        raw_data = self._db.get_all_employees()
        return [
            Employee(id=row[0], name=row[1], position=row[2]) 
            for row in raw_data
        ]

    def save(self, employee: Employee) -> Employee:
        """Persists or updates an Employee aggregate."""
        if not employee.id:
            # New employee
            try:
                employee_id = self._db.add_employee(employee)
                print("Note: Assuming successful save for new employee.") # Placeholder for actual ID return
                return employee
            except Exception as e:
                raise RuntimeError(f"DB Error saving employee: {e}")

        else:
            # Existing employee (update logic)
            try:
                self._db.update_employee(employee.id, employee)
                return employee
            except Exception as e:
                raise RuntimeError(f"DB Error updating employee: {e}")


    def deactivate(self, employee_id: int) -> bool:
        """Soft deletes/deactivates an employee."""
        try:
            self._db.remove_employee_by_id(employee_id)
            print(f"Successfully soft-deleted employee ID {employee_id}")
            return True
        except Exception as e:
            print(f"Error deactivating employee {employee_id}: {e}")
            return False