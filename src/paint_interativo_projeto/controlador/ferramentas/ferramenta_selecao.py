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

        if figura_selecionada is not None:
            self.ultima_posicao = (event.x, event.y)
        else:
            self.ultima_posicao = None

        self.controlador.desenhar_figuras()

    def mouse_move(self, event):
        figura = self.controlador.desenho.obter_figura_selecionada()

        if figura is None:
            return

        if self.ultima_posicao is None:
            return

        x_antigo, y_antigo = self.ultima_posicao

        dx = event.x - x_antigo
        dy = event.y - y_antigo

        figura.mover(dx, dy)

        self.ultima_posicao = (event.x, event.y)

        self.controlador.desenhar_figuras()

    def mouse_release(self, event):
        self.ultima_posicao = None