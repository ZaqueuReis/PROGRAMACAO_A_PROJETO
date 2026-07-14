from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono
from controlador.ferramentas.ferramenta_linha import FerramentaLinha
from controlador.ferramentas.ferramenta_retangulo import FerramentaRetangulo
from controlador.ferramentas.ferramenta_oval import FerramentaOval
from controlador.ferramentas.ferramenta_circulo import FerramentaCirculo
from controlador.ferramentas.ferramenta_rabisco import FerramentaRabisco
from controlador.ferramentas.ferramenta_poligono import FerramentaPoligono
from controlador.ferramentas.ferramenta_poligonoRegular import FerramentaPoligonoRegular
from controlador.ferramentas.ferramenta_selecao import FerramentaSelecao 
from visao.fabrica_desenho import FabricaDesenho # importando a classe que desenha todas as figuras já com a largura

class Controlador:

    def __init__(self, desenho, janela):
        self.desenho = desenho # Referência ao model
        self.janela = janela # Referência ao view
        self.fabrica = FabricaDesenho(janela) # Referencia a FabricaDesenho
        self.ctrl_pressionado = False

        # Associa cada ferramenta de desenho a opção correspondente (lembre que é em string) da interface
        self.ferramentas = {
            "Linha": FerramentaLinha(self),
            "Retangulo": FerramentaRetangulo(self),
            "Oval": FerramentaOval(self),
            "Circulo": FerramentaCirculo(self),
            "Rabisco": FerramentaRabisco(self),
            "Poligono": FerramentaPoligono(self),
            "PoligonoRegular": FerramentaPoligonoRegular(self),
            "Selecionar": FerramentaSelecao(self) # adicionada a ferramenta seleção criada
        }

        # Eventos do mouse para os métodos do controlador 
        canvas = self.janela.obter_canvas()
        
        canvas.bind("<ButtonPress-1>", self.iniciar_figura_atual)
        canvas.bind("<B1-Motion>", self.atualizar_figura_atual)
        canvas.bind("<Motion>", self.atualizar_figura_atual)
        canvas.bind("<Double-Button-1>", self.mouse_double_click)
        canvas.bind("<ButtonRelease-1>", self.incluir_figura_atual)
        self.janela.root.bind("<Delete>", self.deletar_selecionada)
        self.janela.root.bind("<Up>", self.mover_para_topo)
        self.janela.root.bind("<Down>", self.mover_para_fundo)
        self.janela.root.bind("<Right>", self.mover_para_frente)
        self.janela.root.bind("<Left>", self.mover_para_tras)
        self.janela.root.bind("<Control-c>", self.copiar_figura)
        self.janela.root.bind("<Control-v>", self.colar_figura)
        self.janela.root.bind("<KeyPress-Control_L>", self.ctrl_press) #CRIAÇÃO DOS BOTOES CTRL LEFT
        self.janela.root.bind("<KeyRelease-Control_L>", self.ctrl_release) #CRIAÇÃO DOS BOTOES CTRL LEFT
        self.janela.root.bind("<KeyPress-Control_R>", self.ctrl_press)# CRIAÇÃO DOS BOTOES CTRL RIGHT
        self.janela.root.bind("<KeyRelease-Control_R>", self.ctrl_release) # CRIAÇÃO DOS BOTOES CTRL RIGHT
        
        #======= POR QUE O self.janela.root.bind é diferente dos demais?
        '''
        PARA RECEBER COMANDOS DO TECLADO A JANELA PRECISA ESTÁ EM FOCO,
        EU PODERIA RESOLVER DEIXANDO APENAS O CANVAS EM FOCO COM O COMANDO:
        - canvas.focus_set()  - setaria foco em todo canvas;
        
        Mas ficava um contorno em volta do canvas e quando o usuário
        clicava fora do canvas acabava tirando o foco e a função delete
        parava de funciona.
        
        Então com o self.janela.root.bind;
        Ele associa o delete a todo o programa, não precisa um widgete em espécifico
        que anteriormente era o canvas estar em foco, então ele consegue capturar o click
        da tecla delete;   
        '''
        #==================================
        
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
    
    def mouse_double_click(self, event) :
        #Garantindo que isso só ocorra caso a figura em questão seja poligno regular
        tipo_selecionado = self.janela.obter_tipo_figura()
        ferramenta_ativa = self.ferramentas.get(tipo_selecionado)

        if ferramenta_ativa and hasattr(ferramenta_ativa, 'mouse_double_click') :
            ferramenta_ativa.mouse_double_click(event)
    # Desenha todas as figuras naquela lista interessante da classe desenho =============================

    def desenhar_figuras(self):
        self.janela.limpar_canvas()

        # Figuras já concluídas - Adequação para já incluir o destaque da borda se for selecionada
        selecionadas = self.desenho.obter_figuras_selecionadas()

        for figura in self.desenho.obter_figuras():
            self.fabrica.desenhar(figura, figura in selecionadas)

        # Figura que ainda está sendo desenhada
        figura_atual = self.desenho.obter_figura_atual()
        if figura_atual is not None:
            self.fabrica.desenhar(figura_atual)
                    
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
            
    #MÉTODO PARA DELETAR SELECIONADA =================
    def deletar_selecionada(self, event):
        
        if self.desenho.deletar_selecionada():
            self.desenhar_figuras()
            

        #=========== MOVER PARA O TOPO:
    
    
    def mover_para_topo(self, event):
        self.desenho.mover_para_topo()
        self.desenhar_figuras()
        
        
    def mover_para_fundo(self, event):
        self.desenho.mover_para_fundo()
        self.desenhar_figuras()
        
    def mover_para_tras(self, event):
        self.desenho.mover_para_tras()
        self.desenhar_figuras()
        
    def mover_para_frente(self, event):
        self.desenho.mover_para_frente()
        self.desenhar_figuras()
        
    def copiar_figura(self, event):
        self.desenho.copiar_figura()
        
    def colar_figura(self, event):
        self.desenho.colar_figura()
        self.desenhar_figuras()


    #Método para mudar a cor da figura selecionada -> borda =================
    def mudar_cor_borda_selecionada(self, nova_cor):

        for figura in self.desenho.obter_figuras_selecionadas():
            figura.cor_borda = nova_cor

        self.desenhar_figuras()

            
    #Método para mudar a cor da figura selecionada -> preenchimento=================
    def mudar_cor_preenchimento_selecionada(self, nova_cor):

        for figura in self.desenho.obter_figuras_selecionadas():
            figura.cor_preenchimento = nova_cor

        self.desenhar_figuras()

    #Método para mudar a cor da figura selecionada -> espessura da borda=================
    def mudar_tamanho_borda_selecionada(self, tamanho):

        for figura in self.desenho.obter_figuras_selecionadas():
            figura.tamanho_borda = tamanho

        self.desenhar_figuras()
            
            
    def ctrl_press(self, event):
        self.ctrl_pressionado = True

    #CRIAÇÃO DOS MÉTODOS PARA SABER SE O CTRL ESTA PRESSIONADO OU SOLTO
    def ctrl_release(self, event):
        self.ctrl_pressionado = False
    
    # Método para agrupar as figuras, tornando-as compostas
    def agrupar_figuras(self):
        self.desenho.agrupar_figuras()
        self.desenhar_figuras()
    
    # Método para desagrupar as figuras, tornando-as únicas novamente
    def desagrupar_figuras(self):
        self.desenho.desagrupar_figuras()
        self.desenhar_figuras()