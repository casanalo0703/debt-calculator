from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Position(str, Enum):
    VENDEDOR = "Vendedor"
    BODEGUERO = "Bodeguero"


class Employee(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=2, max_length=100, pattern=r"^[a-zA-Z\s]+$")
    position: Position
    is_active: int = Field(default=1)
    hired_at: datetime = Field(default_factory=datetime.now)
    layoff_at: Optional[datetime] = None
