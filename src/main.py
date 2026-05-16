# src/main.py
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db import Database

# Import new architecture components
from application.container import ServiceContainer


def get_app_data_dir() -> Path:
    """
    Obtiene el directorio de datos de la aplicación según el sistema operativo
    """
    if os.environ.get("ENV") == "dev":
        return Path.cwd()
    if sys.platform == "darwin":
        app_data = (
            Path.home() / "Library" / "Application Support" / "Calculadora de Deudas"
        )
    elif sys.platform == "win32":
        app_data = Path(os.getenv("APPDATA")) / "Calculadora de Deudas"
    else:  # Linux y otros
        app_data = Path.home() / ".local" / "share" / "calculadora-deudas"

    app_data.mkdir(parents=True, exist_ok=True)
    return app_data


def main():
    app_data = get_app_data_dir()
    if os.environ.get("ENV") == "dev":
        print(f"Using development database path: {app_data / 'deudas.db'}")
        db_path = app_data / "deudas.db"
    else:
        db_path = app_data / ".deudas.db"

    # --- REFACTORING: Initialize Database and Dependency Container first ---
    print("1. Initializing Database Adapter...")
    db = Database(str(db_path))

    # 2. Build the core application container (wires up repositories -> services)
    container = ServiceContainer.build_default(db=db)

    # 3. Pass dependencies to the UI layer
    print("2. Initializing Main Window with Dependency Injection...")
    window = MainWindow(container)  # Pass the entire container or key services
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
