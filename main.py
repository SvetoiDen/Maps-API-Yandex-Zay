import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray
import sys
from io import BytesIO
from PIL import Image
import requests
from data.form.main_api import Ui_MainAPI

# 1 Задание - Готовый редактор

# XY_Line - вводим адрес
# scaleLine - вводим масштаб

class MainAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainAPI()
        self.ui.setupUi(self)

        # Ссылки на кеокодер и на карту яндекс.
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.map_api_server = "https://static-maps.yandex.ru/v1"

        self.ui.label.setText("Введите адрес")
        self.ui.label_2.setText("Введите масштаб")

        # ключ и масштаб карты
        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.ui.scaleLine.setText("0.005")

        self.ui.SubmitMain.clicked.connect(self.submitMap)

        self.setFixedSize(379, 400)
        self.show()


    def submitMap(self):
        try:
            if self.ui.scaleLine.text() == '' or self.ui.XY_Line.text() == '':
                self.msq = QMessageBox(self).information(self, 'Не введены данные', 'Вы не ввели нужные данные')
                return

            # параметры получения координат
            geocoder_params = {
                "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
                "geocode": self.ui.XY_Line.text(),
                "format": "json"
            }

            url = requests.get(self.geocoder_api_server, params=geocoder_params)

            if not url:
                self.msq = QMessageBox(self).information(self, 'Запрос не получен',
                                                         'Не смогли получить запрос. Повторите попытку')
                return

            # Преобразуем ответ в json-объект
            json_response = url.json()
            # Получаем первый топоним из ответа геокодера.
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Долгота и широта:
            toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

            # Собираем параметры для запроса к StaticMapsAPI:
            if self.ui.checkBox.isChecked():
                map_params = {
                    "ll": ",".join([toponym_longitude, toponym_lattitude]),
                    "spn": ",".join([self.ui.scaleLine.text(), self.ui.scaleLine.text()]),
                    "apikey": self.apikey,
                    "theme": 'dark'
                }
            else:
                map_params = {
                    "ll": ",".join([toponym_longitude, toponym_lattitude]),
                    "spn": ",".join([self.ui.scaleLine.text(), self.ui.scaleLine.text()]),
                    "apikey": self.apikey,
                    "theme": 'light'
                }

            urlMap = requests.get(self.map_api_server, params=map_params)

            imagePixmap = QPixmap(630, 630)
            self.setFixedSize(630, 630)
            imagePixmap.loadFromData(QByteArray(urlMap.content))
            self.ui.map.setPixmap(imagePixmap)
        except:
            self.msg = QMessageBox(self).warning(self, 'Произошла ошибка', 'Вы не корректно ввели данные. Повторите попытку')
            print(traceback.format_exc())
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apimain = MainAPI()
    sys.exit(app.exec())