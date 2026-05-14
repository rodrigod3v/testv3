import ctypes
import pyautogui
import time
import random
from config import GAME_WINDOW, COOLDOWN_ATAQUE, DELAY_VARIACAO, USE_ARDUINO, ARDUINO_PORT, ARDUINO_BAUD
from arduino_comm import ArduinoMouse

def get_real_mouse_pos():
    """Pega a posio real do mouse ignorando o escalonamento do Windows."""
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

# Inicializa o hardware se configurado
hardware_mouse = None
if USE_ARDUINO and ARDUINO_PORT:
    hardware_mouse = ArduinoMouse(ARDUINO_PORT, ARDUINO_BAUD)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0

def coord_absoluta(cx, cy):
    ax = GAME_WINDOW["left"] + cx
    ay = GAME_WINDOW["top"]  + cy
    return ax, ay

def mover_mouse(ax, ay):
    """Move o mouse com trava de segurana (clamping) e preciso absoluta."""
    margem = 15
    
    # Se a janela no foi detectada, no move
    if not GAME_WINDOW:
        return

    min_x = GAME_WINDOW["left"] + margem
    max_x = GAME_WINDOW["left"] + GAME_WINDOW["width"] - margem
    min_y = GAME_WINDOW["top"] + margem
    max_y = GAME_WINDOW["top"] + GAME_WINDOW["height"] - margem

    ax_travado = max(min_x, min(max_x, ax))
    ay_travado = max(min_y, min(max_y, ay))

    if USE_ARDUINO and hardware_mouse:
        # Usa ctypes para pegar a posio real do cursor
        cur_x, cur_y = get_real_mouse_pos()
        dx = ax_travado - cur_x
        dy = ay_travado - cur_y
        hardware_mouse.move(dx, dy)
    else:
        pyautogui.moveTo(ax_travado, ay_travado, duration=random.uniform(0.04, 0.09))

def atacar_mob(cx, cy):
    """Apenas persegue o mob (Cliques desativados)."""
    ax, ay = coord_absoluta(cx, cy)
    
    # Adiciona uma leve variao para no ficar no centro exato sempre
    ax += random.randint(-3, 3)
    ay += random.randint(-3, 3)

    mover_mouse(ax, ay)
    # time.sleep(0.05) 
    
    # if USE_ARDUINO and hardware_mouse:
    #     hardware_mouse.click(button='right')
    # else:
    #     pyautogui.click(button='right')

def fazer_loot(cx, cy):
    time.sleep(0.1)
