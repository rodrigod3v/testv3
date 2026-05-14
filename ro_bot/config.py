import pygetwindow as gw

# Nome da Janela do RO (Ajuste se o seu servidor usar outro nome)
WINDOW_TITLE = "Ragnarok" 

def detectar_janela():
    """Busca a janela do jogo e retorna suas coordenadas e tamanho."""
    try:
        janelas = gw.getWindowsWithTitle(WINDOW_TITLE)
        if not janelas:
            return None
            
        win = janelas[0]
        # Log para voc conferir no terminal
        print(f"[*] Janela encontrada: '{win.title}' em X:{win.left} Y:{win.top}")
        
        return {
            "top": win.top + 32, # Ajuste para barra de ttulo
            "left": win.left + 8, 
            "width": 1024,
            "height": 768
        }
    except Exception as e:
        print(f"[!] Erro ao buscar janela: {e}")
        return None

GAME_WINDOW = detectar_janela()

# Regies a IGNORAR (HUD do RO para 1024x768)
MASCARAS_EXCLUSAO = [
    (0, 0, 1024, 90),       # Barra superior (HP/SP/EXP)
    (0, 680, 1024, 88),    # Chat e hotkeys na base
    (0, 0, 180, 768),      # Minimap lateral esquerdo
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
PROCESS_NAME = "Ragexe.exe"  # Nome exato do processo do RO

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

# Debug
DEBUG_MODE = True         # Mostra a janela com o que o bot v
