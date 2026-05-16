# src/infrastructure/repositories/sqlite_provider_repository.py
from typing import List, Optional
from ..application.repositories.provider_repository import ProviderRepository
from domain.models.provider import Provider # Assuming model exists
from database.db import Database # Using the existing DB class

class SQLiteProviderRepository(ProviderRepository):
    """Implementation of ProviderRepository using raw SQLite connections."""
    def __init__(self, db: Database):
        self._db = db

    def get_by_id(self, provider_id: int) -> Optional[Provider]:
        # Uses existing db.get_all_providers() method (We need to adapt this as it returns list)
        raw_data = self._db.get_all_providers()
        for row in raw_data:
            if row[0] == provider_id:
                return Provider(id=row[0], name=row[1], contact_info=row[2], type_of_service=row[3])
        return None

    def find_all(self) -> List[Provider]:
        # Uses existing db.get_all_providers() method
        raw_data = self._db.get_all_providers()
        return [
            Provider(id=row[0], name=row[1], contact_info=row[2], type_of_service=row[3]) 
            for row in raw_data
        ]

    def save(self, provider: Provider) -> Provider:
        """Persists or updates a Provider aggregate."""
        if not provider.id:
            # New provider
            try:
                provider_id = self._db.add_provider(provider)
                print("Note: Assuming successful save for new provider.") # Placeholder for actual ID return
                return provider
            except Exception as e:
                raise RuntimeError(f"DB Error saving provider: {e}")
        else:
             # Update logic (Skipped/Not implemented in DB adapter pass)
             print("Warning: Updating Provider is not fully implemented in the SQLiteAdapter.")
             return provider

    def delete(self, provider_id: int) -> bool:
        """Deletes a provider record."""
        try:
            self._db.remove_provider_by_id(provider_id)
            print(f"Successfully deleted provider ID {provider_id}")
            return True
        except Exception as e:
            print(f"Error deleting provider {provider_id}: {e}")
            return False