from controlador.ferramentas.ferramenta import Ferramenta

class FerramentaSelecao(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)
        self.ultima_posicao = None

    def mouse_press(self, event):
        figuras_selecionadas = None
        figuras = self.controlador.desenho.obter_figuras()

        for figura in reversed(figuras): # usa reversed pois procuramos na lista de desenhos de trás para frente
            if figura.contem(event.x, event.y):
                figuras_selecionadas = figura
                break
            
        if self.controlador.ctrl_pressionado: #SE O CTRL ESTIVER PRESSIONADO SIGA O BLOCO A SEGUIR:
            if figuras_selecionadas is not None:
                if figuras_selecionadas in self.controlador.desenho.obter_figuras_selecionadas():
                    self.controlador.desenho.remover_selecao(figuras_selecionadas)
                else:
                    self.controlador.desenho.adicionar_selecao(figuras_selecionadas)
        else:
        # SO IRÁ TROCAR A SELECAO SE CLICAR EM UMA FIGURA QUE NAO ESTA SELECIONADA OU LOCAL
        #FOI A UNICA MANEIRA QUE EU CONSEGUI IMPLEMENTAR ISSO
        
            if figuras_selecionadas not in self.controlador.desenho.obter_figuras_selecionadas():
                self.controlador.desenho.limpar_selecao()

                if figuras_selecionadas is not None:
                    self.controlador.desenho.adicionar_selecao(figuras_selecionadas)


        if figuras_selecionadas is not None:
            self.ultima_posicao = (event.x, event.y)
        else:
            self.ultima_posicao = None

        self.controlador.desenhar_figuras()

    def mouse_move(self, event):
        figuras = self.controlador.desenho.obter_figuras_selecionadas()

        if not figuras:
            return

        if self.ultima_posicao is None:
            return

        x_antigo, y_antigo = self.ultima_posicao

        dx = event.x - x_antigo
        dy = event.y - y_antigo
        
        for figura in figuras:
            
            figura.mover(dx, dy)

        self.ultima_posicao = (event.x, event.y)

        self.controlador.desenhar_figuras()

    def mouse_release(self, event):
        self.ultima_posicao = None


