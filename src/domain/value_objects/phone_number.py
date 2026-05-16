# src/domain/value_objects/phone_number.py
from pydantic import BaseModel, field_validator
import re

class PhoneNumber(BaseModel):
    """Encapsulates a phone number with validation."""
    raw: str
    country_code: str = "1" # Defaulting to US country code for now

    @field_validator('raw', mode='before')
    @classmethod
    def validate_phone_format(cls, v):
        if not isinstance(v, str):
            raise TypeError("Phone number must be a string.")
        # Basic validation regex: allows digits, spaces, hyphens, parentheses, and '+' signs
        if not re.match(r"^[+?\d\s()-]{7,}$", v):
             raise ValueError("Invalid phone format.")
        return v

    @classmethod
    def parse_from_string(cls, raw_input: str) -> 'PhoneNumber':
        """Parses and validates a phone number string."""
        # Simple implementation - real world needs library like phonenumbers
        return cls(raw=raw_input)