from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Payment(BaseModel):
    id: Optional[int] = None
    client_id: int
    debt_id: Optional[int]
    amount: float = Field(gt=0)
    date: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None
    ticket_number: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "client_id": 1,
                "amount": 100.50,
                "date": "2023-08-02T10:30:00",
                "description": "Pago mensual",
            }
        }
