from abc import ABC, abstractmethod

class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda

    @abstractmethod
    def desenhar(self, canvas):
        pass

    @abstractmethod
    def incompleta(self):
        pass