import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db import Database


def get_app_data_dir() -> Path:
    """
    Obtiene el directorio de datos de la aplicación según el sistema operativo
    """
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
    db_path = app_data / ".deudas.db"

    # Inicializar aplicación
    app = QApplication(sys.argv)
    db = Database(str(db_path))
    window = MainWindow(db)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
