import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(application_path, "deudas.db")

    app = QApplication(sys.argv)
    window = MainWindow(db_path)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
