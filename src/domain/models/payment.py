# src/domain/models/payment.py
from datetime import datetime
from typing import Optional
from ..value_objects.money import Money


class Payment:
    """Aggregate Root representing a payment made against a debt."""

    def __init__(
        self,
        id: int | None = None,
        client_id: int = 0,
        debt_id: int | None = None,
        amount: float = 0.0,
        date: datetime = None,
        description: Optional[str] = None,
        ticket_number: Optional[str] = None,
    ):
        self.id: int | None = id
        self.client_id: int = client_id
        self.debt_id: int | None = debt_id
        # Use Money VO for internal consistency check
        self._amount = Money(amount=float(amount))
        self.date: datetime = date if date else datetime.now()
        self.description: Optional[str] = description
        self.ticket_number: Optional[str] = ticket_number

    @property
    def amount(self) -> Money:
        return self._amount

    # Expose simple float for compatibility with older DB methods, but prefer using .amount property
    @amount.setter
    def amount(self, value: float):
        from src.domain.value_objects.money import Money

        self._amount = Money(amount=float(value))

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount.amount:.2f})>"
