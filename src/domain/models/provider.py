# src/domain/models/provider.py
from datetime import datetime
from typing import Optional

class Provider:
    """Aggregate Root representing a service provider."""
    def __init__(self, id: int | None = None, name: str = "", contact_info: str = "", type_of_service: str = "", created_at: datetime = None):
        self.id: int | None = id
        self.name: str = name
        self.contact_info: str = contact_info
        self.type_of_service: str = type_of_service
        self.created_at: datetime = created_at if created_at else datetime.now()

    def __repr__(self):
        return f"<Provider(id={self.id}, name='{self.name}')>"