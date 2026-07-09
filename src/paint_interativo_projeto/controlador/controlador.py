from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono
from controlador.ferramentas.ferramenta_linha import FerramentaLinha
from controlador.ferramentas.ferramenta_retangulo import FerramentaRetangulo
from controlador.ferramentas.ferramenta_oval import FerramentaOval
from controlador.ferramentas.ferramenta_circulo import FerramentaCirculo
from controlador.ferramentas.ferramenta_rabisco import FerramentaRabisco
from controlador.ferramentas.ferramenta_poligono import FerramentaPoligono
from controlador.ferramentas.ferramenta_selecao import FerramentaSelecao # importando para o controlador o arquivo criado

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
            "Poligono": FerramentaPoligono(self),
            "Selecionar": FerramentaSelecao(self) # adicionada a ferramenta seleção criada
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

        # Figuras já concluídas - Adequação para já incluir o destaque da borda se for selecionada
        figura_selecionada = self.desenho.obter_figura_selecionada()

        for figura in self.desenho.obter_figuras():
            figura.desenhar(self.janela, figura == figura_selecionada)

        # Figura que ainda está sendo desenhada
        figura_atual = self.desenho.obter_figura_atual()
        if figura_atual is not None:
            figura_atual.desenhar(self.janela)

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
                    
    # Método de salvar arquivos =====================             
    def salvar_arquivo_desenhos(self):
        caminho = self.janela.obter_caminhoPC_salvar()
        if not caminho:
            return
        
        self.desenho.salvar_desenhos(caminho)
        
        self.janela.aviso_salvamento_desenho() # Messagebox para avisar que os desenhos foram salvos
        
    # Método de abrir arquivos =====================     
    def abrir_arquivo_desenho(self):
        caminho = self.janela.obter_caminhoPC_abrir()
        if not caminho:
            return

        self.desenho.abrir_arquivo_desenho(caminho)
        
        self.desenhar_figuras()
        
        self.janela.aviso_carregamento_desenho() # Messagebox para avisar que os desenhos foram carregados com sucesso

    # Método de limpar todo o canvas =====================  
    def limpar_desenhos(self):
        
        if self.desenho.limpar_desenhos():
            self.desenhar_figuras()
            self.janela.aviso_limpeza_tela() # Messagebox para avisar que a tela foi limpa
        else:
            self.janela.aviso_tela_ja_limpa() # Message para avisar que a tela já está limpa, caso seja apertado o botão com a tela limpa
