from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Payment(BaseModel):
    id: int
    client_id: int
    amount: float = Field(gt=0)  # gt=0 asegura que el monto sea positivo
    date: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "client_id": 1,
                "amount": 100.50,
                "date": "2023-08-02T10:30:00",
                "description": "Pago mensual"
            }
        }