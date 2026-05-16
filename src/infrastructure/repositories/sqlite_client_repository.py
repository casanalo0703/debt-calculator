# src/infrastructure/repositories/sqlite_client_repository.py
from typing import List, Optional
from ..application.repositories.client_repository import ClientRepository
from domain.models.client import Client # Assuming Client model is defined in domain/models/
from database.db import Database # Using the existing DB class

class SQLiteClientRepository(ClientRepository):
    """Implementation of ClientRepository using raw SQLite connections."""
    def __init__(self, db: Database):
        self._db = db

    def get_by_id(self, client_id: int) -> Optional[Client]:
        # Uses existing db.get_client() method
        return self._db.get_client(client_id)

    def find_all(self) -> List[Client]:
        # Uses existing db.get_all_clients() method
        return self._db.get_all_clients()

    def save(self, client: Client) -> Client:
        """Persists or updates a Client aggregate."""
        if not client.id:
            # New client
            client_id = self._db.add_client(client)
            if client_id is None:
                raise Exception("Failed to save new client.")
            return client # In reality, we might need to update the object with the real ID

        else:
            # Existing client (update logic)
            self._db.update_client(client.id, client)
            return client

    def delete(self, client_id: int) -> bool:
        # For now, we will just check if the record exists and assume success for simplicity 
        # until soft-delete logic is fully fleshed out in domain/models/client.py
        try:
            # Check existence first
            if self._db.get_client(client_id):
                # TODO: Implement actual soft delete logic based on domain model
                print(f"Soft deleting client {client_id} placeholder.") 
                return True
            return False
        except Exception as e:
            print(f"Error during deletion: {e}")
            return False