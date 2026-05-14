#include <Mouse.h>

void setup() {
  Serial.begin(115200);
  Mouse.begin();
}

void loop() {
  // O pacote agora tem 4 bytes: [0xFF, Comando, Dado1, Dado2]
  if (Serial.available() >= 4) {
    if (Serial.read() == 0xFF) { // Verifica se  o incio de um comando
      byte cmd = Serial.read();
      byte d1 = Serial.read();
      byte d2 = Serial.read();
      
      if (cmd == 1) { // MOVER RELATIVO
        Mouse.move((signed char)d1, (signed char)d2);
      } 
      else if (cmd == 2) { // CLICAR
        if (d1 == 1) { // Esquerdo
          Mouse.press(MOUSE_LEFT);
          delay(120); // Tempo de clique garantido
          Mouse.release(MOUSE_LEFT);
        } else { // Direito
          Mouse.press(MOUSE_RIGHT);
          delay(120);
          Mouse.release(MOUSE_RIGHT);
        }
      }
    }
  }
}
