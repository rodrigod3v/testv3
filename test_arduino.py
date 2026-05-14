import sys
import os
import time

# Adiciona o diretrio ro_bot ao path para importar os mdulos
sys.path.append(os.path.join(os.getcwd(), 'ro_bot'))

try:
    from arduino_comm import ArduinoMouse
    from config import ARDUINO_PORT, ARDUINO_BAUD
except ImportError as e:
    print(f"Erro ao importar mdulos: {e}")
    sys.exit(1)

def test():
    print("--- Teste de Hardware: Arduino Leonardo ---")
    print(f"Configurao atual: Porta={ARDUINO_PORT}, Baud={ARDUINO_BAUD}")
    
    mouse = ArduinoMouse(ARDUINO_PORT, ARDUINO_BAUD)
    
    if mouse.ser and mouse.ser.is_open:
        print("\n[OK] Conexo Serial aberta com sucesso!")
        print("Iniciando sequncia de teste em 3 segundos...")
        print("CUIDADO: O mouse ir se mover!")
        time.sleep(3)
        
        # Teste de movimento (Quadrado)
        print("-> Movendo para a Direita (+100px)")
        mouse.move(100, 0)
        time.sleep(0.5)
        
        print("-> Movendo para Baixo (+100px)")
        mouse.move(0, 100)
        time.sleep(0.5)
        
        print("-> Movendo para a Esquerda (-100px)")
        mouse.move(-100, 0)
        time.sleep(0.5)
        
        print("-> Movendo para Cima (-100px)")
        mouse.move(0, -100)
        time.sleep(1)
        
        # Teste de clique
        print("-> Testando Clique Direito...")
        mouse.click('right')
        
        print("\n[SUCESSO] Se o mouse se moveu e clicou, a integrao est funcional!")
        mouse.close()
    else:
        print("\n[ERRO] No foi possvel comunicar com o Arduino.")
        print(f"Verifique se:")
        print(f"1. O Arduino Leonardo est conectado na porta {ARDUINO_PORT}")
        print(f"2. O cdigo .ino foi carregado corretamente")
        print(f"3. Nenhuma outra aplicao (como o Monitor Serial da IDE Arduino) est usando a porta {ARDUINO_PORT}")

if __name__ == "__main__":
    test()
