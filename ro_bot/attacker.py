import pyautogui
import time
import random
from config import GAME_WINDOW, COOLDOWN_ATAQUE, DELAY_VARIACAO, USE_ARDUINO, ARDUINO_PORT, ARDUINO_BAUD
from arduino_comm import ArduinoMouse

# Inicializa o hardware se configurado
hardware_mouse = None
if USE_ARDUINO:
    hardware_mouse = ArduinoMouse(ARDUINO_PORT, ARDUINO_BAUD)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0

def coord_absoluta(cx, cy):
    ax = GAME_WINDOW["left"] + cx
    ay = GAME_WINDOW["top"]  + cy
    return ax, ay

def mover_mouse(ax, ay):
    """Move o mouse com trava de segurana (clamping) dentro da janela."""
    margem = 15 # Margem interna para evitar bordas
    
    min_x = GAME_WINDOW["left"] + margem
    max_x = GAME_WINDOW["left"] + GAME_WINDOW["width"] - margem
    min_y = GAME_WINDOW["top"] + margem
    max_y = GAME_WINDOW["top"] + GAME_WINDOW["height"] - margem

    # Fora as coordenadas a ficarem dentro do 'raio de execuo'
    ax_travado = max(min_x, min(max_x, ax))
    ay_travado = max(min_y, min(max_y, ay))

    if USE_ARDUINO and hardware_mouse:
        cur_x, cur_y = pyautogui.position()
        dx = ax_travado - cur_x
        dy = ay_travado - cur_y
        hardware_mouse.move(dx, dy)
    else:
        pyautogui.moveTo(ax_travado, ay_travado, duration=random.uniform(0.04, 0.09))

def atacar_mob(cx, cy):
    """Clique direito no mob para atacar (padro RO)."""
    ax, ay = coord_absoluta(cx, cy)
    ax += random.randint(-3, 3)
    ay += random.randint(-3, 3)

    mover_mouse(ax, ay)
    time.sleep(0.05) # Pequeno delay para o jogo registrar o foco
    
    if USE_ARDUINO and hardware_mouse:
        hardware_mouse.click(button='right')
    else:
        pyautogui.click(button='right')

    delay = COOLDOWN_ATAQUE + random.uniform(0, DELAY_VARIACAO)
    time.sleep(delay)

def fazer_loot(cx, cy):
    """Alt+clique para pegar item do cho."""
    ax, ay = coord_absoluta(cx, cy)
    
    mover_mouse(ax, ay)
    time.sleep(0.05)

    if USE_ARDUINO and hardware_mouse:
        pyautogui.keyDown('alt')
        time.sleep(0.03)
        hardware_mouse.click(button='left')
        pyautogui.keyUp('alt')
    else:
        pyautogui.keyDown('alt')
        time.sleep(0.03)
        pyautogui.click(ax, ay)
        pyautogui.keyUp('alt')
    
    time.sleep(0.1)
