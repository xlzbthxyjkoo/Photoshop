import numpy as np
import cv2

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이

while(True):
    ret, frame = cap.read() # 사진 촬영
    frame = cv2.flip(frame, 1) # 좌우 대칭

    cv2.imshow('Press the c key', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('C:/photo/myphoto.jpg', frame) # 사진 저장
        break
  
cap.release()
cv2.destroyAllWindows()