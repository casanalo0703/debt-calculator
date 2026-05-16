# src/application/services/employee_service.py
from typing import List, Optional
from ..repositories.employee_repository import EmployeeRepository
from ..dtos.employee_dto import EmployeeDTO, ListEmployeesDTO
from domain.models.employee import Employee
from domain.exceptions.domain_exceptions import DomainException # Assuming this handles general errors
from src.application.events.event_bus import EventBus 

class EmployeeService:
    """Use Case Service for managing employee records."""

    def __init__(self, employee_repo: EmployeeRepository, event_bus: EventBus):
        # Dependency Inversion: Depends on abstract repository port and event bus
        self.employee_repo = employee_repo
        self.event_bus = event_bus

    def create_employee(self, name: str, position: str) -> EmployeeDTO:
        """Use Case: Creates a new active employee."""
        if not name or not position:
            raise ValueError("Name and position are required.")

        new_employee = Employee(name=name, position=position, is_active=True)
        
        try:
            saved_employee = self.employee_repo.save(new_employee)
        except Exception as e:
            raise RuntimeError(f"Failed to persist employee data: {e}")

        # Publish event
        self.event_bus.publish(ClientUpdated(client_id=0, fields_changed={"name": saved_employee.name})) # Placeholder for proper Event
        
        return EmployeeDTO(**{
            "id": saved_employee.id, 
            "name": saved_employee.name, 
            "position": saved_employee.position, 
            "is_active": True, 
            "hired_at": saved_employee.hired_at
        })

    def get_employee(self, employee_id: int) -> Optional[EmployeeDTO]:
        """Use Case: Retrieves an employee's details by ID."""
        try:
            employee = self.employee_repo.get_by_id(employee_id)
            if not employee:
                raise DomainException(f"Employee with ID {employee_id} not found.")
            return EmployeeDTO(**{
                "id": employee.id, 
                "name": employee.name, 
                "position": employee.position, 
                "is_active": employee.is_active, 
                "hired_at": employee.hired_at
            })
        except DomainException as e:
             print(f"Employee retrieval failed: {e}")
             return None

    def list_all_employees(self) -> List[ListEmployeesDTO]:
        """Use Case: Lists all active employees."""
        try:
            employees = self.employee_repo.find_active_all()
            dtos = [ListEmployeesDTO(**{
                "employee_id": e.id, 
                "name": e.name, 
                "position": e.position
            }) for e in employees]
            return dtos
        except Exception as e:
            print(f"Error listing employees: {e}")
            return []

    def deactivate_employee(self, employee_id: int) -> bool:
        """Use Case: Soft deletes/deactivates an employee."""
        success = self.employee_repo.deactivate(employee_id)
        if success:
             # Publish event on deactivation (Placeholder for proper Event)
            return True
        return False