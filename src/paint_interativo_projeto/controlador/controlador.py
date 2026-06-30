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
