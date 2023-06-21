from jogador import Jogador
from baralho import Baralho
from descarte import Descarte
from trinca import Trinca

class Mesa:
    def __init__(self):
        self.local_player = Jogador()
        self.remote_player = Jogador()

        # self.local_player.initialize(1, "local_player", "local_player")
        # self.remote_player.initialize(2, "remote_player", "remote_player")

        self.trincas = []

        self.match_status = 1
    
    def start_match(self, players, local_player_id):
        self.baralho = Baralho()
        self.descarte = Descarte()
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

    def receive_move(self,a_move):
        if self.baralho == None:
            self.baralho = Baralho()
            self.baralho.set_cards(a_move["baralho"])
        else:
            if a_move["comprou_baralho"]:
                self.comprou_baralho(self.remote_player, True)
            else:
                self.comprou_baralho(self.remote_player, False)

            for trinca in a_move["trincas_baixadas"]:
                self.baixar_trinca(self.remote_player, trinca)
            self.descartar_carta(a_move["carta_descarte"])
        self.toggle_turn()

    def baixar_trinca(self, player: Jogador, trinca:list()):
        if self.valido(trinca):
            nova_trinca = Trinca(player, trinca)
            for card in trinca:
                player.remove_card(card)
            player.add_trinca(nova_trinca)
            self.trincas.append(nova_trinca)
            if self.checa_fim_jogo():
                self.match_status = 4

    def descartar_carta(self, player:Jogador, card):
        player.remove_card(card)
        self.descarte.push_top(card)

    def comprou_baralho(self, player: Jogador, comprou_baralho: bool):
        if comprou_baralho:
            card = self.baralho.retirarCarta()
        else:
            card = self.descarte.retirarCarta()
        player.adicionaCarta(card)
        

    def toggle_turn(self):
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
    
    def checa_fim_jogo(self):
        return len(self.remote_player.getTrincas()) == 3 or len(self.remote_player.getTrincas()) == 3

    def valido(self, trinca: list()):
        naipe_igual = False
        if trinca[0].getNaipe() == trinca[1].getNaipe() and trinca[0].getNaipe() == trinca[1].getNaipe():
            naipe_igual = True
        
        if naipe_igual:
            trinca.sort(key=lambda x: x.getNum(), reverse=False)
            return int(trinca[0].getNum())+1 == int(trinca[1].getNum()) and int(trinca[0].getNum())+2 == int(trinca[2].getNum())
        else:
            return trinca[0].getNum() == trinca[1].getNum and trinca[0].getNum() == trinca[2].getNum()