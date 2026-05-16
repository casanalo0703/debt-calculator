# src/domain/value_objects/money.py
from pydantic import BaseModel, field_validator
from typing import Union

class Money(BaseModel):
    amount: float
    currency: str = "USD" # Assuming USD for now as a default

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v < 0.0:
            raise ValueError("Amount cannot be negative.")
        return round(v, 2)

    def add(self, other: 'Money') -> 'Money':
        """Adds another Money object."""
        if self.currency != other.currency:
            raise ValueError("Cannot add money of different currencies.")
        return Money(amount=round(self.amount + other.amount, 2), currency=self.currency)

    def subtract(self, other: 'Money') -> 'Money':
        """Subtracts another Money object."""
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money of different currencies.")
        new_amount = self.amount - other.amount
        return Money(amount=max(0.0, round(new_amount, 2)), currency=self.currency)

    def is_positive(self) -> bool:
        """Checks if the amount is greater than zero."""
        return self.amount > 0.0

    @classmethod
    def from_float(cls, value: float, currency: str = "USD") -> 'Money':
        """Factory method to create Money from a raw float."""
        return cls(amount=value, currency=currency)