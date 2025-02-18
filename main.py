from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
import sys
from io import BytesIO
from PIL import Image
import requests
from data.form.main_api import Ui_MainAPI


class MainAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainAPI()
        self.ui.setupUi(self)

        self.ui.SubmitMain.clicked.connect(self.submitMap)

        self.setFixedSize(400, 300)
        self.show()

    def submitMap(self):
        if self.ui.scaleLine.text() == '' or self.ui.XY_Line.text() == '':
            self.msq = QMessageBox(self).information(self, 'Не введены данные', 'Вы не ввели нужные данные')
            return

        url = requests.get('')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    apimain = MainAPI()
    sys.exit(app.exec())
