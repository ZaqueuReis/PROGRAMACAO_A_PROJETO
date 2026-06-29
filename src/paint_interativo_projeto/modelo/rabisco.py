from modelo.Figura import Figura


class Rabisco(Figura):

    def __init__(self, pontos, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.pontos = pontos
    
    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill = self.cor_borda, width = self.tamanho_borda)
    
    def incompleta(self):
        return len(self.pontos) <= 1
