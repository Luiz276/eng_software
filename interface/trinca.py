class Trinca:
    def __init__(self, jogador, cartas):
        self.cartas = cartas
        self.dono = jogador
    
    def getDono(self):
        return self.dono

    def getCartas(self):
        return self.cartas