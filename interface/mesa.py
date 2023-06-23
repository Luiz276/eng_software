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
        
    def get_card_amount(self):
        j_atual = self.get_turn_player()
        n = len(j_atual.cartas)
        return n
        
    def swap_turn(self):
        if self.getStatus() == 3:
            self.match_status = 2
        else:
            self.match_status = 3
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
    
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
            
    def checa_fim_jogo(self):
        return len(self.remote_player.getTrincas()) == 3 or len(self.local_player.getTrincas()) == 3

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
        elif a_move['match_status'] == 'end':
            print('END GAME')
        else:
            print("receive else")
            if a_move["comprou_baralho"]:
                self.comprou_baralho(self.remote_player, True)
            else:
                self.comprou_baralho(self.remote_player, False)

            trinca = []
            print(a_move["trincas_baixadas"])
            for trinca in a_move["trincas_baixadas"]:
                print(trinca)
                self.baixar_trinca(self.remote_player, self.getTrincaFromDict(trinca))
                print(self.remote_player.getTrincas())
            
            if a_move["carta_descarte"] != None:
                self.descartar_carta(self.remote_player, self.getCartaFromDict(a_move["carta_descarte"]))

            # if a_move['match_status'] == 'end':
            #     print("END GAME")

            self.toggle_turn()
        #self.swap_turn()

    def baixar_trinca(self, player: Jogador, trinca:list()):
        if self.valido(trinca):
            nova_trinca = Trinca(player, trinca)
            for card in trinca:
                player.remove_card(card.num, card.naipe)
            player.add_trinca(nova_trinca)
            self.trincas.append(nova_trinca)
            if self.checa_fim_jogo():
                self.match_status = 4
            return True
        return False
                
    def get_num_trincas(self, player: Jogador):
        return len(player.trincas)
    
    def checaVez(self):
        return self.local_player.vez_jogada

    def descartar_carta(self, player:Jogador, card):
        player.remove_card(card.num, card.naipe)
        self.descarte.push_top(card)
        self.toggle_turn()

    def comprou_baralho(self, player: Jogador, comprou_baralho: bool):
        if comprou_baralho:
            card = self.baralho.retirarCarta()
            if len(self.baralho.getCartas()) == 0:
                self.baralho.set_cards = self.descarte.cartas
                self.descarte.cartas = []
                self.baralho.embaralhar()
        else:
            card = self.descarte.retirarCarta()
        player.adicionaCarta(card)
        

    def toggle_turn(self):
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()

    def valido(self, trinca: list()):
        print("validando")
        naipe_igual = False
        if trinca[0].getNaipe() == trinca[1].getNaipe() and trinca[0].getNaipe() == trinca[2].getNaipe():
            naipe_igual = True
        
        if naipe_igual:
            print("naipe igual")
            trinca.sort(key=lambda x: x.getNum(), reverse=False)
            return int(trinca[0].getNum())+1 == int(trinca[1].getNum()) and int(trinca[0].getNum())+2 == int(trinca[2].getNum())
        else:
            print("naipe diferente")
            return int(trinca[0].getNum()) == int(trinca[1].getNum()) and int(trinca[0].getNum()) == int(trinca[2].getNum())
    
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
    
    def getTrincaFromDict(self, dic):
        print("trinca from dict")
        print(dic)
        trinca = []
        for i in dic:
            num = i['num']
            naipe = i['naipe']
            trinca.append(Carta(num, naipe))
        return trinca
