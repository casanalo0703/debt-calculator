from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Provider(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=2, max_length=100, pattern=r"^[a-zA-Z\s]+$")
    contact_info: str = Field(min_length=2, max_length=100)
    type_of_service: str = Field(min_length=2, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
