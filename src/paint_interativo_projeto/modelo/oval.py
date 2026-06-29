from modelo.Figura import Figura

class Oval(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas):
        canvas.create_oval(self.x1, 
                           self.y1, 
                           self.x2, 
                           self.y2, outline = self.cor_borda, 
                           fill = self.cor_preenchimento, 
                           width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

