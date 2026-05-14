import mss
import numpy as np
import cv2
from config import GAME_WINDOW

sct = mss.mss()

def capturar():
    frame = sct.grab(GAME_WINDOW)
    img = np.array(frame)
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def capturar_cinza():
    return cv2.cvtColor(capturar(), cv2.COLOR_BGR2GRAY)
