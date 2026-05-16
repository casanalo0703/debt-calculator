# src/domain/models/client.py
from datetime import datetime
from typing import Optional
from ..value_objects.phone_number import PhoneNumber  # Use the VO


class Client:
    """Aggregate Root representing a client."""

    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        phone: PhoneNumber = None,
        email: str = "",
        created_at: datetime = None,
    ):
        # Simple representation for domain logic (uses basic types for now)
        self.id: int | None = id
        self.name: str = name
        self.phone: PhoneNumber = (
            phone if phone else PhoneNumber(raw="")
        )  # Use VO instance
        self.email: str = email
        self.created_at: datetime = created_at if created_at else datetime.now()

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', phone={self.phone.raw})>"
