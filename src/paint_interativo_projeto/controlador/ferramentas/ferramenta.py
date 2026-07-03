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