import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.database import create_tables

if __name__ == "__main__":
    # Garante que as tabelas do banco de dados sejam criadas (ou verificadas)
    create_tables()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())