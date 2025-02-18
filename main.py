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

            toponym = self.get_toponym_info(self.ui.XY_Line.text())
            toponym_coordinates = toponym["Point"]["pos"]
            toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")

            lower_corner = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
            upper_corner = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
            span = self.get_map_scale(lower_corner, upper_corner)

            # Собираем параметры для запроса к StaticMapsAPI:
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_latitude]),
                "spn": ",".join(map(str, span)),
                "l": "map",
                "pt": f"{toponym_longitude},{toponym_latitude},pm2dgl",
                "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
            }

            urlMap = requests.get(self.map_api_server, params=map_params)

            if not urlMap:
                self.msq = QMessageBox(self).information(self, 'Запрос не получен',
                                                         'Не смогли получить запрос. Повторите попытку')
                return

            imagePixmap = QPixmap(630, 630)
            self.setFixedSize(630, 630)
            imagePixmap.loadFromData(QByteArray(urlMap.content))
            self.ui.map.setPixmap(imagePixmap)
        except:
            self.msg = QMessageBox(self).warning(self, 'Произошла ошибка',
                                                 'Вы не корректно ввели данные. Повторите попытку')
            print(traceback.format_exc())
            return

    def get_map_scale(self, lower_corner, upper_corner):
        lower_longitude, lower_latitude = map(float, lower_corner)
        upper_longitude, upper_latitude = map(float, upper_corner)

        delta_longitude = abs(upper_longitude - lower_longitude)
        delta_latitude = abs(upper_latitude - lower_latitude)

        return delta_longitude, delta_latitude

    def get_toponym_info(self, toponym_to_find):
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": toponym_to_find,
            "format": "json"
        }

        response = requests.get(self.geocoder_api_server, params=geocoder_params)

        if not response:
            raise RuntimeError("Ошибка запроса для геокодера")

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apimain = MainAPI()
    sys.exit(app.exec())
