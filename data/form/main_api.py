# Form implementation generated from reading ui file 'data/ui/main_api.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainAPI(object):
    def setupUi(self, MainAPI):
        MainAPI.setObjectName("MainAPI")
        MainAPI.resize(379, 508)
        self.centralwidget = QtWidgets.QWidget(parent=MainAPI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(9, 10, -1, 10)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 9, -1, 16)
        self.gridLayout.setHorizontalSpacing(19)
        self.gridLayout.setVerticalSpacing(16)
        self.gridLayout.setObjectName("gridLayout")
        self.scaleLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.scaleLine.setObjectName("scaleLine")
        self.gridLayout.addWidget(self.scaleLine, 1, 1, 1, 1)
        self.XY_Line = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.XY_Line.setObjectName("XY_Line")
        self.gridLayout.addWidget(self.XY_Line, 1, 0, 1, 1)
        self.SubmitMain = QtWidgets.QPushButton(parent=self.centralwidget)
        self.SubmitMain.setObjectName("SubmitMain")
        self.gridLayout.addWidget(self.SubmitMain, 2, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignJustify)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.map = QtWidgets.QLabel(parent=self.centralwidget)
        self.map.setText("")
        self.map.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.map.setObjectName("map")
        self.verticalLayout.addWidget(self.map)
        self.verticalLayout.setStretch(1, 2)
        MainAPI.setCentralWidget(self.centralwidget)
        self.StatusApp = QtWidgets.QStatusBar(parent=MainAPI)
        self.StatusApp.setObjectName("StatusApp")
        MainAPI.setStatusBar(self.StatusApp)

        self.retranslateUi(MainAPI)
        QtCore.QMetaObject.connectSlotsByName(MainAPI)

    def retranslateUi(self, MainAPI):
        _translate = QtCore.QCoreApplication.translate
        MainAPI.setWindowTitle(_translate("MainAPI", "Редактор Карты"))
        self.SubmitMain.setText(_translate("MainAPI", "Создать карту"))
        self.label.setText(_translate("MainAPI", "TextLabel"))
        self.label_2.setText(_translate("MainAPI", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainAPI = QtWidgets.QMainWindow()
    ui = Ui_MainAPI()
    ui.setupUi(MainAPI)
    MainAPI.show()
    sys.exit(app.exec())
