from jogador import Jogador
from baralho import Baralho
from descarte import Descarte
from trinca import Trinca
from carta import Carta

class Mesa:
    def __init__(self):
        self.local_player = Jogador()
        self.remote_player = Jogador()

        # self.local_player.initialize(1, "local_player", "local_player")
        # self.remote_player.initialize(2, "remote_player", "remote_player")

        self.trincas = []

        self.match_status = 1
        self.baralho = None
        self.descarte = Descarte()
        
    def get_turn_player(self):
        if self.local_player.vez_jogada == True:
            return self.local_player
        else:
            return self.remote_player
        
    #def only_one_selected(player: Jogador): bool
        
    def get_card_amount(self):
        j_atual = self.get_turn_player()
        n = len(j_atual.cartas)
        return n
        
    def swap_turn(self):
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
        
    #def get_game_state(self): int
    
    def start_match(self, players, local_player_id):
        # self.baralho = Baralho()
        # self.descarte = Descarte()
        # self.local_player.reset()
        # self.remote_player.reset()
        self.local_player.initialize(1, players[0][1], players[0][0])
        self.remote_player.initialize(2, players[1][1], players[1][0])
        if players[0][2] == "1":
            self.local_player.toggle_turn()
            self.match_status = 2  #    waiting piece or origin selection (first action)
        else:
            self.remote_player.toggle_turn()
            self.match_status = 3  #    waiting remote action
        print("HERE!")
    
    def getStatus(self):
        return self.match_status
    
    def validar_trinca(self, trinca):
        if (trinca[0].naipe == trinca[1].naipe) and (trinca[0].naipe == trinca[2].naipe):
            trincaNumero = []
            for i in range(3):
                if trinca[i].num == 'A':
                    trincaNumero.append(1)
                elif trinca[i].num == 'J':
                    trincaNumero.append(11)
                elif trinca[i].num == 'Q':
                    trincaNumero.append(12)
                elif trinca[i].num == 'K':
                    trincaNumero.append(13)
                else:
                    trincaNumero.append(trinca[i].num)
            trincaNumero.sort()
            if ((trincaNumero[0]+1) == trincaNumero[1]) and ((trincaNumero[0]+2) == trincaNumero[2]):
                return True
            else:
                return False
        else:
            if (trinca[0].num == trinca[1].num) and (trinca[0].num == trinca[2].num):
                return True
            else:
                return False
            
    def checa_fim_jogo(self):
        return len(self.remote_player.getTrincas()) == 3 or len(self.remote_player.getTrincas()) == 3

    def receive_move(self,a_move):
        if self.baralho == None:
            print("receive baralho")
            self.baralho = Baralho()
            #print(a_move["baralho"])
            self.baralho.set_cards(self.getBaralhoFromDict(a_move["baralho"]))
            self.local_player.setCartas(self.getMaoFromCartas(a_move["j2_mao"]))
            self.remote_player.setCartas(self.getMaoFromCartas(a_move['j1_mao']))
            print(self.local_player.cartas)
            print(self.remote_player.cartas)
        else:
            print("receive else")
            if a_move["comprou_baralho"]:
                self.comprou_baralho(self.remote_player, True)
            else:
                self.comprou_baralho(self.remote_player, False)

            for trinca in a_move["trincas_baixadas"]:
                self.baixar_trinca(self.remote_player, trinca)
            self.descartar_carta(self.getCartaFromDict(a_move["carta_descarte"]))

            self.toggle_turn()

    #def update_trinca(self, trincas):
    
    #def set_turn_discard(self):
    
    #def set_turn_baixar(self):
    
    #def add_carta_trinca(self, card):

    def baixar_trinca(self, player: Jogador, trinca:list()):
        if self.valido(trinca):
            nova_trinca = Trinca(player, trinca)
            for card in trinca:
                player.remove_card(card)
            player.add_trinca(nova_trinca)
            self.trincas.append(nova_trinca)
            if self.checa_fim_jogo():
                self.match_status = 4
                
    def get_num_trincas(self, player: Jogador):
        return len(player.trincas)
    
    def checaVez(self):
        return self.local_player.vez_jogada

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

    def valido(self, trinca: list()):
        naipe_igual = False
        if trinca[0].getNaipe() == trinca[1].getNaipe() and trinca[0].getNaipe() == trinca[1].getNaipe():
            naipe_igual = True
        
        if naipe_igual:
            trinca.sort(key=lambda x: x.getNum(), reverse=False)
            return int(trinca[0].getNum())+1 == int(trinca[1].getNum()) and int(trinca[0].getNum())+2 == int(trinca[2].getNum())
        else:
            return trinca[0].getNum() == trinca[1].getNum and trinca[0].getNum() == trinca[2].getNum()
    
    def getCartaFromDict(self, dic):
        num = dic['num']
        naipe = dic['naipe']
        return Carta(num, naipe)
    
    def getMaoFromCartas(self, cartas):
        mao = []
        for i in cartas:
            num = i['num']
            naipe = i['naipe']
            mao.append(Carta(num, naipe))
        return mao

    def getBaralhoFromDict(self, dic):
        print("bar from dic")
        print(dic)
        bar = []
        for i in dic:
            print(i)
            num = i['num']
            naipe = i['naipe']
            bar.append(Carta(num, naipe))
        return bar
