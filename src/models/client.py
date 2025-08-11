from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from datetime import datetime


class Client(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=2, max_length=100, pattern=r"^[a-zA-Z\s]+$")
    phone: PhoneNumber
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
