import cv2
import numpy as np
from config import GAME_WINDOW, MASCARAS_EXCLUSAO, AREA_MINIMA_MOB, THRESHOLD_DIFF

def criar_mascara():
    """Cria mscara que cobre o HUD do RO (reas estticas)."""
    h = GAME_WINDOW["height"]
    w = GAME_WINDOW["width"]
    mascara = np.ones((h, w), dtype=np.uint8) * 255

    for (x, y, larg, alt) in MASCARAS_EXCLUSAO:
        mascara[y:y+alt, x:x+larg] = 0

    return mascara

MASCARA_HUD = criar_mascara()

def detectar_movimento(frame_ant, frame_atual):
    """Retorna lista de (cx, cy, area) onde h movimento relevante."""
    gray1 = cv2.cvtColor(frame_ant,   cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    diff = cv2.bitwise_and(diff, diff, mask=MASCARA_HUD)

    _, mask = cv2.threshold(diff, THRESHOLD_DIFF, 255, cv2.THRESH_BINARY)

    # Dilata para unir partes do mesmo mob (sprite fragmentado)
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mobs = []
    for c in contornos:
        area = cv2.contourArea(c)
        if area >= AREA_MINIMA_MOB:
            x, y, w, h = cv2.boundingRect(c)
            # Centro da base do sprite (onde clicar no RO)
            cx = x + w // 2
            cy = y + h          # base do sprite = p do mob
            mobs.append((cx, cy, area))

    return mobs


def confirmar_com_template(frame, mobs, templates, threshold=0.72):
    """Confirma mobs usando template matching na ROI de movimento."""
    confirmados = []

    for (cx, cy, area) in mobs:
        # Recorta regio ao redor do mob
        margem = 50
        x1 = max(0, cx - margem)
        y1 = max(0, cy - margem * 2)
        x2 = min(frame.shape[1], cx + margem)
        y2 = min(frame.shape[0], cy + margem)
        roi = frame[y1:y2, x1:x2]

        if roi.size == 0:
            continue

        for nome, tmpl in templates.items():
            if tmpl.shape[0] > roi.shape[0] or tmpl.shape[1] > roi.shape[1]:
                continue
            res = cv2.matchTemplate(roi, tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val >= threshold:
                confirmados.append((cx, cy, area, nome, max_val))
                break

    return confirmados
