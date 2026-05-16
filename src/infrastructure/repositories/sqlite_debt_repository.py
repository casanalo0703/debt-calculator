# src/infrastructure/repositories/sqlite_debt_repository.py
from typing import List, Optional
from ..application.repositories.debt_repository import DebtRepository
from domain.models.debt import Debt # Assuming model exists
from database.db import Database # Using the existing DB class

class SQLiteDebtRepository(DebtRepository):
    """Implementation of DebtRepository using raw SQLite connections."""
    def __init__(self, db: Database):
        self._db = db

    def get_by_id(self, debt_id: int) -> Optional[Debt]:
        # Requires a way to fetch one specific debt by ID. This is missing from current db.py methods.
        # We will assume the DB layer gets updated later or we adapt this for now.
        print("Warning: get_by_id for Debt is not explicitly implemented in db.py.")
        return None

    def find_all_for_client(self, client_id: int) -> List[Debt]:
        # Uses existing db.get_all_debts_by_client() method
        return self._db.get_all_debts_by_client(client_id)

    def save(self, debt: Debt) -> Debt:
        """Persists or updates a Debt aggregate."""
        if not debt.id:
            # New debt (assuming creation happens via add_debt which is more specific)
            try:
                self._db.add_debt(debt)
                print("Note: Assuming successful save for new debt.") # Placeholder for actual ID return
                return debt
            except Exception as e:
                raise RuntimeError(f"DB Error saving debt: {e}")

        else:
            # Update logic (Complex, requires more DB support)
            raise NotImplementedError("Updating a specific Debt record via repository is complex and not implemented in this pass.")


    def get_remaining_debt_status(self, debt_id: int) -> Optional[float]:
        """Calculates remaining balance using the specialized DB method."""
        try:
            # Uses existing db.get_remaining_debt() method
            remaining = self._db.get_remaining_debt(debt_id)
            return remaining if remaining is not None else 0.0
        except Exception as e:
            print(f"Error getting debt status: {e}")
            return None