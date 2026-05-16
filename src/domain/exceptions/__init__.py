# src/domain/exceptions/domain_exceptions.py
from typing import Optional

class DomainException(Exception):
    """Base exception class for all domain-specific errors."""
    pass

class ClientNotFound(DomainException):
    """Raised when a requested client ID does not exist."""
    def __init__(self, client_id: int):
        super().__init__(f"Client with ID {client_id} not found.")
        self.client_id = client_id

class ClientValidationError(DomainException):
    """Raised for invalid client data (e.g., name too short)."""
    pass

class DebtNotFound(DomainException):
    """Raised when a requested debt ID does not exist."""
    def __init__(self, debt_id: int):
        super().__init__(f"Debt with ID {debt_id} not found.")
        self.debt_id = debt_id

class InsufficientBalance(DomainException):
    """Raised when a payment amount exceeds the available balance."""
    def __init__(self, requested: float, available: float):
        super().__init__(f"Insufficient funds. Requested: {requested:.2f}, Available: {available:.2f}")
        self.requested = requested
        self.available = available

class DebtAlreadyPaid(DomainException):
    """Raised if attempting to process payments on a fully paid debt."""
    pass

# Add more domain-specific exceptions as needed (e.g., PaymentValidationError)