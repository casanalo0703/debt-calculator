# src/application/services/debt_service.py
from typing import List, Optional
from ..repositories.debt_repository import DebtRepository
from ..dtos.debt_dto import DebtDTO, ListDebtsDTO
from domain.models.debt import Debt
from domain.value_objects.money import Money
from domain.exceptions.domain_exceptions import DebtNotFound, InsufficientBalance
from src.application.events.event_bus import EventBus # Assume global event bus is available

class DebtService:
    """Use Case Service for managing debt obligations."""

    def __init__(self, debt_repo: DebtRepository, event_bus: EventBus):
        # Dependency Inversion: Depends on abstract repository port and event bus
        self.debt_repo = debt_repo
        self.event_bus = event_bus

    def record_debt(self, client_id: int, amount: float, due_date_str: str, description: Optional[str], ticket_number: Optional[str]) -> DebtDTO:
        """Use Case: Records a new debt for a client."""
        if amount <= 0.0:
            raise ValueError("Debt amount must be positive.")

        # 1. Domain Model Creation & Validation
        new_debt = Debt(
            client_id=client_id,
            amount=amount, # This uses the float conversion in the VO setter
            due_date=due_date_str, # Expecting YYYY-MM-DD format string
            description=description,
            ticket_number=ticket_number
        )

        # 2. Persistence (Calling the repository port)
        saved_debt = None
        try:
            saved_debt = self.debt_repo.save(new_debt)
        except Exception as e:
            # Handle potential saving errors, re-raise or wrap appropriately
            print(f"Error saving debt: {e}")
            raise # Re-raise the exception to notify the caller

        finally:
            if saved_debt and hasattr(self.event_bus, 'publish'):
                 # Assuming DomainEvent usage was a placeholder, using a more concrete event name/structure if possible
                self.event_bus.publish(DebtRecorded(client_id=client_id, debt_id=saved_debt.id!, amount=amount))

        return DebtDTO(
            client_id=saved_debt.client_id,
            amount=saved_debt.amount,
            due_date=saved_debt.due_date,
            description=saved_debt.description,
            ticket_number=saved_debt.ticket_number,
        )

    def get_debt_status(self, debt_id: int) -> Optional[float]:
        """Use Case: Gets the current remaining balance for a given debt."""
        try:
            # The repository handles the complex calculation logic (Ports & Adapters interaction)
            remaining = self.debt_repo.get_remaining_debt_status(debt_id)
            return remaining
        except Exception as e:
            print(f"Error checking debt status: {e}")
            return None

    def list_debts_by_client(self, client_id: int) -> List[ListDebtsDTO]:
        """Use Case: Retrieves all active debts for a client."""
        try:
            # Fetching from the repository port
            debts = self.debt_repo.find_all_for_client(client_id)
            
            dtos = []
            for debt in debts:
                dto = DebtDTO( # Using DTO for consistency, although ListDebtsDTO exists
                    client_id=debt.client_id,
                    amount=debt.amount,
                    due_date=debt.due_date,
                    description=debt.description,
                    ticket_number=debt.ticket_number,
                )
                dtos.append(dto)
            return dtos
        except Exception as e:
            print(f"Error listing debts for client {client_id}: {e}")
            return []
