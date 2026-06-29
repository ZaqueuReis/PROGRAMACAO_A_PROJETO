from abc import ABC, abstractmethod


#CLASSE ABSTRATA FIGURA =====================
class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda
    
    @abstractmethod
    def atualizar(self, *args): # Todas as figuras são obrigadas a ter atualizar, e não desenhar agora
        pass

    @abstractmethod
    def incompleta(self):
        pass


#CLASSE LINHA ==========================
class Linha(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


#CLASSE RABISCO ==========================
class Rabisco(Figura):

    def __init__(self, pontos, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.pontos = pontos
    
    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1

#CLASSE RETANGULO =============================
class Retangulo(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


#CLASSE OVAL ====================================
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
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


#CLASSE CIRCULO =================================
class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio
    
    def atualizar(self, x, y) :
        self.raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5 # substituição aqui, pois estava redundante

    def incompleta(self):
        return self.raio <= 0


# CLASSE POLIGONO =====================================
class Poligono(Figura):

    def __init__(self, pontos, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.pontos = pontos
        self.fechado = False # Tirei o self.mouse pois está função é do controler

    def atualizar(self, x, y):
        """
        Mantido apenas para preservar a interface da classe Figura, já que o polígono 
        é atualizado adicionando novos vértices. Como foi sugerido por Giovanny em sala
        """
        pass

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    # Função desenhar tirada, pois está no view

    def fechar(self): # Tirado canvas porque ele está na view
        self.fechado = True
        # Tirado o movimento de rastreio do mouse, pois é função do controler

    def incompleta(self):
        return len(self.pontos) < 3