from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ClientDTO(BaseModel):
    """Data Transfer Object for Client operations."""
    id: int | None = None
    name: str
    phone: str
    email: str
    created_at: datetime

    @classmethod
    def from_domain(cls, client: 'Client'):
        # Helper to convert domain model to DTO
        return cls(
            id=client.id,
            name=client.name,
            phone=client.phone,
            email=client.email,
            created_at=client.created_at
        )

class DebtDTO(BaseModel):
    """Data Transfer Object for Debt operations."""
    id: int | None = None
    client_id: int
    amount: float
    due_date: datetime # Stored as YYYY-MM-DD in DB, but use datetime for DTO clarity
    description: Optional[str] = None
    ticket_number: Optional[str] = None

class PaymentDTO(BaseModel):
    """Data Transfer Object for Payment operations."""
    id: int | None = None
    client_id: int
    debt_id: int | None = None
    amount: float
    date: datetime # Stored as YYYY-MM-DD HH:MM:SS in DB, but use datetime for DTO clarity
    description: Optional[str] = None

class ListClientsDTO(BaseModel):
    client_id: int
    name: str
    phone: str
    email: str
    created_at: datetime

class ListDebtsDTO(BaseModel):
    debt_id: int
    client_id: int
    amount: float
    due_date: datetime
    description: Optional[str] = None
    ticket_number: Optional[str] = None

class ListPaymentsDTO(BaseModel):
    payment_id: int
    client_id: int
    debt_id: int | None = None
    amount: float
    date: datetime
    description: Optional[str] = None