from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono
from controlador.ferramentas.ferramenta_linha import FerramentaLinha
from controlador.ferramentas.ferramenta_retangulo import FerramentaRetangulo
from controlador.ferramentas.ferramenta_oval import FerramentaOval
from controlador.ferramentas.ferramenta_circulo import FerramentaCirculo
from controlador.ferramentas.ferramenta_rabisco import FerramentaRabisco
from controlador.ferramentas.ferramenta_poligono import FerramentaPoligono

class Controlador:

    def __init__(self, desenho, janela):
        self.desenho = desenho # Referência ao model
        self.janela = janela # Referência ao view

        # Armazena a posição atual do mouse durante a construção de um polígono, permitindo desenhar a linha guia.
        self.mouse_x = None
        self.mouse_y = None

        # Associa cada ferramenta de desenho a opção correspondente (lembre que é em string) da interface
        self.ferramentas = {
            "Linha": FerramentaLinha(self),
            "Retangulo": FerramentaRetangulo(self),
            "Oval": FerramentaOval(self),
            "Circulo": FerramentaCirculo(self),
            "Rabisco": FerramentaRabisco(self),
            "Poligono": FerramentaPoligono(self)
        }

        # Eventos do mouse para os métodos do controlador 
        canvas = self.janela.obter_canvas()

        canvas.bind("<ButtonPress-1>", self.iniciar_figura_atual)
        canvas.bind("<B1-Motion>", self.atualizar_figura_atual)
        canvas.bind("<Motion>", self.atualizar_figura_atual)
        canvas.bind("<ButtonRelease-1>", self.incluir_figura_atual)
    
    # Retorna a ferramenta correspondente ao tipo de figura atualmente selecionado.
    def obter_ferramenta(self):
        return self.ferramentas[self.janela.obter_tipo_figura()]

    # Inicia a criação de uma nova figura =====================

    # Quando o mouse é pressionado
    def iniciar_figura_atual(self, event):
        # Informa o "tratamento" do clique do mouse para a ferramenta atualmente selecionada.
        self.obter_ferramenta().mouse_press(event)
        return
    
    # Atualiza a figura enquanto o mouse é movimetando =====================

    def atualizar_figura_atual(self, event):
        # Informa o "tratamento" do abandono do mouse para a ferramenta atualmente selecionada.
        self.obter_ferramenta().mouse_move(event)
        return

# Finaliza o desenho das figuras, exceto polígono porque precisa ser atualizado até chegar ao vertice final ===================

    # Quando o mouse é solto
    def incluir_figura_atual(self, event):
         # Informa o "tratamento" do abandono do mouse para a ferramenta atualmente selecionada.
        self.obter_ferramenta().mouse_release(event)
        return
    
    # Desenha todas as figuras naquela lista interessante da classe desenho =============================

    def desenhar_figuras(self):
        self.janela.limpar_canvas()

        # Figuras já concluídas
        for figura in self.desenho.obter_figuras():
            self.desenhar_figura(figura)

        # Figura que ainda está sendo desenhada
        figura_atual = self.desenho.obter_figura_atual()
        if figura_atual is not None:
            self.desenhar_figura(figura_atual)

            # Linha guia do polígono
            if isinstance(figura_atual, Poligono):
                if self.mouse_x is not None:
                    ultimo_x, ultimo_y = figura_atual.pontos[-1]

                    mostrar_fechamento = False
                    inicio_x = None
                    inicio_y = None

                    # Verifica se o cursor está próximo do primeiro vértice
                    if len(figura_atual.pontos) >= 3:
                        inicio_x, inicio_y = figura_atual.pontos[0]
                        distancia = ((self.mouse_x - inicio_x) ** 2 + (self.mouse_y - inicio_y) ** 2) ** 0.5

                        if distancia < 10:
                            mostrar_fechamento = True

                    self.janela.desenhar_linha_guia(ultimo_x, ultimo_y, self.mouse_x, self.mouse_y, mostrar_fechamento, inicio_x, inicio_y)

    # Método que desenha uma única figura na interface ========================
    def desenhar_figura(self, figura):

        if isinstance(figura, Linha):
            self.janela.desenhar_linha(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, figura.tamanho_borda)

        elif isinstance(figura, Rabisco):
            self.janela.desenhar_rabisco(figura.pontos, figura.cor_borda, figura.tamanho_borda)

        elif isinstance(figura, Retangulo):
            self.janela.desenhar_retangulo(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, figura.cor_preenchimento, figura.tamanho_borda)

        elif isinstance(figura, Oval):
            self.janela.desenhar_oval(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, figura.cor_preenchimento, figura.tamanho_borda)

        elif isinstance(figura, Circulo):
            self.janela.desenhar_circulo(figura.centro_x, figura.centro_y, figura.raio, figura.cor_borda, figura.cor_preenchimento, figura.tamanho_borda)

        elif isinstance(figura, Poligono):
            self.janela.desenhar_poligono(figura.pontos, figura.cor_borda, figura.cor_preenchimento, figura.tamanho_borda, figura.fechado)