# src/application/services/client_service.py
from typing import List, Optional
from ..repositories.client_repository import ClientRepository
from ..dtos.client_dto import ClientDTO, ListClientsDTO
from domain.models.client import Client
from domain.exceptions.domain_exceptions import ClientNotFound, ClientValidationError
from src.application.events.event_bus import EventBus # Use the global bus for now

class ClientService:
    """Use Case Service for managing client records."""

    def __init__(self, client_repo: ClientRepository, event_bus: EventBus):
        # Dependency Inversion: Depends on abstract repository and event bus (Ports)
        self.client_repo = client_repo
        self.event_bus = event_bus

    def create_client(self, name: str, phone: str, email: str) -> ClientDTO:
        """Use Case: Creates a new client record."""
        # 1. Domain Validation (Using VO logic would be better here, but using raw checks for now)
        if not name or len(name) < 2:
            raise ClientValidationError("Client name must be at least 2 characters long.")

        new_client = Client(name=name, phone=phone, email=email) # Domain Model instantiation
        
        # 2. Persistence (Calling the repository port)
        try:
            saved_client = self.client_repo.save(new_client)
        except Exception as e:
            raise RuntimeError(f"Failed to persist client data: {e}")

        # 3. Event Publishing (Decoupling UI/other services from the save operation)
        self.event_bus.publish(ClientCreated(client_id=saved_client.id!, name=saved_client.name))

        return ClientDTO.from_domain(saved_client)

    def get_client(self, client_id: int) -> Optional[ClientDTO]:
        """Use Case: Retrieves a client's details by ID."""
        try:
            client = self.client_repo.get_by_id(client_id)
            if not client:
                raise ClientNotFound(client_id)
            return ClientDTO.from_domain(client)
        except ClientNotFound as e:
            print(f"Client retrieval failed: {e}") # Should handle in UI layer properly
            return None

    def list_all_clients(self) -> List[ListClientsDTO]:
        """Use Case: Lists all active clients."""
        try:
            clients = self.client_repo.find_all()
            dtos = [ClientDTO.from_domain(c).model_dump(mode='json') for c in clients] # Using model_dump placeholder
            # Simplified list return structure to match DTO usage pattern
            return [ListClientsDTO(**dto) for dto in dtos] 

        except Exception as e:
            print(f"Error listing clients: {e}")
            return []