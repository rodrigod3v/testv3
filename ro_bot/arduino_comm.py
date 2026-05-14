import serial
import time
import struct

class ArduinoMouse:
    def __init__(self, port, baud=115200):
        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            time.sleep(2) # Aguarda inicializao do Arduino
            print(f"Conectado ao Arduino na porta {port}")
        except Exception as e:
            print(f"Erro ao conectar ao Arduino: {e}")
            self.ser = None

    def move(self, dx, dy):
        if not self.ser: return
        
        # O Arduino Mouse.move aceita signed char (-128 a 127)
        # Se dx ou dy for maior, precisamos quebrar em pequenos passos
        while dx != 0 or dy != 0:
            step_x = max(-127, min(127, dx))
            step_y = max(-127, min(127, dy))
            
            # Pacote: [0xFF, Comando 1, dx, dy]
            # Usamos 'b' para signed char (1 byte)
            packet = struct.pack('BBbb', 0xFF, 1, int(step_x), int(step_y))
            self.ser.write(packet)
            
            dx -= step_x
            dy -= step_y
            # O Arduino Leonardo processa rpido, mas um micro-delay ajuda na estabilidade
            time.sleep(0.001)

    def click(self, button='left'):
        if not self.ser: return
        # Comando 2: Clicar. Dado1: 1=Esquerdo, 2=Direito. Dado2: 0 (no usado)
        btn_code = 1 if button == 'left' else 2
        packet = struct.pack('BBbb', 0xFF, 2, btn_code, 0)
        self.ser.write(packet)

    def close(self):
        if self.ser:
            self.ser.close()
