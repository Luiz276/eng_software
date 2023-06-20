from jogador import Jogador
from baralho import Baralho

class Mesa:
    def __init__(self):
        self.local_player = Jogador()
        self.remote_player = Jogador()

        # self.local_player.initialize(1, "local_player", "local_player")
        # self.remote_player.initialize(2, "remote_player", "remote_player")

        self.trincas_locais = []
        self.trincas_remotas = []

        self.match_status = 1
    
    def start_match(self, players, local_player_id):
        self.baralho = Baralho()
        self.local_player.reset()
        self.remote_player.reset()
        self.local_player.initialize(1, players[0][1], players[0][0], self.baralho)
        self.remote_player.initialize(2, players[1][1], players[1][0], self.baralho)
        if players[0][2] == "1":
            self.local_player.toggle_turn()
            self.match_status = 2  #    waiting piece or origin selection (first action)
        else:
            self.remote_player.toggle_turn()
            self.match_status = 3  #    waiting remote action
        print("HERE!")
    
    def getStatus(self):
        return self.match_status