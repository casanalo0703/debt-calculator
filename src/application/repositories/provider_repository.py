# src/application/repositories/provider_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.provider import Provider # Assuming model exists

class ProviderRepository(ABC):
    """Abstract Port for Provider data persistence."""

    @abstractmethod
    def get_by_id(self, provider_id: int) -> Optional[Provider]:
        """Retrieves a full Provider aggregate by ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Provider]:
        """Retrieves all providers."""
        pass

    @abstractmethod
    def save(self, provider: Provider) -> Provider:
        """Persists or updates a Provider aggregate. Returns the saved entity."""
        pass

    @abstractmethod
    def delete(self, provider_id: int) -> bool:
        """Deletes a provider record."""
        pass