from modelo.figuras import Poligono_irregular
from .ferramenta import Ferramenta

'''Classe responsável por controlar toda a interação do usuário com a ferramenta
de desenho do poligono. Cada método representa um evento do mouse durante
a criação da figura (pressionar, mover e soltar o botão).'''


class FerramentaPoligonoIrregular(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)

        self.mouse_x = None
        self.mouse_y = None

    def mouse_press(self, event):
        desenho = self.controlador.desenho
        janela = self.controlador.janela

        figura = desenho.obter_figura_atual()

        # Primeiro clique
        if figura is None:
            figura = Poligono_irregular([(event.x, event.y)],janela.obter_cor_borda(),janela.obter_cor_preenchimento(),janela.obter_tamanho_borda())
            desenho.inicializar_figura_atual(figura)

        # Próximos cliques
        else:
            inicio_x, inicio_y = figura.pontos[0]
            distancia = ((event.x - inicio_x) ** 2 + (event.y - inicio_y) ** 2) ** 0.5

            if distancia < 10 and len(figura.pontos) >= 3:
                figura.fechar()
                desenho.adicionar_figura_concluida()

                self.mouse_x = None
                self.mouse_y = None

            else:
                figura.adicionar_ponto(event.x, event.y)

        self.controlador.desenhar_figuras()

        if self.controlador.desenho.obter_figura_atual() is not None:
            self.desenhar_linha_guia()

    def mouse_move(self, event):
        figura = self.controlador.desenho.obter_figura_atual()

        if figura is None:
            return

        self.mouse_x = event.x
        self.mouse_y = event.y

        self.controlador.desenhar_figuras()
        self.desenhar_linha_guia()

    def mouse_release(self, event):
        pass

    def desenhar_linha_guia(self):

        figura = self.controlador.desenho.obter_figura_atual()

        if figura is None:
            return

        if self.mouse_x is None:
            return

        ultimo_x, ultimo_y = figura.pontos[-1]

        mostrar_fechamento = False
        inicio_x = None
        inicio_y = None

        if len(figura.pontos) >= 3:
            inicio_x, inicio_y = figura.pontos[0]
            distancia = ((self.mouse_x - inicio_x) ** 2 + (self.mouse_y - inicio_y) ** 2) ** 0.5

            if distancia < 10:
                mostrar_fechamento = True

        self.controlador.janela.desenhar_linha_guia(ultimo_x, ultimo_y, self.mouse_x, self.mouse_y, mostrar_fechamento, inicio_x, inicio_y)