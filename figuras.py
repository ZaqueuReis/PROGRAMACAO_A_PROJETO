from abc import ABC, abstractmethod

class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.borda = cor_borda
        self.preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda
    
    @abstractmethod
    def desenhar(self,canvas):
        pass

    @abstractmethod
    def incompleta(self):
        pass

class Linha(Figura):

    def __init__(self, x1, y1, x2, y2, borda, tamanho_borda):
        super().__init__(borda, '', tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y
    
    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill = self.borda, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

class Rabisco(Figura):
    def __init__(self, pontos, borda, tamanho_borda):
        super().__init__(borda, '', tamanho_borda)
        self.pontos = pontos
    
    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill = self.borda, width = self.tamanho_borda)
    
    def incompleta(self):
        return len(self.pontos) <= 1

class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, borda, preenchimento, tamanho_borda):
        super().__init__(borda, preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline = self.borda, fill = self.preenchimento, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, borda, preenchimento, tamanho_borda):
        super().__init__(borda, preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline = self.borda, fill = self.preenchimento, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, borda, preenchimento, tamanho_borda):
        super().__init__(borda, preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio
    
    def atualizar(self, x, y) :
        raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5
        self.raio = raio

    def desenhar(self, canvas):
        canvas.create_oval(self.centro_x - self.raio, self.centro_y - self.raio, self.centro_x + self.raio, self.centro_y + self.raio, outline=self.borda, fill=self.preenchimento, width = self.tamanho_borda)

    def incompleta(self):
        return self.raio <= 0

class Poligono(Figura):

    def __init__(self, pontos, borda, preenchimento, tamanho_borda):
        super().__init__(borda, preenchimento, tamanho_borda)
        self.pontos = pontos
    
    def atualizar(self, x, y) :
        self.pontos.append((x,y))

    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos, outline=self.borda, fill=self.preenchimento, width = self.tamanho_borda)

    def incompleta(self):
        return len(self.pontos) < 3