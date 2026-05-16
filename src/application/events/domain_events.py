# src/application/events/domain_events.py
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    timestamp: datetime = None

@dataclass(frozen=True)
class ClientCreated(DomainEvent):
    client_id: int
    name: str

@dataclass(frozen=True)
class ClientUpdated(DomainEvent):
    client_id: int
    fields_changed: dict[str, any]

@dataclass(frozen=True)
class DebtRecorded(DomainEvent):
    debt_id: int
    client_id: int
    amount: float

@dataclass(frozen=True)
class PaymentAdded(DomainEvent):
    payment_id: int
    debt_id: int
    client_id: int
    amount: float

# Add more event types as services are developed...