import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout

from .config import config_by_name, Config

class ClientApp(QMainWindow):

    def __init__(self, config: Config):
        super().__init__()

        self.setWindowTitle(config.TITLE)
        self.setFixedSize(QSize(config.WIDTH, config.HEIGHT))


def start_client_app(config_name: str) -> None:
    app = QApplication([])
    window = ClientApp(config_by_name[config_name])
    window.show()
    sys.exit(app.exec_())

