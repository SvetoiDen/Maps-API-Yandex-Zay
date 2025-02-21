import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage, QTransform
from PyQt6.QtCore import QByteArray, Qt
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
        self.img_size = [630, 630]
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
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join([self.ui.scaleLine.text(), self.ui.scaleLine.text()]),
                "apikey": self.apikey,
            }

            urlMap = requests.get(self.map_api_server, params=map_params)
            print(urlMap.status_code, urlMap.url)

            imagePixmap = QPixmap(630, 630)
            imagePixmap.loadFromData(QByteArray(urlMap.content))
            self.full_img = Image.open(BytesIO(urlMap.content))
            self.full_img_size = (630, 630)
            self.img_size = [50, 50]
            self.img_pos = [0, 0]
            self.ui.map.setFocus()
            self.ui.map.setPixmap(imagePixmap)
        except Exception:
            self.msg = QMessageBox(self).warning(self, 'Произошла ошибка', 'Вы не корректно ввели данные. Повторите попытку')
            print(traceback.format_exc())
            return

    def draw_map(self):
        img = self.full_img.crop((*self.img_pos, self.img_pos[0] + self.img_size[0], self.img_pos[1] + self.img_size[1])).resize((630, 630))
        img = img.convert("RGB")

        imagePixmap = QPixmap(QImage(img.tobytes("raw", "RGB"), img.size[0], img.size[1], img.size[0]*3, QImage.Format.Format_RGB888))
        self.ui.map.setPixmap(imagePixmap)

    def keyPressEvent(self, event):
        self.move_delta = self.img_size[0] // 10
        if event.key() == Qt.Key.Key_Up:
            self.img_pos[1] -= self.move_delta
            self.img_pos[1] = max(self.img_pos[1], 0)
            self.draw_map()

        elif event.key() == Qt.Key.Key_Down:
            self.img_pos[1] += self.move_delta
            self.img_pos[1] = min(self.img_pos[1], self.full_img_size[1] - self.img_size[1])
            self.draw_map()

        elif event.key() == Qt.Key.Key_Left:
            self.img_pos[0] -= self.move_delta
            self.img_pos[0] = max(self.img_pos[0], 0)
            self.draw_map()

        elif event.key() == Qt.Key.Key_Right:
            self.img_pos[0] += self.move_delta
            self.img_pos[0] = min(self.img_pos[0], self.full_img_size[0] - self.img_size[0])
            self.draw_map()

        elif event.key() == Qt.Key.Key_PageUp and self.img_size[1] < self.full_img_size[1]:
            self.img_size[0] += 10
            self.img_size[1] += 10
            self.img_pos[0] -= 5
            self.img_pos[1] -= 5
            self.img_pos[1] = max(self.img_pos[1], 0)
            self.img_pos[0] = max(self.img_pos[0], 0)
            self.draw_map()

        elif event.key() == Qt.Key.Key_PageDown and self.img_size[1] > 10:
            self.img_size[0] -= 10
            self.img_size[1] -= 10
            self.img_pos[0] += 5
            self.img_pos[1] += 5
            self.img_pos[1] = max(self.img_pos[1], 0)
            self.img_pos[0] = max(self.img_pos[0], 0)
            self.img_pos[0] = min(self.img_pos[0], self.full_img_size[0] - self.img_size[0])
            self.img_pos[1] = min(self.img_pos[1], self.full_img_size[1] - self.img_size[1])
            self.draw_map()

        print("b")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apimain = MainAPI()
    sys.exit(app.exec())
