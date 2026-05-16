# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Stack & Build System
*   **Language/Framework:** Python 3.11, PySide6 for GUI.
*   **Dependencies:** Managed via `requirements.txt` (PySide6, pydantic, etc.).
*   **Build Tooling:** Uses `Makefile` with `pyinstaller` for packaging (macOS: `release-mac`, Windows: `release-windows`).

## Core Architecture & Flow
The application follows a Model-View-Controller pattern structure:
1.  **Model (`src/models/`):** Defines data structures using Pydantic models (`Client`, `Debt`, `Payment`, etc.). These are the single source of truth for data contracts.
2.  **Database Layer (`src/database/db.py`):** Handles all SQLite interactions. It abstracts raw SQL, providing methods like `add_client()`, `get_all_debts()`, etc. **Crucially, it manages database schema creation.**
3.  **View/Controller (`src/ui/main_window.py`):** The main GUI orchestrator. It calls the DB layer and updates widgets based on results.

## Critical Project Conventions & Gotchas (Non-Obvious)
*   **Database Naming:** The database file name changes based on environment: `deudas.db` in development (`ENV=dev`), but `.deudas.db` in production/release builds, as seen in `src/main.py`.
*   **Client ID Retrieval:** When adding a client, the returned ID from `db.add_client()` must be captured and used immediately for subsequent operations (e.g., creating debts).
*   **Date Handling:** Dates are stored in SQLite using ISO format strings (`YYYY-MM-DD HH:MM:SS`). Python's `datetime` objects must be explicitly converted to/from string formats when interacting with the DB layer, especially when reading/writing dates (e.g., `client.created_at.isoformat()`).
*   **Employee Status:** Employee deactivation is *soft delete*: setting `is_active = 0` and recording a `layoff_at` timestamp in `src/models/employee.py`, rather than deleting the record entirely.

## Code Style & Conventions
*   **Data Validation:** All data models must use Pydantic for validation (`pydantic.BaseModel`). Custom types like `PhoneNumber` from `pydantic-extra-types` are used and should be respected.
*   **Error Handling:** Database operations *must* wrap SQLite calls in `try...except sqlite3.Error` blocks, ensuring a `connection.rollback()` on failure to maintain transactional integrity.

## Build/Run Commands (Makefile)
*   **Development Run:** Use `make run-dev` which sets `ENV=dev` before running `python src/main.py`.
*   **macOS Release:** The full build process is sequential: `make release-mac` $\rightarrow$ `build` $\rightarrow$ `sign`.
*   **Windows Release:** Uses PowerShell for compression (`Compress-Archive`) or falls back to 7z if available.