import random
from carta import Carta

class Baralho:
    def __init__(self):
        self.cartas = []
        for naipe in (['paus', 'ouros', 'espadas', 'copas']):
            for num in range (1,14):
                if num==1:
                    self.cartas.append(Carta('A', naipe))
                elif num==13:
                    self.cartas.append(Carta('K', naipe))
                elif num==12:
                    self.cartas.append(Carta('Q', naipe))
                elif num==11:
                    self.cartas.append(Carta('J', naipe))
                else:
                    self.cartas.append(Carta(str(num), naipe))
        self.embaralhar()
    
    def embaralhar(self):
        random.shuffle(self.cartas)
    
    def distribuir_cartas(self):
        mao = []
        for _ in range(9):
            mao.append(self.cartas.pop())
        return mao
    
    def getCartas(self):
        return self.cartas
    
    def set_cards(self, cards):
        self.cartas = cards
    
    def retirarCarta(self):
        if len(self.cartas) < 1:
            return None
        return self.cartas.pop(-1)