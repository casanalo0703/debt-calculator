# src/application/repositories/debt_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.debt import Debt # Assuming the domain model exists later

class DebtRepository(ABC):
    """Abstract Port for Debt data persistence."""

    @abstractmethod
    def get_by_id(self, debt_id: int) -> Optional[Debt]:
        """Retrieves a full Debt aggregate by ID. Returns None if not found."""
        pass

    @abstractmethod
    def find_all_for_client(self, client_id: int) -> List[Debt]:
        """Retrieves all debts associated with a given client."""
        pass

    @abstractmethod
    def save(self, debt: Debt) -> Debt:
        """Persists or updates a Debt aggregate. Returns the saved entity."""
        pass

    # Potentially add methods like record_payment_on_debt if necessary here
    @abstractmethod
    def get_remaining_debt_status(self, debt_id: int) -> Optional[float]:
        """Calculates and returns the remaining balance for a debt."""
        pass