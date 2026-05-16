# Refactoring Plan: Hexagonal Architecture Implementation

**Date:** May 15, 2026  
**Status:** Planning Phase  
**Target:** Improve code quality, testability, and maintainability  

---

## 📋 Table of Contents
1. [Current State Analysis](#current-state-analysis)
2. [Target Architecture](#target-architecture)
3. [Refactoring Phases](#refactoring-phases)
4. [Implementation Details](#implementation-details)
5. [Success Criteria](#success-criteria)

---

## Current State Analysis

### ⚠️ Critical Issues

| # | Problem | Severity | Impact |
|---|---------|----------|--------|
| 1 | Tight coupling: UI directly imports Database | 🔴 High | Cannot test widgets independently; hard to change persistence layer |
| 2 | Business logic scattered: UI + Database + Models | 🔴 High | Duplicate validations; logic hard to locate; inconsistent behavior |
| 3 | Inconsistent Database return types | 🟠 Medium | Some methods return tuples, others return Pydantic models; type confusion |
| 4 | ~5% test coverage (models only) | 🔴 High | No Database tests; no UI tests; no integration tests |
| 5 | Empty folders: `application/` and `domain/` | 🟡 Low | Initial architecture plan never completed |
| 6 | Duplicate methods in Database | 🟡 Low | `get_debts_by_client()` vs `get_all_debts_by_client()` |
| 7 | Hardcoded values scattered | 🟡 Low | Country code `+52` in UI; paths in main.py |

### Current Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                       UI Layer (PySide6)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ MainWindow + Widgets (add_debt, list_clients...)│  │
│  └──────────────────────────────────────────────────┘  │
│                  ⬇️ TIGHT COUPLING ⬇️                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │    Database (26 methods, mixed concerns)        │  │
│  │  - CRUD operations                             │  │
│  │  - Business logic (get_remaining_debt)         │  │
│  │  - Data transformation                         │  │
│  └──────────────────────────────────────────────────┘  │
│                  ⬇️                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │           SQLite Database                        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

Models (Pydantic)
├── Validation only
└── No business logic
```

### Problems with Current Design

1. **No Separation of Concerns**
   - Database handles CRUD, calculations, and transformations
   - UI handles presentation and validation
   - No dedicated application/domain layer

2. **Hard to Test**
   - Cannot test business logic without database
   - Cannot test UI without creating actual database
   - No dependency injection = everything tightly coupled

3. **Hard to Change**
   - Switching from SQLite to PostgreSQL requires updating all widgets
   - Adding new business rules requires modifying Database class
   - Database class is 500+ lines and growing

---

## Target Architecture

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────────────────────────────────────┐
│                     🎯 DOMAIN LAYER (Core)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Domain Models (Business Logic)                         │   │
│  │  • Client (aggregate root)                            │   │
│  │  • Debt (aggregate root)                              │   │
│  │  • Payment                                            │   │
│  │  • Value Objects (Money, PhoneNumber)                 │   │
│  │  • Domain Exceptions                                 │   │
│  │  • Business Rules & Constraints                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
               ⬆️                                              ⬇️
    ┌──────────────────────┐                 ┌──────────────────────┐
    │  🔌 PRIMARY PORTS     │                 │  🔌 SECONDARY PORTS  │
    │  (Inputs/Driving)    │                 │  (Outputs/Driven)    │
    │                      │                 │                      │
    │  • UI Events         │                 │  • Repository        │
    │  • User Interactions │                 │  • Event Bus         │
    │  • API Endpoints     │                 │  • Logger            │
    └──────────────────────┘                 └──────────────────────┘
               ⬆️                                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│           🛠️ APPLICATION LAYER (Orchestration)                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Application Services (Use Cases)                       │   │
│  │  • ClientService (CreateClient, UpdateClient, etc)    │   │
│  │  • DebtService (RecordDebt, PayDebt, etc)             │   │
│  │  • PaymentService (AddPayment, etc)                   │   │
│  │  • CommissionService (CalculateCommissions, etc)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ DTOs & Contracts                                       │   │
│  │  • ClientDTO, DebtDTO, PaymentDTO                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Event Bus (Domain Event Publishing)                    │   │
│  │  • ClientCreated, DebtRecorded, PaymentAdded          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
               ⬆️                                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│       📡 ADAPTER LAYER (Technical Implementation)              │
│                                                                 │
│  PRIMARY ADAPTERS (Inputs)                                     │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  UI Adapter (PySide6)                                 │   │
│  │  • Widgets → Services                                 │   │
│  │  • Subscribe to domain events                         │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  SECONDARY ADAPTERS (Outputs)                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Repository Adapter (SQLite Implementation)            │   │
│  │  • ClientRepository → Database                         │   │
│  │  • DebtRepository → Database                           │   │
│  │  • PaymentRepository → Database                        │   │
│  │  • Interfaces in application/, impl. in infrastructure/│   │
│  └────────────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Config Adapter                                        │   │
│  │  • Settings & Environment                             │   │
│  │  • Logging configuration                              │   │
│  │  • Dependency Injection Container                      │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
               ⬆️
        ┌──────────────┐
        │  SQLite DB   │
        └──────────────┘
```

### New Folder Structure

```
src/
├── main.py                              # Entry point
│
├── domain/                              # ⭐ CORE BUSINESS LOGIC (Independent)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── client.py                   # Aggregate root with business logic
│   │   ├── debt.py                     # Aggregate root with business logic
│   │   ├── payment.py
│   │   └── employee.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── money.py                    # Money with validation
│   │   ├── phone_number.py
│   │   └── date_range.py
│   └── exceptions/
│       ├── __init__.py
│       └── domain_exceptions.py        # InsufficientBalance, ClientNotFound, etc
│
├── application/                         # ⭐ USE CASES & ORCHESTRATION
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── client_service.py           # CreateClient, UpdateClient, etc
│   │   ├── debt_service.py             # RecordDebt, GetDebtStatus, etc
│   │   ├── payment_service.py          # AddPayment, GetPaymentHistory, etc
│   │   ├── commission_service.py       # CalculateCommissions, etc
│   │   └── employee_service.py         # ManageEmployees, etc
│   ├── repositories/                   # ⭐ ABSTRACT CONTRACTS (Ports)
│   │   ├── __init__.py
│   │   ├── client_repository.py        # Abstract ClientRepository
│   │   ├── debt_repository.py          # Abstract DebtRepository
│   │   ├── payment_repository.py       # Abstract PaymentRepository
│   │   └── employee_repository.py
│   ├── dtos/                           # Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── client_dto.py
│   │   ├── debt_dto.py
│   │   ├── payment_dto.py
│   │   └── responses.py                # Success/Error responses
│   ├── events/                         # Domain Events (Event Bus)
│   │   ├── __init__.py
│   │   ├── domain_events.py            # ClientCreated, DebtRecorded, etc
│   │   ├── event_bus.py                # Publish/Subscribe pattern
│   │   └── event_handlers.py           # Event listeners
│   └── container.py                    # 🔧 Dependency Injection Container
│
├── infrastructure/                      # ⭐ TECHNICAL ADAPTERS
│   ├── __init__.py
│   ├── repositories/                   # ⭐ CONCRETE IMPLEMENTATIONS (Adapters)
│   │   ├── __init__.py
│   │   ├── sqlite_client_repository.py # Implements ClientRepository
│   │   ├── sqlite_debt_repository.py   # Implements DebtRepository
│   │   ├── sqlite_payment_repository.py
│   │   └── sqlite_employee_repository.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── database.py                 # Raw SQLite operations (lower level)
│   │   └── migrations.py               # Schema management
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                 # Centralized configuration
│   │   └── logging.py
│   └── events/
│       ├── __init__.py
│       └── simple_event_bus.py         # Simple in-memory implementation
│
├── ui/                                  # 🎨 PRESENTATION LAYER (Adapters)
│   ├── __init__.py
│   ├── main_window.py                  # Refactored to use services
│   ├── dialogs/
│   │   ├── __init__.py
│   │   ├── client_dialog.py            # Refactored
│   │   ├── debt_dialog.py              # Refactored
│   │   └── payment_dialog.py           # Refactored
│   └── widgets/
│       ├── __init__.py
│       ├── client_list_widget.py       # Refactored
│       ├── debt_list_widget.py         # Refactored
│       └── ...
│
└── models/                              # 🌉 BRIDGE LAYER (Pydantic for validation)
    ├── __init__.py
    ├── client.py                       # Will be phased out
    ├── debt.py                         # Will be phased out
    └── ...                             # Temporary during transition
```

---

## Refactoring Phases

### Phase 1: Foundation & Repository Pattern (Week 1)

**Goal:** Create the infrastructure for dependency injection and abstract persistence

**Tasks:**

1. **Create Domain Exceptions**
   - `src/domain/exceptions/domain_exceptions.py`
   - Define: `InsufficientBalance`, `ClientNotFound`, `DebtNotFound`, etc.

2. **Create Repository Interfaces**
   - `src/application/repositories/client_repository.py`
   - `src/application/repositories/debt_repository.py`
   - `src/application/repositories/payment_repository.py`
   - Each defines abstract interface (Python ABC)

3. **Create SQLite Repository Implementations**
   - `src/infrastructure/repositories/sqlite_client_repository.py`
   - `src/infrastructure/repositories/sqlite_debt_repository.py`
   - `src/infrastructure/repositories/sqlite_payment_repository.py`
   - Implement interfaces using existing Database class

4. **Create Dependency Injection Container**
   - `src/application/container.py`
   - Registers: repositories, services, event bus, logger
   - Manages singleton instances

5. **Update main.py**
   - Initialize container instead of Database directly
   - Pass container to MainWindow

**Files Created:** ~15 new files  
**Files Modified:** `main.py`  
**Tests:** Unit tests for repositories  

---

### Phase 2: Application Services (Week 2)

**Goal:** Create use cases that orchestrate domain and repository layers

**Tasks:**

1. **Create Application Services**
   - `src/application/services/client_service.py`
     - `create_client(name, phone, email) → ClientDTO`
     - `update_client(id, name, phone, email) → ClientDTO`
     - `get_client(id) → ClientDTO`
     - `list_all_clients() → List[ClientDTO]`
     - `delete_client(id) → None`
   
   - `src/application/services/debt_service.py`
     - `record_debt(client_id, amount, due_date, description) → DebtDTO`
     - `get_debt_status(debt_id) → DebtStatusDTO`
     - `list_debts_by_client(client_id) → List[DebtDTO]`
     - `get_remaining_debt(debt_id) → Money`
   
   - `src/application/services/payment_service.py`
     - `add_payment(debt_id, amount) → PaymentDTO`
     - `list_payments_by_client(client_id) → List[PaymentDTO]`
     - `get_total_paid(debt_id) → Money`
   
   - `src/application/services/commission_service.py`
     - `calculate_commissions(start_date, end_date) → CommissionDTO`
     - `get_employee_commission(employee_id, start_date, end_date) → Money`

2. **Create DTOs (Data Transfer Objects)**
   - `src/application/dtos/client_dto.py`
   - `src/application/dtos/debt_dto.py`
   - `src/application/dtos/payment_dto.py`
   - DTOs use Pydantic for validation and serialization

3. **Create Event Bus Infrastructure**
   - `src/application/events/domain_events.py` - Event definitions
   - `src/application/events/event_bus.py` - Pub/Sub interface
   - `src/infrastructure/events/simple_event_bus.py` - In-memory implementation

4. **Move Business Logic from Database to Services**
   - Extract `get_remaining_debt()` logic → into service
   - Extract `calculate_commissions()` logic → into service
   - Move validation logic from widgets → into services

**Files Created:** ~12 new files  
**Files Modified:** Database class (remove business logic)  
**Tests:** Unit tests for services + mocked repositories  

---

### Phase 3: Domain Models Enhancement (Week 3)

**Goal:** Move business rules into domain models (where they belong)

**Tasks:**

1. **Create Value Objects**
   - `src/domain/value_objects/money.py`
     - Encapsulates amount + currency + validation
     - Methods: `add()`, `subtract()`, `is_positive()`
   
   - `src/domain/value_objects/phone_number.py`
     - Encapsulates phone + validation
   
   - `src/domain/value_objects/date_range.py`
     - For commission period queries

2. **Enhance Domain Models**
   - `src/domain/models/debt.py`
     - Method: `get_remaining_balance(payments) → Money`
     - Method: `is_overdue() → bool`
     - Method: `mark_as_paid()`
   
   - `src/domain/models/payment.py`
     - Method: `is_valid(debt) → bool`
   
   - `src/domain/models/employee.py`
     - Method: `calculate_commission(sales) → Money`
     - Method: `can_deactivate() → bool`

3. **Create Aggregate Roots**
   - Define `Client` as aggregate root (contains Debts, Payments)
   - Define validation rules at aggregate level
   - Encapsulate consistency rules

**Files Created:** ~8 new files  
**Files Modified:** Existing model files  
**Tests:** Domain model unit tests  

---

### Phase 4: UI Refactoring & Decoupling (Week 4)

**Goal:** Remove Database imports from UI; use services instead

**Tasks:**

1. **Refactor MainWindow**
   - Inject services from container
   - Listen to domain events (event bus)
   - Refresh tables when events fired
   - Remove `self.db` references

2. **Refactor UI Widgets**
   - `client_dialog.py` → use `client_service`
   - `debt_dialog.py` → use `debt_service`
   - `payment_dialog.py` → use `payment_service`
   - Remove Database imports
   - Add event listeners for auto-refresh

3. **Create Event Handlers**
   - `ClientCreated` event → refresh client table
   - `DebtRecorded` event → refresh debt table
   - `PaymentAdded` event → update totals

4. **Update List Widgets**
   - Use services to fetch data
   - Respond to domain events
   - Remove hardcoded queries

**Files Modified:** ~15 UI files  
**Tests:** UI component tests (mocked services)  

---

### Phase 5: Configuration & Logging (Week 5)

**Goal:** Centralize configuration and improve observability

**Tasks:**

1. **Create Configuration Module**
   - `src/infrastructure/config/settings.py`
     - Database paths (dev vs prod)
     - Environment-specific configs
     - Constants (country code, currency, etc)
   
   - `src/infrastructure/config/logging.py`
     - Centralized logging setup
     - Replace `print()` with proper logging

2. **Migrate Hardcoded Values**
   - Move `+52` country code → settings
   - Move DB paths → settings
   - Move app constants → settings

3. **Update main.py**
   - Load settings from environment
   - Initialize container with settings
   - Setup logging

**Files Created:** ~3 new files  
**Files Modified:** `main.py`, existing modules  

---

### Phase 6: Testing Infrastructure (Week 6)

**Goal:** Establish comprehensive testing strategy

**Tasks:**

1. **Create Test Structure**
   - `tests/unit/domain/` - Model tests
   - `tests/unit/application/` - Service tests (mocked repos)
   - `tests/integration/repositories/` - Database tests
   - `tests/fixtures/` - Test factories and builders

2. **Write Tests for New Layers**
   - Domain model business logic tests
   - Repository integration tests
   - Service use case tests
   - Event bus tests

3. **Create Test Utilities**
   - Factory functions for test objects
   - Mocked repository implementations
   - Test database setup/teardown

4. **Measure Coverage**
   - Target: 70%+ overall coverage
   - Focus: Domain + Application layers
   - CI/CD integration for coverage reports

**Files Created:** ~40 test files  
**Target Coverage:** From 5% → 70%+

---

## Implementation Details

### Key Design Principles

1. **Dependency Inversion**
   - UI depends on Application (services)
   - Application depends on abstractions (repository interfaces)
   - Infrastructure implements abstractions (SQLite repos)
   - ✅ NOT: UI → Database (direct dependency)

2. **Domain-Driven Design**
   - Business rules live in domain models
   - Use cases orchestrate in services
   - Technical details hidden in infrastructure
   - ✅ Domain models are independent of frameworks

3. **Event-Driven Architecture**
   - Domain publishes events (ClientCreated, DebtRecorded)
   - UI listens to events and updates
   - ✅ NO tight coupling between UI and services

4. **Single Responsibility**
   - Database: SQL + data mapping only
   - Service: Orchestration + validation only
   - Model: Business rules + state only
   - Repository: Persistence abstraction only

### Example: Client Creation Flow (After Refactoring)

```python
# UI Layer (PySide6 widget)
class ClientDialog(QDialog):
    def __init__(self, client_service: ClientService, event_bus: EventBus):
        self.client_service = client_service
        self.event_bus = event_bus
        
        # Listen to domain event
        self.event_bus.subscribe(ClientCreated, self._on_client_created)
    
    def accept(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        
        try:
            # Call service (NOT database directly)
            client = self.client_service.create_client(name, phone, email)
            QMessageBox.success("Client created!")
        except DomainException as e:
            QMessageBox.error(str(e))
    
    def _on_client_created(self, event: ClientCreated):
        # UI auto-updates when event fires
        self.parent().refresh_client_table()

# Application Layer (Use Case)
class ClientService:
    def __init__(self, client_repo: ClientRepository, event_bus: EventBus):
        self.repo = client_repo
        self.event_bus = event_bus
    
    def create_client(self, name: str, phone: str, email: str) -> ClientDTO:
        # Validate & create domain model
        client = Client(name=name, phone=phone, email=email)
        
        # Persist
        saved_client = self.repo.save(client)
        
        # Publish event (UI listens)
        self.event_bus.publish(ClientCreated(saved_client.id))
        
        return ClientDTO.from_domain(saved_client)

# Domain Layer (Business Logic)
class Client(AggregateRoot):
    def __init__(self, name: str, phone: PhoneNumber, email: EmailStr):
        if not name or len(name) < 2:
            raise InvalidClientName("Name too short")
        
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = datetime.now()
        self.debts = []

# Repository Adapter (Infrastructure)
class SQLiteClientRepository(ClientRepository):
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, client: Client) -> Client:
        # SQL operation
        id = self.db.cursor.execute(
            "INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)",
            (client.name, str(client.phone), client.email)
        )
        client.id = id
        return client
```

---

## Success Criteria

### Code Quality Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Test Coverage | 5% | 70%+ | 75% |
| Cyclomatic Complexity (avg method) | 4.2 | 2.1 | < 3 |
| Lines per method (avg) | 28 | 12 | < 15 |
| Coupling (fan-in/fan-out) | High | Low | < 2 |
| Classes with >1 responsibility | 8+ | 0 | 0 |

### Architectural Goals

- ✅ **Testability:** Can test domain logic without database
- ✅ **Flexibility:** Can switch database without changing UI
- ✅ **Maintainability:** Clear separation of concerns
- ✅ **Scalability:** Easy to add new features/services
- ✅ **Documentation:** Code structure explains itself

### Verification Steps

1. **No direct imports of Database in UI**
   ```bash
   grep -r "from database" src/ui/
   # Should return: 0 matches
   ```

2. **All UI imports use application layer**
   ```bash
   grep -r "from application" src/ui/
   # Should return: multiple matches (services, events)
   ```

3. **Domain models have no framework dependencies**
   - ✅ No PySide6 imports
   - ✅ No database imports
   - ✅ No infrastructure imports

4. **70%+ test coverage**
   ```bash
   pytest --cov=src tests/
   ```

5. **All services can be instantiated with mock repos**
   ```python
   repo = MockClientRepository()
   service = ClientService(repo, event_bus)
   # Should work without needing a real database
   ```

---

## Timeline

| Phase | Week | Deliverables | Tests | PRs |
|-------|------|--------------|-------|-----|
| **Foundation** | 1 | Repos + Container | Unit | 1 |
| **Services** | 2 | Services + DTOs + Events | Unit + Integration | 1 |
| **Domain** | 3 | Value Objects + Aggregates | Unit | 1 |
| **UI Refactor** | 4 | Decoupled Widgets | Component | 1 |
| **Config** | 5 | Settings + Logging | Unit | 1 |
| **Testing** | 6 | Test Suite (70%+) | Full | 1 |

**Total:** 6 weeks | **Target Completion:** June 26, 2026

---

## Rollback Strategy

If critical issues arise:

1. All work on `refactor/architecture` branch (not main)
2. Can revert individual phases
3. Keep `main` branch production-ready at all times
4. If Phase X breaks critical functionality:
   - Revert that phase's PR
   - Discuss and plan fixes
   - Re-apply with corrections

---

## Next Steps

When ready to begin implementation:

1. Create feature branch: `git checkout -b refactor/architecture`
2. Start Phase 1: Foundation
3. Create PR for peer review after Phase 1
4. Iterate on feedback
5. Proceed to Phase 2 after Phase 1 approval

---

**Questions?** This document will be updated as we progress through each phase.
