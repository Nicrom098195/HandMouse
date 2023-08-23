import cv2
import mediapipe as mp
import pyautogui as pag
from math import sqrt
cap = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

sw = pag.size()[0]
sh = pag.size()[1]
mx,my,tid,mtid=0,0,0,0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        
        tt = (0, 0)
        for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cc=True
            if id == 4:
                tt = (cx, cy)
                cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
            if id == 8:
                if cx < 100:
                    x = 100
                elif cx > 500:
                    x = 500
                else:
                    x = cx
                if cy < 240:
                    y = 40
                elif cy > 470:
                    y = 470
                else:
                    y = cy
                x -= 100
                y -= 240
                x = 360 - x
                mx = round(sw * x / 360)
                my = round(sh * y / 230)
                pag.moveTo(mx, my)
                cv2.circle(img, (cx, cy), 6, (255, 0, 0), cv2.FILLED)
                #Click detection
                tid=sqrt((abs(cx-tt[0])**2)+(abs(cy-tt[1])**2))
                if tid < 12 and cc:
                    pag.click()
                    cc=False
                elif tid > 12:
                    cc=True
            if id==12:
                #Click detection
                mtid=sqrt((abs(cx-tt[0])**2)+(abs(cy-tt[1])**2))
                if mtid < 12:
                    pag.mouseDown()
                else:
                    pag.mouseUp()
                cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)
                
            #Output data
            print("CX:", cx, "CY:", cy, "|", mx, " - ", my, "| ITID:",round(tid*100)/100, "MTID:",round(mtid*100)/100, "\r", end="")

    #cv2.imshow("Image", img)
    #cv2.waitKey(1)
