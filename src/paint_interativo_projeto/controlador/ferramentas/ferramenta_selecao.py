from controlador.ferramentas.ferramenta import Ferramenta
from controlador.ferramentas.retangulo_selecao import RetanguloSelecao

class FerramentaSelecao(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)
        self.ultima_posicao = None
        self.movimentando_figura = False
        self.retangulo_selecao = None
        self.inicioX_retangulo_selecao = 0
        self.inicioY_retangulo_selecao = 0

    def mouse_press(self, event):
        figuras_selecionadas = None
        figuras = self.controlador.desenho.obter_figuras()

        for figura in reversed(figuras): # usa reversed pois procuramos na lista de desenhos de trás para frente
            if figura.contem(event.x, event.y):
                figuras_selecionadas = figura
                break

        self.inicioX_retangulo_selecao = event.x
        self.inicioY_retangulo_selecao = event.y
        
        if figuras_selecionadas is None:
            self.retangulo_selecao = RetanguloSelecao(self.inicioX_retangulo_selecao, self.inicioY_retangulo_selecao)
            self.controlador.desenhar_figuras()
            return

        if self.controlador.ctrl_pressionado: 
            if figuras_selecionadas is not None:
                if figuras_selecionadas in self.controlador.desenho.obter_figuras_selecionadas():
                    self.controlador.desenho.remover_selecao(figuras_selecionadas)
                else:
                    self.controlador.desenho.adicionar_selecao(figuras_selecionadas)
        else:
        # Só irá trocar a seleção de clicar no canvas ou em uma figura não selecionada
        
            if figuras_selecionadas not in self.controlador.desenho.obter_figuras_selecionadas():
                self.controlador.desenho.limpar_selecao()

                if figuras_selecionadas is not None:
                    self.controlador.desenho.adicionar_selecao(figuras_selecionadas)

        if figuras_selecionadas is not None:
            self.ultima_posicao = (event.x, event.y)
            self.movimentando_figura = False
        else:
            self.ultima_posicao = None

        self.controlador.desenhar_figuras()
        
        
    def desenhar(self):
        '''Sempre que o controlador redesenha o canvas, este método
        é chamado para desenhar o retângulo de seleção, caso ele exista.'''
        
        if self.retangulo_selecao is not None:
            self.controlador.janela.desenhar_retangulo_selecao(self.retangulo_selecao)
            # Caso exista um retângulo de seleção, ele deve ser desenhado.
            # Esse retângulo é apenas um elemento visual temporário e não faz parte da lista de figuras do modelo.
            
    def mouse_move(self, event):
        figuras = self.controlador.desenho.obter_figuras_selecionadas()
        
        # Caso exista um retângulo de seleção, significa que o usuário está arrastando o mouse para criar uma área de seleção.
        if self.retangulo_selecao is not None:
            self.retangulo_selecao.mover_ponto_final(event.x, event.y) # Atualiza com o ponto do mouse arrastado
            self.controlador.desenhar_figuras()
            return

        if not figuras:
            return

        if self.ultima_posicao is None:
            return
        
        if not self.movimentando_figura:
            self.controlador.desenho.salvar_estado()
            self.movimentando_figura = True

        x_antigo, y_antigo = self.ultima_posicao
        dx = event.x - x_antigo
        dy = event.y - y_antigo
        
        for figura in figuras:
            figura.mover(dx, dy)

        self.ultima_posicao = (event.x, event.y)
        self.controlador.desenhar_figuras()

    def mouse_release(self, event):
        self.ultima_posicao = None
        self.movimentando_figura = False

        # Se não existe um retângulo de seleção, então a figura está sendo movimentada
        if self.retangulo_selecao is None:
            return

        # Recupera os pontos inicial e final do retângulo de seleção criado pelo usuário.
        x1 = self.retangulo_selecao.x1
        y1 = self.retangulo_selecao.y1
        x2 = self.retangulo_selecao.x2
        y2 = self.retangulo_selecao.y2

        menor_x = min(x1, x2)
        maior_x = max(x1, x2)
        menor_y = min(y1, y2)
        maior_y = max(y1, y2)

        # Remove qualquer seleção anterior para criar uma nova seleção baseada no retângulo atual.
        self.controlador.desenho.limpar_selecao()

        # Percorre todas as figuras existentes no desenho. Cada figura é testada para verificar se está dentro do retângulo de seleção.
        for figura in self.controlador.desenho.obter_figuras():
            if self.figura_dentro_retangulo_selecao(figura, menor_x, menor_y, maior_x, maior_y):
                self.controlador.desenho.adicionar_selecao(figura)

        # Remove o triângulo de seleção
        self.retangulo_selecao = None
        self.controlador.desenhar_figuras()
        
    def figura_dentro_retangulo_selecao(self, figura, x1, y1, x2, y2):
        '''Verifica se uma figura está dentro do retângulo de seleção'''

        if figura.__class__.__name__ == "FiguraComposta":
            # Caso seja uma figura composta, verificamos cada figura interna.
            # O grupo só será selecionado se TODAS as figuras que fazem parte dele estiverem dentro do retângulo de seleção.
            for figura_interna in figura.figuras:
                if not self.figura_dentro_retangulo_selecao(figura_interna, x1, y1, x2, y2):
                    return False
            return True
            
        elif figura.__class__.__name__ in ("Retangulo", "Oval"):
            return (min(figura.x1, figura.x2) >= x1 and max(figura.x1, figura.x2) <= x2 and min(figura.y1, figura.y2) >= y1 and max(figura.y1, figura.y2) <= y2)

        elif figura.__class__.__name__ == "Linha":
            return (min(figura.x1, figura.x2) >= x1 and max(figura.x1, figura.x2) <= x2 and min(figura.y1, figura.y2) >= y1 and max(figura.y1, figura.y2) <= y2)

        elif figura.__class__.__name__ == "Circulo":
            return (figura.centro_x - figura.raio >= x1 and figura.centro_x + figura.raio <= x2 and figura.centro_y - figura.raio >= y1 and figura.centro_y + figura.raio <= y2)

        elif figura.__class__.__name__ in ("Rabisco", "Poligono_irregular", "Poligono_regular"):
            for px, py in figura.pontos:
                if not (x1 <= px <= x2 and y1 <= py <= y2):
                    return False
            return True
         # Caso apareça algum tipo de figura não tratado, ela não será selecionada pelo retângulo.
        return False