from abc import ABC, abstractmethod

'''Classe abstrata ferramenta que serve de base para a construção das demais classes de ferramentas'''

class Ferramenta(ABC):

    def __init__(self, controlador):
        self.controlador = controlador

    @abstractmethod
    def mouse_press(self, event):
        pass

    @abstractmethod
    def mouse_move(self, event):
        pass

    @abstractmethod
    def mouse_release(self, event):
        pass
    
    def desenhar(self):
        pass
    
        """
        Antes o controlador.desenhar_figuras() desenhava apenas figuras do modelo.
        Quando foi criado o retangulo de seleção surge um problema:
        O retangulo de seleção nao possui ao modelo, porque nao é uma figura definitiva.
        É uma figura auxiliar, temporária...
        Então era preciso de algo para desenhar essa fingura temporariamente e quem conhece
        esse objeto é justamente a ferramenta de seleção.

        - Emanuel por que nao é um metodo abstrato?
        Até poderia ser, mas seria desnecessário, pois todas as outras ferramentas
        seriam obrigas a implementar esse método.
        """