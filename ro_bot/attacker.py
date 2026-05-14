import pyautogui
import time
import random
from config import GAME_WINDOW, COOLDOWN_ATAQUE, DELAY_VARIACAO

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0

def coord_absoluta(cx, cy):
    ax = GAME_WINDOW["left"] + cx
    ay = GAME_WINDOW["top"]  + cy
    return ax, ay

def atacar_mob(cx, cy):
    """Clique direito no mob para atacar (padro RO)."""
    ax, ay = coord_absoluta(cx, cy)

    # Movimento humano com leve variao
    pyautogui.moveTo(
        ax + random.randint(-3, 3),
        ay + random.randint(-3, 3),
        duration=random.uniform(0.04, 0.09)
    )
    pyautogui.click(button='right')

    delay = COOLDOWN_ATAQUE + random.uniform(0, DELAY_VARIACAO)
    time.sleep(delay)

def fazer_loot(cx, cy):
    """Alt+clique para pegar item do cho."""
    ax, ay = coord_absoluta(cx, cy)
    pyautogui.keyDown('alt')
    time.sleep(0.03)
    pyautogui.click(ax, ay)
    pyautogui.keyUp('alt')
    time.sleep(0.1)
