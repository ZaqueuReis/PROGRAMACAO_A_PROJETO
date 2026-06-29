
from modelo.Figura import Figura

class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio
    
    def atualizar(self, x, y) :
        raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5
        self.raio = raio

    def desenhar(self, canvas):
        canvas.create_oval(self.centro_x - self.raio, 
                           self.centro_y - self.raio, 
                           self.centro_x + self.raio, 
                           self.centro_y + self.raio, 
                           outline=self.cor_borda, 
                           fill=self.cor_preenchimento, 
                           width = self.tamanho_borda)

    def incompleta(self):
        return self.raio <= 0

