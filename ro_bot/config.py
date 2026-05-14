# Resoluo tpica do RO (ajuste para o seu cliente)
GAME_WINDOW = {"top": 0, "left": 0, "width": 800, "height": 600}

# Regies a IGNORAR (HUD do RO)
# Ajuste conforme sua resoluo
MASCARAS_EXCLUSAO = [
    (0, 0, 800, 70),      # Barra superior (HP/SP/EXP)
    (0, 530, 800, 70),    # Chat e hotkeys na base
    (0, 0, 150, 600),     # Minimap lateral esquerdo
]

# Configuraes de deteco
AREA_MINIMA_MOB = 300     # Pixels  filtra rudo de animao
THRESHOLD_DIFF = 20       # Sensibilidade ao movimento (0-255)
COOLDOWN_ATAQUE = 0.25    # Segundos entre ataques
DELAY_VARIACAO = 0.1      # Variao aleatria (anti-deteco)

# Teclas do jogo
TECLA_ATAQUE = None       # None = clique direito no mob
TECLA_LOOT   = 'z'        # Alt+click ou tecla de loot

# Configuraes do Arduino Leonardo (Hardware Mouse)
USE_ARDUINO = True        # Altere para False se quiser usar PyAutoGUI
ARDUINO_PORT = 'COM10'     # Ajuste para a sua porta (ex: COM3, COM4)
ARDUINO_BAUD = 115200

# Offsets de Memria (Endereos Hex)
PROCESS_NAME = "ragexe.exe"  # Nome do processo do RO (ajuste se necessrio)

OFFSETS = {
    "HP_ATUAL": 0x1684B48,
    "HP_MAX":   0x1684B4C,
    "SP_ATUAL": 0x1684B50,
    "PLAYER_X": 0x12D7964,
    "PLAYER_Y": 0x12D7968
}

# Configuraes de Autopot
AUTO_POT_HP_PERCENT = 70  # Usa poo se HP < 70%
TECLA_POT_HP = 'f3'

# Atalhos de Controle do Bot
TECLA_START = 'f1'       # Inicia o loop de ataque
TECLA_STOP  = 'f2'         # Para o bot e fecha o programa
