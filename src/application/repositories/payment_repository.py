# src/application/repositories/payment_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.payment import Payment # Assuming the domain model exists later

class PaymentRepository(ABC):
    """Abstract Port for Payment data persistence."""

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Retrieves a full Payment aggregate by ID. Returns None if not found."""
        pass

    @abstractmethod
    def find_all_for_client(self, client_id: int) -> List[Payment]:
        """Retrieves all payments associated with a given client."""
        pass

    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        """Persists or updates a Payment aggregate. Returns the saved entity."""
        pass