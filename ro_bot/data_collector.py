import cv2
import os
import time
import keyboard
from capture import capturar
from detector import detectar_movimento

def iniciar_coleta():
    # Cria a pasta para o dataset se no existir
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
        print("[*] Pasta 'dataset' criada.")

    print("--- Coletor de Dados de Mobs ---")
    print("O bot vai salvar imagens automaticamente quando houver movimento.")
    print("Pressione 'C' para capturar manualmente ou 'Q' para parar.")

    frame_ant = capturar()
    count = 0
    ultima_captura = 0

    while not keyboard.is_pressed('q'):
        frame_atual = capturar()
        mobs = detectar_movimento(frame_ant, frame_atual)

        agora = time.time()
        # Salva automaticamente se houver movimento (com delay de 1s para no inundar o HD)
        if (mobs or keyboard.is_pressed('c')) and (agora - ultima_captura > 1.0):
            filename = f"dataset/mob_{int(agora)}.png"
            cv2.imwrite(filename, frame_atual)
            count += 1
            ultima_captura = agora
            print(f"[+] Imagem {count} salva: {filename}")

        frame_ant = frame_atual
        time.sleep(0.1)

    print(f"--- Coleta finalizada. Total de imagens: {count} ---")

if __name__ == "__main__":
    iniciar_coleta()
