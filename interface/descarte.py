class Descarte:
    def __init__(self):
        self.cartas = []
    
    def push_top(self, carta):
        self.cartas.append(carta)
    
    def retirarCarta(self):
        if len(self.cartas) < 1:
            return None
        return self.cartas.pop(-1)