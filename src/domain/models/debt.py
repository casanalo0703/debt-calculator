# src/domain/models/debt.py
from datetime import datetime
from typing import Optional
from ..value_objects.money import Money  # Use the VO


class Debt:
    """Aggregate Root representing a debt obligation."""

    def __init__(
        self,
        id: int | None = None,
        client_id: int = 0,
        amount: float = 0.0,
        due_date: str = "",
        description: Optional[str] = None,
        ticket_number: Optional[str] = None,
        created_at: datetime = None,
    ):
        self.id: int | None = id
        self.client_id: int = client_id
        # Use Money VO for internal consistency check
        self._amount = Money(amount=float(amount))
        self.due_date: str = (
            due_date  # YYYY-MM-DD format expected from persistence (keep string for DB layer compatibility)
        )
        self.description: Optional[str] = description
        self.ticket_number: Optional[str] = ticket_number
        self.created_at: datetime = created_at if created_at else datetime.now()

    @property
    def amount(self) -> Money:
        return self._amount

    # Methods using the VO for calculations
    def get_remaining_balance(self, payments: list["Payment"]) -> float:
        """Calculates the remaining balance after accounting for payments."""
        total_paid = sum(
            p.amount.amount for p in payments if isinstance(p, Payment)
        )  # Type check needed
        return max(0.0, self._amount.amount - total_paid)

    def is_overdue(self, check_date: datetime = None) -> bool:
        """Checks if the debt is overdue relative to a given date."""
        if not check_date:
            check_date = datetime.now()
        return self.due_date < check_date.strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Debt(id={self.id}, amount={self._amount}, due='{self.due_date}')>"
