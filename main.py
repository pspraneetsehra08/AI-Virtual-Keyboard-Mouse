import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import autopy
import pyautogui
#from pynput import keyboard
#from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/","_"],
        ["0","1","2","3","4", "5","6","7","8","9","-"]]

finalText = ""

#keyboard = Controller()

def drawALL(img,buttonList):
    imgNew=np.zeros_like(img,np.uint8)
    for button in buttonList:
        x,y=button.pos
        w, h = button.size
        cv2.rectangle(imgNew, button.pos, (x + w, y + h), (50, 50, 50), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    out=img.copy()
    alpha = 0.5
    mask=imgNew.astype(bool)
    #print(mask.shape)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# 44.03

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 30:
                    if button.text=="-":
                        finalText,result=finalText[:-1],finalText[-1]
                        pyautogui.press('backspace')
                        #autopy.key.tap(autopy.key.Code.BACKSPACE, [autopy.key.Modifier.META])
                    elif button.text=="_":
                        finalText+=" "
                        pyautogui.press('space')
                    else:
                        #autopy.key.tap(button.text, [autopy.key.Modifier.META])
                        pyautogui.press(button.text)
                        finalText += button.text
                    #keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    sleep(0.25)
    cv2.rectangle(img, (50, 450), (1150, 550), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, finalText, (60, 525),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)