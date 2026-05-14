import cv2
import os
import time
import keyboard
from capture   import capturar
from detector  import detectar_movimento, confirmar_com_template
from attacker  import atacar_mob

# Carrega sprites dos mobs da pasta /sprites
def carregar_templates(pasta="sprites"):
    templates = {}
    if not os.path.exists(pasta):
        return templates
    for nome in os.listdir(pasta):
        if nome.endswith(".png"):
            img = cv2.imread(os.path.join(pasta, nome))
            if img is not None:
                templates[nome] = img
    return templates

def main():
    print("Bot iniciado  pressione Q para parar")
    templates = carregar_templates()

    frame_ant = capturar()
    ultimo_ataque = 0
    INTERVALO_FRAMES = 0.05  # ~20 FPS de anlise

    while not keyboard.is_pressed('q'):
        frame_atual = capturar()

        mobs = detectar_movimento(frame_ant, frame_atual)

        if mobs:
            # Confirma com template se tiver sprites carregados
            if templates:
                mobs = confirmar_com_template(frame_atual, mobs, templates)

            if mobs:
                # Ataca o mob com maior rea (mais prximo/visvel)
                alvo = max(mobs, key=lambda m: m[2])
                cx, cy = alvo[0], alvo[1]

                agora = time.time()
                if agora - ultimo_ataque > 0.2:
                    atacar_mob(cx, cy)
                    ultimo_ataque = agora

        frame_ant = frame_atual
        time.sleep(INTERVALO_FRAMES)

    print("Bot encerrado.")

if __name__ == "__main__":
    main()
