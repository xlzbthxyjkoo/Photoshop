from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import numpy as np
import cv2
import qimage2ndarray


form_class = uic.loadUiType("C:/photo/ui2.ui")[0]

class editWindow(QMainWindow, form_class) :

    global img
    global pixmap
    global editimg

    def __init__(self) :
        super(editWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_12.clicked.connect(self.home) #home 버튼 클릭 시
        self.pushButton_13.clicked.connect(self.open) #사진 불러오기 버튼 클릭 시
        self.pushButton_14.clicked.connect(self.original)
        self.pushButton.clicked.connect(self.cut)   
        self.pushButton_3.clicked.connect(self.updown)
        self.pushButton_4.clicked.connect(self.leftright)
        self.pushButton_2.clicked.connect(self.gray)
        self.pushButton_5.clicked.connect(self.rotation)

        self.horizontalSlider_2.valueChanged.connect(self.brightness)
        self.pushButton_6.clicked.connect(self.brightness)

        self.horizontalSlider.valueChanged.connect(self.blur)
        self.pushButton_7.clicked.connect(self.blur)

        self.pushButton_8.clicked.connect(self.mosaic)
        self.pushButton_9.clicked.connect(self.sharp)

        self.pushButton_10.clicked.connect(self.sketch) 
        self.pushButton_17.clicked.connect(self.cartoon)      
        self.pushButton_16.clicked.connect(self.parasite)
        self.pushButton_15.clicked.connect(self.blemish_rmv)
        self.pushButton_19.clicked.connect(self.blemish_rmv2)
        self.pushButton_18.clicked.connect(self.frame)

        #setCheckable: True 설정 시, 누른 상태와 그렇지 않은 상태를 구분
        #blur 안에 isChecked를 사용하기 위해 해줌
        self.pushButton_6.setCheckable(True)
        self.pushButton_7.setCheckable(True)
        
        self.pushButton_11.clicked.connect(self.save)
        self.label = QLabel(self)   
        self.show()

        
    def home(self):
        self.close()

    def open(self): #사진 불러오기
        #global fileopen
        #QFileDialog의 getOpenFileName을 사용해 사진 파일 형식이 모두 보여지도록 설정함
        fileopen = QFileDialog.getOpenFileName(self,"사진 선택", './',
                '모든 그림 파일(*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif)' )

        if fileopen[0]: #파일이 선택되면
            self.label.setGeometry(10,70,811,641) #원하는 사이즈로 조정
            self.pixmap = QPixmap(fileopen[0])
            self.img = cv2.imread(fileopen[0])
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB) #RGB로 변환
            self.editimg = self.img
            self.label.setPixmap(QPixmap(self.pixmap).scaled(QSize(811, 641), 
                    Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)) #label위에 사진을 보여줌


    def brightness(self):
        global add
        brightimg = self.editimg.copy()

        if self.pushButton_6.isChecked() == True:
            val = self.horizontalSlider_2.value()
            array = np.full(brightimg.shape, (val, val, val), dtype=np.uint8)

            add = cv2.add(brightimg,  array)
            self.display(add)

        elif self.pushButton_6.isChecked() == False:
            self.editimg = add

    def blur(self):   #블러링
        global blur
        blurimg = self.editimg.copy() 
        
        if self.pushButton_7.isChecked() == True:    #블러버튼(pushButton_7)이 클릭되면 상태가 True로 반환
            val = self.horizontalSlider.value()         #qtdesigner 슬라이더를 이용해 변경된 값 받아주기
            blur = cv2.GaussianBlur(blurimg , (val*2+1, val*2+1), 0)  #받아온 value 값만큼 가우시안 블러 처리
            self.display(blur) #화면에 편집한 이미지를 보여주는 함수

        elif self.pushButton_7.isChecked() == False: 
            self.editimg = blur  #블러처리 된 이미지 반환

    def sharp(self):
        sharpimg = self.editimg
        array = np.array([0, -1, 0, -1, 5, -1, 0, -1, 0])
        sharpimg = cv2.filter2D(sharpimg, -1, array)
        self.editimg = sharpimg
        self.display(self.editimg)


    def mosaic(self):
        mosaicimage = self.editimg.copy()

        x, y, w, h = cv2.selectROI('mosaicimage', 
                    cv2.cvtColor(mosaicimage, cv2.COLOR_RGB2BGR), False)

        if w and h:
            roi = mosaicimage[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w//15, h//15)) #1/rate비율로 축소
            #원래 크기로 확대
            roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)
            mosaicimage[y:y+h, x:x+w] = roi
            self.editimg = mosaicimage
            self.display(mosaicimage)
            

    def cut(self):
        cutimage = self.editimg
        x, y, w, h = cv2.selectROI('cutimage', cv2.cvtColor(cutimage, cv2.COLOR_RGB2BGR), False)
        if w and h:
            roi = cutimage[y:y+h, x:x+w]
            self.editimg = roi
            self.display(self.editimg)


    def updown(self): #상하반전
        updownimg = cv2.flip(self.editimg, 0) #0은 상하반전
        self.editimg = updownimg
        self.display(self.editimg)

    def leftright(self): #좌우반전
        leftrightimg = cv2.flip(self.editimg, 1) #1은 좌우반전
        self.editimg = leftrightimg
        self.display(self.editimg)


    def gray(self): #흑백
        src = self.editimg
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 
        dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) 
        self.editimg = dst
        self.display(self.editimg)
            

    def rotation(self): #사진을 회전시켜주는 함수
        rotateimg = self.editimg
        rotateimg =  cv2.rotate(rotateimg, cv2.ROTATE_90_CLOCKWISE)
        self.editimg = rotateimg
        self.display(self.editimg)


    def sketch(self):
        sketchimg = self.editimg
        gray = cv2.cvtColor(sketchimg, cv2.COLOR_BGR2GRAY) #변환한 RGB값을 GRAY값으로 변환해준다
        sketchimg = cv2.GaussianBlur(gray , (0, 0), 19) # 밝은 곳은 더 밝게 어두운 곳은 더 어둡게 해야 스케치스러운 느낌
        sketchimg = cv2.divide(gray, sketchimg, scale=255)
        sketchimg = cv2.cvtColor(sketchimg, cv2.COLOR_GRAY2RGB)
        self.editimg = sketchimg
        self.display(sketchimg)

    def cartoon(self):
        cartoonimg = self.editimg
        edge = 255 - cv2.Canny(cartoonimg, 80, 120)
        edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        cartoonimg = cv2.bitwise_and(cartoonimg, edge)
        self.editimg = cartoonimg
        self.display(self.editimg)



    def blemish_rmv(self):
        blemishimg = self.editimg.copy()

        x, y, w, h = cv2.selectROI('blemishimg', cv2.cvtColor(blemishimg, cv2.COLOR_RGB2BGR), False)
        
        if w and h:
            roi = blemishimg[y:y+h, x:x+w]
            roi = cv2.GaussianBlur(roi, (23,23), 0)
            blemishimg[y:y+h, x+w:x+w+w] = roi
            self.editimg = blemishimg
            self.display(blemishimg)

    def blemish_rmv2(self):
        blemishimg = self.editimg.copy()

        x, y, w, h = cv2.selectROI('blemishimg', cv2.cvtColor(blemishimg, cv2.COLOR_RGB2BGR), False)
        
        if w and h:
            roi = blemishimg[y:y+h, x:x+w]
            roi = cv2.medianBlur(roi, 5)
            blemishimg[y:y+h, x:x+w] = roi
            self.editimg = blemishimg
            self.display(self.editimg)
            


    def parasite(self):
        prsfilter = self.editimg.copy()

        x, y, w, h = cv2.selectROI('parasite', cv2.cvtColor(prsfilter, cv2.COLOR_RGB2BGR), False)

        if w and h:
            roi = prsfilter[y:y+h, x:x+w]
            roi = [0,0,0]
            prsfilter[y:y+h, x:x+w] = roi
            self.editimg = prsfilter
            self.display(self.editimg)

    def frame(self):
        frameimg = self.editimg.copy()

        frame = cv2.imread("C:/photo/frame.jpg")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        y, x = frameimg.shape[:2]

        frame = cv2.resize(frame, dsize=(x,y), interpolation=cv2.INTER_AREA)

        frame2gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(frame2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        y2, x2 = frame.shape[:2]
        roi = frameimg[0:y2, 0:x2]

        frameimg_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        frame_fg = cv2.bitwise_and(frame, frame, mask=mask)

        result = cv2.add(frameimg_bg, frame_fg)

        frameimg[0:y2, 0:x2] = result

        self.editimg = frameimg
        self.display(self.editimg)


    def original(self): #원본 이미지를 보여줌
        #편집 전 이미지를 copy해서 변수에  저장
        originalimg = self.img.copy() 
        #편집하던 이미지 editimg를 원본이미지로 바꿔줌
        self.editimg = originalimg
        self.display(self.editimg)


    def display(self, basicimg):
        imagedisplay = qimage2ndarray.array2qimage(basicimg, normalize=False)
        displaypixmap = QPixmap.fromImage(imagedisplay)     
        self.label.setPixmap(QPixmap(displaypixmap).scaled(QSize(811, 641), 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            

    def save(self): #사진 저장
        self.img = self.editimg #원본 이미지를 편집하던 이미지로 바꿔준다
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB) 
        #QFileDialog의 getSaveFileName을 사용해 사진을 사진 파일으로 저장해준다.
        self.savefile, _ = QFileDialog.getSaveFileName(self, '사진저장', '', 
            '모든 그림 파일(*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif)')
        cv2.imwrite(self.savefile, self.img)
          