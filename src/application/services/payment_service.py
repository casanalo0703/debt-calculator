# src/application/services/payment_service.py
from typing import List, Optional
from ..repositories.payment_repository import PaymentRepository
from ..dtos.payment_dto import PaymentDTO
from domain.models.payment import Payment # Domain model reference
from domain.value_objects.money import Money
from src.application.events.event_bus import EventBus

class PaymentService:
    """Use Case Service for recording and querying payments."""

    def __init__(self, payment_repo: PaymentRepository, event_bus: EventBus):
        self.payment_repo = payment_repo
        self.event_bus = event_bus

    def add_payment(self, client_id: int, debt_id: int | None, amount: float, description: Optional[str], ticket_number: Optional[str]) -> PaymentDTO:
        """Use Case: Records a payment and emits an event."""
        if amount <= 0.0:
            raise ValueError("Payment amount must be positive.")

        # 1. Validation/Domain Check (Requires fetching debt first to check balance)
        # This is complex, so we assume the repository/domain handles checking if debt_id exists and has enough remaining funds.
        
        new_payment = Payment(
            client_id=client_id,
            debt_id=debt_id,
            amount=amount,
            description=description,
            ticket_number=ticket_number
        )

        # 2. Persistence
        try:
            saved_payment = self.payment_repo.save(new_payment)
        except Exception as e:
            raise RuntimeError(f"Failed to persist payment: {e}")

        # 3. Event Publishing
        self.event_bus.publish(PaymentAdded(payment_id=saved_payment.id!, debt_id=saved_payment.debt_id!, client_id=client_id, amount=amount))

        return PaymentDTO(
            client_id=saved_payment.client_id,
            debt_id=saved_payment.debt_id,
            amount=self._extract_money_amount(saved_payment), # Placeholder conversion
            date=saved_payment.date,
            description=saved_payment.description,
            ticket_number=saved_payment.ticket_number
        )

    def list_payments_by_client(self, client_id: int) -> List[PaymentDTO]:
        """Use Case: Retrieves payment history for a client."""
        try:
            # Note: This uses the simplified method signature from SQLitePaymentRepository adapter
            payments = self.payment_repo.find_all_for_client(client_id)
            dtos = []
            for p in payments:
                dto = PaymentDTO(
                    client_id=p.client_id,
                    debt_id=p.debt_id,
                    amount=self._extract_money_amount(p), # Placeholder conversion
                    date=p.date,
                    description=p.description,
                    ticket_number=p.ticket_number
                )
                dtos.append(dto)
            return dtos
        except Exception as e:
            print(f"Error listing payments for client {client_id}: {e}")
            return []

    def _extract_money_amount(self, payment: Payment) -> float:
        """Helper to extract amount consistently."""
        # In a real scenario, we'd map Money VO to DTO field
        return payment.amount.amount