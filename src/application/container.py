# src/application/container.py
from typing import Type, Dict, Any


class ServiceContainer:
    """
    Dependency Injection Container for managing application services, repositories, and dependencies.
    This implements the Dependency Inversion Principle (DIP).
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._repositories: Dict[str, Any] = {}
        # Initialize Event Bus globally or pass it in during setup if possible.
        from src.application.events.event_bus import (
            event_bus,
        )  # Use the global instance

        self.event_bus = event_bus

    def register_repository(self, name: str, repository: Any) -> None:
        """Registers a concrete repository implementation."""
        print(f"Container registered Repository: {name}")
        self._repositories[name] = repository

    def get_repository(self, name: str) -> Any:
        """Retrieves a configured repository instance."""
        if name not in self._repositories:
            raise ValueError(f"Repository '{name}' is not registered.")
        return self._repositories[name]

    # --- Service Registration Methods (Simplified for this scope) ---
    def register_client_service(self, client_repo):
        """Registers ClientService using the provided repository."""
        from .services.client_service import ClientService

        self._services["client"] = ClientService(
            client_repo=client_repo,
            # event_bus=self.event_bus # Placeholder for full setup
        )

    def get_client_service(self) -> "ClientService":
        """Retrieves the client service."""
        if "client" not in self._services:
            raise ValueError(
                "ClientService has not been initialized. Call register_client_service first."
            )
        return self._services["client"]

    # Placeholder for other services (Debt, Payment, etc.)

    # --- Full Registration Pipeline (Recommended Initialization Block) ---
    @classmethod
    def build_default(cls, db: "Database") -> "ServiceContainer":
        """Builds and wires up the container with default implementations."""
        container = cls()

        # 1. Register Repositories (Adapters)
        client_repo = SQLiteClientRepository(db)
        debt_repo = SQLiteDebtRepository(db)
        payment_repo = SQLitePaymentRepository(db)
        employee_repo = SQLiteEmployeeRepository(db)
        provider_repo = SQLiteProviderRepository(db)
        container.register_repository("client", client_repo)
        container.register_repository("debt", debt_repo)
        container.register_repository("payment", payment_repo)
        container.register_repository("employee", employee_repo)
        container.register_repository("provider", provider_repo)

        # 2. Register Services (Use Cases)
        container.register_client_service(client_repo)

        from .services import (
            debt_service,
            payment_service,
            commission_service,
            employee_service,
        )  # Import all services

        container._services["debt"] = debt_service.DebtService(
            debt_repo, container.event_bus
        )
        container._services["payment"] = payment_service.PaymentService(
            payment_repo, container.event_bus
        )
        container._services["commission"] = commission_service.CommissionService(
            employee_repo, container.event_bus
        )
        container._services["employee"] = employee_service.EmployeeService(
            employee_repo, container.event_bus
        )
        return container
