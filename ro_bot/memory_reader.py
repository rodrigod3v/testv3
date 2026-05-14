from pymem import Pymem
from config import PROCESS_NAME, OFFSETS

class MemoryReader:
    def __init__(self):
        self.pm = None
        try:
            self.pm = Pymem(PROCESS_NAME)
            self.base_address = self.pm.process_base.lpBaseOfDll
            print(f"Conectado ao processo: {PROCESS_NAME}")
        except Exception as e:
            print(f"Aguardando processo {PROCESS_NAME}... (Certifique-se de que o jogo est aberto)")

    def esta_conectado(self):
        return self.pm is not None

    def ler_int(self, endereco):
        try:
            return self.pm.read_int(endereco)
        except:
            return 0

    def ler_hp(self):
        if not self.pm: return 0, 0
        hp = self.ler_int(OFFSETS["HP_ATUAL"])
        max_hp = self.ler_int(OFFSETS["HP_MAX"])
        return hp, max_hp

    def ler_sp(self):
        if not self.pm: return 0
        return self.ler_int(OFFSETS["SP_ATUAL"])

    def ler_posicao(self):
        if not self.pm: return 0, 0
        x = self.ler_int(OFFSETS["PLAYER_X"])
        y = self.ler_int(OFFSETS["PLAYER_Y"])
        return x, y

    def get_hp_percent(self):
        hp, max_hp = self.ler_hp()
        if max_hp <= 0: return 100
        return (hp / max_hp) * 100
