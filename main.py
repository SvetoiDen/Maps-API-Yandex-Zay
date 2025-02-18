from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
import sys


class MainAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apimain = MainAPI()
    sys.exit(app.exec())
