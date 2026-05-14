import cv2
import os
import time
import keyboard
from capture   import capturar
from detector  import detectar_movimento, confirmar_com_template
from attacker  import atacar_mob
from memory_reader import MemoryReader
from yolo_detector import YOLODetector
from config import AUTO_POT_HP_PERCENT, TECLA_POT_HP, TECLA_START, TECLA_STOP, DEBUG_MODE, GAME_WINDOW, YOLO_MODEL, YOLO_CONFIDENCE

# ... (templates function if still needed, but YOLO usually replaces it)

def main():
    print(f"--- Ragnarok Bot YOLO Edition ---")
    if not GAME_WINDOW:
        print("[!] Janela do Ragnarok NO encontrada.")
        return
        
    mem = MemoryReader()
    yolo = YOLODetector(YOLO_MODEL)

    print(f"[*] Aguardando [{TECLA_START.upper()}] para Iniciar...")
    keyboard.wait(TECLA_START)
    print("\n[!] Bot em EXECUO com YOLO!")

    ultimo_ataque = 0
    ultimo_log_memoria = 0
    INTERVALO_FRAMES = 0.01  # YOLO pode ser pesado, ajuste conforme seu PC

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

        # 2. Inteligncia Artificial (YOLO)
        frame_atual = capturar()
        mobs = yolo.detectar(frame_atual, conf_threshold=YOLO_CONFIDENCE)

        if mobs:
            # Debug Visual
            if DEBUG_MODE:
                yolo.desenhar_deteccoes(frame_atual, mobs)

            # Escolhe o mob com maior confiana (conf  o 3 item do tupla)
            alvo = max(mobs, key=lambda m: m[2])
            cx, cy = alvo[0], alvo[1]

            agora = time.time()
            if agora - ultimo_ataque > 0.3: # Delay maior para o YOLO
                atacar_mob(cx, cy)
                ultimo_ataque = agora

        # Mostrar janela de Debug
        if DEBUG_MODE:
            cv2.imshow("Bot Vision - YOLO Debug", frame_atual)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(INTERVALO_FRAMES)

    cv2.destroyAllWindows()
    print("Bot finalizado.")

if __name__ == "__main__":
    main()
