

class Jogador:
    def __init__(self):
        self.cartas = []
        self.trincas = []
        self.vez_jogada = False

    def initialize(self, aSymbol, an_id, a_name, baralho):
        self.reset()
        self.identifier = an_id  #   string
        self.symbol = aSymbol  # int
        self.name = a_name  #   string
        self.cartas = baralho.distribuir_cartas()

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