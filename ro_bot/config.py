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
