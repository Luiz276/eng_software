

class Jogador:
    def __init__(self):
        self.cartas = []
        self.trincas = []
        self.vez_jogada = False

    def initialize(self, aSymbol, an_id, a_name):
        #self.reset()
        self.identifier = an_id  #   string
        self.symbol = aSymbol  # int
        self.name = a_name  #   string
        #self.cartas = baralho.distribuir_cartas()
    
    def setCartas(self, cartas):
        self.cartas = cartas

    def reset(self):
        self.identifier = ""  #   string
        self.name = ""  #   string
        self.symbol = None  # int
        self.cartas = []
        self.trincas = []
        self.vez_jogada = False

    def toggle_turn(self):
        if self.vez_jogada:
            self.vez_jogada=False
        else:
            self.vez_jogada=True
    
    def adicionaCarta(self, carta):
        self.cartas.append(carta)
    
    def getCartas(self):
        return self.cartas
    
    def remove_card(self, num, naipe):
        for i in self.cartas:
            if i.num == num and i.naipe == naipe:
                self.cartas.remove(i)
                break
    
    def getTrincas(self):
        return self.trincas
    
    def add_trinca(self, trinca):
        self.trincas.append(trinca)