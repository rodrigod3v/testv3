import cv2
import os
import time
import keyboard
from capture   import capturar
from detector  import detectar_movimento, confirmar_com_template
from attacker  import atacar_mob
from memory_reader import MemoryReader
from config import AUTO_POT_HP_PERCENT, TECLA_POT_HP, TECLA_START, TECLA_STOP, DEBUG_MODE, GAME_WINDOW

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
    print(f"--- Ragnarok Bot MVP ---")
    if not GAME_WINDOW:
        print("[!] Janela do Ragnarok NO encontrada. Verifique o ttulo no config.py")
        return
        
    print(f"Janela detectada em: {GAME_WINDOW['left']}, {GAME_WINDOW['top']}")
    print(f"Aguardando comando: [{TECLA_START.upper()}] para Iniciar | [{TECLA_STOP.upper()}] para Sair")
    
    templates = carregar_templates()
    mem = MemoryReader()

    # Bloqueia at que a tecla de incio seja pressionada
    keyboard.wait(TECLA_START)
    print("\n[!] Bot em EXECUO!")

    frame_ant = capturar()
    ultimo_ataque = 0
    ultimo_log_memoria = 0
    INTERVALO_FRAMES = 0.05  # ~20 FPS de anlise

    while not keyboard.is_pressed(TECLA_STOP):
        # 1. Monitoramento de Memria (Autopot)
        if mem.esta_conectado():
            hp_atual = mem.get_hp_percent()
            if hp_atual < AUTO_POT_HP_PERCENT:
                keyboard.press_and_release(TECLA_POT_HP)
            
            agora = time.time()
            if agora - ultimo_log_memoria > 2:
                x, y = mem.ler_posicao()
                ultimo_log_memoria = agora

        # 2. Viso Computacional (Ataque)
        frame_atual = capturar()
        mobs = detectar_movimento(frame_ant, frame_atual)

        if mobs:
            if templates:
                mobs = confirmar_com_template(frame_atual, mobs, templates)

            if mobs:
                # Debug Visual: Desenha nos mobs encontrados
                if DEBUG_MODE:
                    for (mx, my, mw, mh) in mobs:
                        cv2.rectangle(frame_atual, (mx-mw//2, my-mh//2), (mx+mw//2, my+mh//2), (0, 255, 0), 2)

                alvo = max(mobs, key=lambda m: m[2])
                cx, cy = alvo[0], alvo[1]

                agora = time.time()
                if agora - ultimo_ataque > 0.2:
                    atacar_mob(cx, cy)
                    ultimo_ataque = agora

        # Mostrar janela de Debug
        if DEBUG_MODE:
            cv2.imshow("Bot Vision - Debug", frame_atual)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frame_ant = frame_atual
        time.sleep(INTERVALO_FRAMES)

    cv2.destroyAllWindows()
    print("Bot finalizado com sucesso.")

if __name__ == "__main__":
    main()
