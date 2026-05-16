# src/application/repositories/client_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..dtos.client_dto import ClientDTO
from domain.models.client import Client # Assuming the domain model exists later

class ClientRepository(ABC):
    """Abstract Port for Client data persistence."""

    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """Retrieves a full Client aggregate by ID. Returns None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> List[Client]:
        """Retrieves all active clients."""
        pass

    @abstractmethod
    def save(self, client: Client) -> Client:
        """Persists or updates a Client aggregate. Returns the saved entity."""
        pass

    @abstractmethod
    def delete(self, client_id: int) -> bool:
        """Marks or soft-deletes a client."""
        pass