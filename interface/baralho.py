import random
from carta import Carta

class Baralho:
    def __init__(self):
        self.cartas = []
        for _ in range(2):  # baralho de 104 cartas
            for naipe in (['paus', 'ouros', 'espadas', 'copas']):   # baralho de 52 cartas
                for num in range (1,14):
                    self.cartas.append(Carta(num, naipe))
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