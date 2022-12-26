from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5 import uic
import sys
from edit import editWindow

form_class = uic.loadUiType("C:/photo/ui.ui")[0]

class MainWindow(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.showMenu) #pushButton이 클릭되면 showMenu 실행
        self.pushButton_2.clicked.connect(self.selfcamera) #pushButton_2가 클릭되면 selfcamera 실행

    def showMenu(self) :
        self.editWindow = editWindow()
        self.editWindow.show()

    def selfcamera(self) :
        self.Information() #카메라가 열리기 전 촬영 버튼을 안내해주는 팝업창을 보여주는 함수
        exec(open("C:/photo/camera.py", encoding="UTF-8").read())

    def Information(self): 
        QMessageBox.information(self, 'camera info', '촬영 버튼은 C키 입니다.')


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    main = MainWindow() 
    main.show()
    app.exec_()