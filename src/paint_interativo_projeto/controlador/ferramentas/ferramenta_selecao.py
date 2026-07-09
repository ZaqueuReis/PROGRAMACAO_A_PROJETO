from controlador.ferramentas.ferramenta import Ferramenta

class FerramentaSelecao(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)
        self.ultima_posicao = None

    def mouse_press(self, event):
        figura_selecionada = None
        figuras = self.controlador.desenho.obter_figuras()

        for figura in reversed(figuras): # usa reversed pois procuramos na lsita de desenhos de trás para frente
            if figura.contem(event.x, event.y):
                figura_selecionada = figura
                break

        self.controlador.desenho.definir_figura_selecionada(figura_selecionada)
        self.ultima_posicao = (event.x, event.y)
        self.controlador.desenhar_figuras()

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass