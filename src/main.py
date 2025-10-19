import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


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

    # Crear el directorio si no existe
    app_data.mkdir(parents=True, exist_ok=True)
    return app_data


def main():
    # Obtener el directorio de datos
    app_data = get_app_data_dir()
    db_path = app_data / "deudas.db"

    app = QApplication(sys.argv)
    window = MainWindow(str(db_path))
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
