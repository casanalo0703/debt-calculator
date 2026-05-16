# src/application/dtos/debt_dto.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DebtDTO(BaseModel):
    """Data Transfer Object for Debt operations."""
    id: int | None = None
    client_id: int
    amount: float
    due_date: datetime # Stored as YYYY-MM-DD in DB, but use datetime for DTO clarity
    description: Optional[str] = None
    ticket_number: Optional[str] = None

class ListDebtsDTO(BaseModel):
    debt_id: int
    client_id: int
    amount: float
    due_date: datetime
    description: Optional[str] = None
    ticket_number: Optional[str] = None