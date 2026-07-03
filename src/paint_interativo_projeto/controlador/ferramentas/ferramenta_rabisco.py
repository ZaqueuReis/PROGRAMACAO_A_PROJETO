from modelo.figuras import Rabisco
from .ferramenta import Ferramenta

'''Classe responsável por controlar toda a interação do usuário com a ferramenta
de desenho do rabisco. Cada método representa um evento do mouse durante
a criação da figura (pressionar, mover e soltar o botão).'''

class FerramentaRabisco(Ferramenta):

    def mouse_press(self, event):
        figura = Rabisco([(event.x, event.y)], self.controlador.janela.obter_cor_borda(), self.controlador.janela.obter_tamanho_borda())
        self.controlador.desenho.inicializar_figura_atual(figura)

    def mouse_move(self, event):
        figura = self.controlador.desenho.obter_figura_atual()

        if figura is None:
            return

        if event.state & 0x0100:
            figura.atualizar(event.x, event.y)
            self.controlador.desenhar_figuras()

    def mouse_release(self, event):
        figura = self.controlador.desenho.obter_figura_atual()

        if figura is None:
            return

        if not figura.incompleta():
            self.controlador.desenho.adicionar_figura_concluida()

        self.controlador.desenhar_figuras()