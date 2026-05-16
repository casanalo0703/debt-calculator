# src/application/dtos/provider_dto.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProviderDTO(BaseModel):
    id: int | None = None
    name: str
    contact_info: str
    type_of_service: str
    created_at: datetime