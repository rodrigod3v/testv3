import cv2
import os
import time
import keyboard
from capture   import capturar
from detector  import detectar_movimento, confirmar_com_template
from attacker  import atacar_mob
from memory_reader import MemoryReader
from config import AUTO_POT_HP_PERCENT, TECLA_POT_HP

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
    mem = MemoryReader()

    frame_ant = capturar()
    ultimo_ataque = 0
    ultimo_log_memoria = 0
    INTERVALO_FRAMES = 0.05  # ~20 FPS de anlise

    while not keyboard.is_pressed('q'):
        # 1. Monitoramento de Memria (Autopot)
        if mem.esta_conectado():
            hp_atual = mem.get_hp_percent()
            if hp_atual < AUTO_POT_HP_PERCENT:
                keyboard.press_and_release(TECLA_POT_HP)
                # print(f"HP Crítico: {hp_atual:.1f}% - Usando Poção!")
            
            # Log de status a cada 2 segundos
            agora = time.time()
            if agora - ultimo_log_memoria > 2:
                x, y = mem.ler_posicao()
                # print(f"Status: HP {hp_atual:.1f}% | Posio: {x}, {y}")
                ultimo_log_memoria = agora

        # 2. Viso Computacional (Ataque)
        frame_atual = capturar()
        mobs = detectar_movimento(frame_ant, frame_atual)

        if mobs:
            if templates:
                mobs = confirmar_com_template(frame_atual, mobs, templates)

            if mobs:
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
