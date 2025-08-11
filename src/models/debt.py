from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Debt(BaseModel):
    id: Optional[int] = None
    client_id: int
    amount: float
    due_date: datetime
    description: Optional[str] = None
    ticket_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
