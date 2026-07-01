from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

class Controlador:

    def __init__(self, desenho, janela):
        self.desenho = desenho # Referência ao model
        self.janela = janela # Referência ao view

        # Armazena a posição atual do mouse durante a construção de um polígono, permitindo desenhar a linha guia.
        self.mouse_x = None
        self.mouse_y = None

        # Associa o nome da figura selecionada as suas classes do model
        self.dict_classes_figuras = {
            'Oval': Oval,
            'Circulo': Circulo,
            'Retangulo': Retangulo,
            'Rabisco': Rabisco,
            'Poligono': Poligono,
            'Linha': Linha
        }

        # Eventos do mouse para os métodos do controlador 
        canvas = self.janela.obter_canvas()

        canvas.bind("<ButtonPress-1>", self.iniciar_figura_atual)
        canvas.bind("<B1-Motion>", self.atualizar_figura_atual)
        canvas.bind("<Motion>", self.atualizar_figura_atual)
        canvas.bind("<ButtonRelease-1>", self.incluir_figura_atual)

    # Inicia a criação de uma nova figura =====================

    # Quando o mouse é pressionado
    def iniciar_figura_atual(self, event):
        figura_atual = self.desenho.obter_figura_atual()
        tipo = self.janela.obter_tipo_figura()
        cls_figura = self.dict_classes_figuras.get(tipo)

        # Travamento de segurança caso uma figura selecionada não exista para aprimoramento do código no fututo
        if not cls_figura:
            return

    # Caso políogno
        if tipo == 'Poligono':

            # Primeiro clique: cria o polígono
            if figura_atual is None:
                figura_atual = cls_figura([(event.x, event.y)], self.janela.obter_cor_borda(), self.janela.obter_cor_preenchimento(), self.janela.obter_tamanho_borda())
                self.desenho.inicializar_figura_atual(figura_atual)

            else:

                # Obtém o primeiro vértice
                p_inicio_x, p_inicio_y = figura_atual.pontos[0]

                # Calcula a distância até o primeiro vértice
                distancia = ((event.x - p_inicio_x) ** 2 +(event.y - p_inicio_y) ** 2) ** 0.5

                # Se o usuário clicar próximo ao primeiro ponto, fecha poligono e pinta por dentro
                if distancia < 10 and len(figura_atual.pontos) >= 2:
                    figura_atual.fechar()
                    self.desenho.adicionar_figura_concluida()

                    self.mouse_x = None
                    self.mouse_y = None

                else:
                     # Caso contrário adiciona um novo vértice
                    figura_atual.adicionar_ponto(event.x,event.y)

            self.desenhar_figuras()
            return

        # Caso retângulo e oval
        if tipo in ['Oval', 'Retangulo']:
            figura_atual = cls_figura(event.x, event.y, event.x, event.y, self.janela.obter_cor_borda(), self.janela.obter_cor_preenchimento(), self.janela.obter_tamanho_borda())

        # Caso linha
        elif tipo == 'Linha':
            figura_atual = cls_figura(event.x, event.y, event.x, event.y, self.janela.obter_cor_borda(), self.janela.obter_tamanho_borda())

        # Caso rabisco
        elif tipo == 'Rabisco':
            figura_atual = cls_figura([(event.x, event.y)], self.janela.obter_cor_borda(), self.janela.obter_tamanho_borda())

        # Caso círculo
        elif tipo == 'Circulo':
            figura_atual = cls_figura(event.x, event.y, 0, self.janela.obter_cor_borda(), self.janela.obter_cor_preenchimento(), self.janela.obter_tamanho_borda())

        # Armazena a figura em construção
        self.desenho.inicializar_figura_atual(figura_atual)
    
    # Atualiza a figura enquanto o mouse é movimetando =====================

    def atualizar_figura_atual(self, event):
        figura_atual = self.desenho.obter_figura_atual()

        if figura_atual is None:
            return

        # Atualização apenas a linha guia, se for poligono
        if isinstance(figura_atual, Poligono):
            self.mouse_x = event.x
            self.mouse_y = event.y

            self.desenhar_figuras()
            return

        # Caso para as outras figuras, vai atualizando enquanto mouse ficar pressionado, por isso o uso do event.state
        if event.state & 0x0100:
            figura_atual.atualizar(event.x,event.y)
            self.desenhar_figuras()

# Finaliza o desenho das figuras, exceto polígono porque precisa ser atualizado até chegar ao vertice final ===================

    # Quando o mouse é solto
    def incluir_figura_atual(self, event):
        figura_atual = self.desenho.obter_figura_atual()

        if figura_atual is None:
            return

        # se for polígono, é atualizado por cliques sucessivos
        if isinstance(figura_atual, Poligono):
            return

        # para armazenar apenas figuras completas
        if not figura_atual.incompleta():
            self.desenho.adicionar_figura_concluida()

        self.desenhar_figuras()
    
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