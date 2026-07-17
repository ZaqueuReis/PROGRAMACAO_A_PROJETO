# Classe direcionada apenas para o retângulo vermelho da seleção das figuras no canvas

class RetanguloSelecao:
    
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def mover_ponto_final(self, x, y):
        self.x2 = x
        self.y2 = y


