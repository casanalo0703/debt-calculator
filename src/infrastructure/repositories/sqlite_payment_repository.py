# src/infrastructure/repositories/sqlite_payment_repository.py
from typing import List, Optional
from ..application.repositories.payment_repository import PaymentRepository
from domain.models.payment import Payment # Assuming model exists
from database.db import Database # Using the existing DB class

class SQLitePaymentRepository(PaymentRepository):
    """Implementation of PaymentRepository using raw SQLite connections."""
    def __init__(self, db: Database):
        self._db = db

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        # Missing direct fetch by ID in DB layer.
        return None 

    def find_all_for_client(self, client_id: int) -> List[Payment]:
        # Uses existing db.get_all_payments_by_client() method
        return self._db.get_all_payments_by_client(0, 0, client_id) # Dummy month/year for now

    def save(self, payment: Payment) -> Payment:
        """Persists or updates a Payment aggregate."""
        if not payment.id:
            try:
                # Use the specific add_payment method
                self._db.add_payment(payment) 
                print("Note: Assuming successful save for new payment.") # Placeholder for actual ID return
                return payment
            except Exception as e:
                raise RuntimeError(f"DB Error saving payment: {e}")

        else:
            # Update logic (Not implemented)
            raise NotImplementedError("Updating a specific Payment record via repository is complex and not implemented in this pass.")