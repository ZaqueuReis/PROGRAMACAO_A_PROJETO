from tkinter import *
from tkinter import ttk, font
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox


class Janela:

    def __init__(self):
        self.controller = None

        self.root = Tk()
        self.root.title("Paint - Figuras Compostas")

        # Frame da parte superior
        self.frame = Frame(self.root)
        self.frame.pack()

        #Frame da parte inferior (para os botões)
        self.frame_botoes = Frame(self.frame)
        self.frame_botoes.grid(row=1, column=0, columnspan=11, sticky=W)

        paddings = {'padx': 5, 'pady': 5}

        negrito = font.Font(family='Arial', size=10, weight='bold')

        # Widgets de texto e seleção do tipo da figura

        label_1 = ttk.Label(self.frame, text='Formato:', font=negrito)
        label_1.grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(self.root)

        self.option_menu = ttk.OptionMenu(
            self.frame,
            self.tipo_figura_var,
            'Selecionar', # Acrescentei e definir o selecionar como o inicio do programa, podemos trocar depois...
            'Selecionar',
            'Linha',
            'Retangulo',
            'Oval',
            'Circulo',
            'Rabisco',
            'Poligono',
            'PoligonoRegular',
        )

        self.option_menu.grid(column=1, row=0, sticky=W, **paddings)

        # Widgets de texto e seleção da cor da borda das figuras

        label_2 = ttk.Label(self.frame, text='Cor da borda:', font=negrito)
        label_2.grid(column=2, row=0, sticky=W, **paddings)

        self.cor_borda_var = StringVar(self.root, value='black')

        botao_cor_borda = ttk.Button(self.frame, text='Escolher cor da borda', command=self.escolher_cor_borda)
        botao_cor_borda.grid(column=3, row=0, sticky=W, **paddings)
        
        #Caixa de cor borda
        self.caixa_cor_borda = Label(self.frame, bg=self.cor_borda_var.get(), width=3, relief='solid')
        self.caixa_cor_borda.grid(column=4, row=0, sticky=W , **paddings)

        #implementação do botão na caixa -> cor_borda
        self.caixa_cor_borda.bind("<Button-1>", lambda event : self.controller.mudar_cor_borda_selecionada(self.cor_borda_var.get()) if self.controller else None)
        
        # Widgets de texto e seleção da cor do preenchimento das figuras

        label_3 = ttk.Label(self.frame, text='Cor preenchimento:', font=negrito)
        label_3.grid(column=5, row=0, sticky=W, **paddings)

        self.cor_preenchimento_var = StringVar(self.root, value='white')

        botao_cor_prrenchimento = ttk.Button(self.frame, text='Escolher cor do preenchimento', command=self.escolher_cor_preenchimento)
        botao_cor_prrenchimento.grid(column=6, row=0, sticky=W, **paddings)
 
        #Caixa de cor preenchimento

        self.caixa_cor_preenchimento = Label(self.frame, bg=self.cor_preenchimento_var.get(), width=3, relief='solid')
        self.caixa_cor_preenchimento.grid(column=7, row=0, sticky=W, **paddings)
        
        #implementação do botão na caixa -> cor_preenchimento
        self.caixa_cor_preenchimento.bind("<Button-1>", lambda event : self.controller.mudar_cor_preenchimento_selecionada(self.cor_preenchimento_var.get()) if self.controller else None)
        
        # Widgets de texto e seleção da espessura da borda das figuras

        label_4 = ttk.Label(self.frame, text='Espessura da borda:', font=negrito)
        label_4.grid(column=8, row=0, sticky=W, **paddings)

        self.tamanho_borda = StringVar(self.root, value='1')

        self.barra_espessura = ttk.Scale(
            self.frame,
            from_= 1,
            to = 10,
            orient = 'horizontal',
            command=lambda v: self.tamanho_borda.set(str(int(float(v))))
        )

        self.barra_espessura.grid(column=9, row=0, sticky=W, **paddings)

        # Label adicional para permitir o usuário verificar qual a espessura selecionada

        self.label_espessura = ttk.Label(
            self.frame,
            textvariable=self.tamanho_borda,
            width=2
            )
        
        self.label_espessura.grid(column=10, row=0, sticky=W, **paddings)
        
        # Widgets para salvar, abrir arquivos e limpar tudo 

        botao_para_salvar = ttk.Button(self.frame_botoes, text='Salvar', command=lambda: self.controller.salvar_arquivo_desenhos())
        botao_para_salvar.grid(column = 0, row = 1, sticky=W, **paddings)

    
        botao_para_abrir = ttk.Button(self.frame_botoes, text='Abrir', command=lambda: self.controller.abrir_arquivo_desenho())
        botao_para_abrir.grid(column = 1, row = 1, sticky=W, **paddings)


        botao_para_limpar = ttk.Button(self.frame_botoes, text='Limpar Tudo', command=lambda: self.controller.limpar_desenhos())
        botao_para_limpar.grid(column = 2, row = 1, sticky=W, **paddings)

        # Botão para agrupar
        botao_agrupar = ttk.Button(self.frame_botoes, text="Agrupar", command=lambda: self.controller.agrupar_figuras())
        botao_agrupar.grid(column=3, row=1, sticky=W, **paddings)
        
        # Botão para desagrupar
        botao_desagrupar = ttk.Button(self.frame_botoes, text="Desagrupar",command=lambda: self.controller.desagrupar_figuras())
        botao_desagrupar.grid(column=4, row=1, sticky=W, **paddings)
        
        # Parte da área de desenho (canvas)

        self.canvas = Canvas(self.frame, bg='white', width=1920, height=1080)
        self.canvas.grid(column=0, row=4, columnspan=100, sticky=W, **paddings)

    #Estes métodos serão chamados pelo controle para atualizar a view
    def atualizar_indicador_borda(self, cor_hex) :
        self.caixa_cor_borda.config(bg=cor_hex)
        
    def atualizar_indicador_preenchimento(self, cor_hex) :
        self.caixa_cor_preenchimento.config(bg=cor_hex)

    # Configuração do widget de escolher qualquer cor arbitrária

    def escolher_cor_borda(self, event=None):
        cor = colorchooser.askcolor(title="Escolha a cor da borda")
        if cor[1]:
            self.cor_borda_var.set(cor[1])
            self.atualizar_indicador_borda(cor[1])
            
            #Se houver alguma figura selecionada, manda um aviso para o controlador alterar a cor da mesma
            if self.controller :
                self.controller.mudar_cor_borda_selecionada(cor[1])
            
    def escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")
        if cor[1]:
            self.cor_preenchimento_var.set(cor[1])
            self.atualizar_indicador_preenchimento(cor[1])
            
            #Se houver alguma figura selecionada, manda um aviso para o controlador alterar a cor da mesma
            if self.controller :
                self.controller.mudar_cor_preenchimento_selecionada(cor[1])

    # Getters para obter os atributos da janela

    def obter_tipo_figura(self):
        return self.tipo_figura_var.get()

    def obter_cor_borda(self):
        return self.cor_borda_var.get()

    def obter_cor_preenchimento(self):
        return self.cor_preenchimento_var.get()

    def obter_tamanho_borda(self):
        return int(self.tamanho_borda.get())

    def obter_canvas(self):
        return self.canvas

    # Limpar todo o Canvas

    def limpar_canvas(self):
        self.canvas.delete("all")
    
    # Registra o controlador que atenderá as ações da interface
    def registrar_controlador(self, controlador):
        self.controller = controlador

    '''
    ==================== Part - 1 : salvar desenhos -> - Como alguns metódos são do tkinter,
    então algumas partes terão que ficar na view -> visao'''

    def obter_caminhoPC_salvar(self):
        return filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Arquivos Pickle", "*.pkl")]) # Mudança pois agora é pickle
    '''
    - filedialog.asksavesfilename = método do tkinter que faz a janela de salvamento aparecer na tela;
    
    - defaultextension=".pkl": se o usuário apenas digitar o nome do arquivo e esquecer de colocar a extensão
    que será ele, o tkinter irá adiciona o .pkl automaticamente no final;
    
    - filetypes=[("Arquivos Pickle", "*.pkl")]: cria um filtro na parte inferior da janela. 
      Isso faz com que o sistema mostre apenas arquivos com a extensão .pkl;
    
    '''
    
    '''
    ==================== Part - 2 : Encontrar arquivo -> -Para ser mais exato, o caminho, no gerenciador de arquivos''' 

    def obter_caminhoPC_abrir(self):
        return filedialog.askopenfilename(filetypes=[("Arquivos Pickle", "*.pkl")]) # Mudança pois agora é pickle
    
    '''
    - filedialog.askopenfilename: método do tkinter que abre a janela para selecionar um arquivo existente no computador;
    
    - filetypes=[("Arquivos Pickle", "*.pkl")]: força a janela a exibir apenas arquivos .pkl;
    
    '''
    
    # Métodos que retornam messagebox - módulo do tkinter que recebe mensagens de aviso =============================
    
    def aviso_salvamento_desenho(self):
        return messagebox.showinfo("Sucesso", "Desenho(s) salvo(s) com sucesso!")
    
    def aviso_carregamento_desenho(self):
         return messagebox.showinfo("Sucesso", "Desenho(s) carregado(s) com sucesso!")
     
    def aviso_limpeza_tela(self):
        return messagebox.showinfo("Sucesso", "Tela limpa!")
    
    def aviso_tela_ja_limpa(self):
        return messagebox.showwarning("Aviso", "A tela já está limpa.")

    # Métodos que permitem desenhar cada tipo de figura ===============================

    def desenhar_linha(self, x1, y1, x2, y2, cor_borda, tamanho_borda):
        self.canvas.create_line(x1, y1, x2, y2, fill=cor_borda, width=tamanho_borda)

    def desenhar_rabisco(self, pontos, cor_borda,tamanho_borda):
        self.canvas.create_line(pontos, fill=cor_borda, width=tamanho_borda)

    def desenhar_retangulo(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento, width=tamanho_borda)

    def desenhar_oval(self,x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        self.canvas.create_oval(x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento, width=tamanho_borda)

    def desenhar_circulo(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        self.canvas.create_oval(centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio, outline=cor_borda, fill=cor_preenchimento, width=tamanho_borda)

    def desenhar_poligono(self, pontos, cor_borda, cor_preenchimento, tamanho_borda, fechado):
        if len(pontos) == 0:
            return

        coordenadas = []
        for x, y in pontos:
            coordenadas.extend([x, y])

        if fechado:
            self.canvas.create_polygon(coordenadas, outline=cor_borda, fill=cor_preenchimento, width=tamanho_borda)

        else:
            if len(pontos) >= 2:
                self.canvas.create_line(coordenadas, fill=cor_borda, width=tamanho_borda)

    def desenhar_linha_guia(self, ultimo_x, ultimo_y, mouse_x, mouse_y, mostrar_fechamento=False, inicio_x=None, inicio_y=None):
        self.canvas.create_line(ultimo_x, ultimo_y, mouse_x, mouse_y, fill="black", dash=(4, 4))

        if mostrar_fechamento:
            self.canvas.create_rectangle(inicio_x - 5, inicio_y - 5, inicio_x + 5, inicio_y + 5, outline="red", fill="white")
    
    def desenhar_poligono_regular(self, pontos, cor_borda, cor_preenchimento, tamanho_borda, fechado) :
        if not pontos or len(pontos) < 3 :
            return
        coordenadas = []
        for x, y in pontos :
            coordenadas.extend([x, y])
        self.canvas.create_polygon(
            coordenadas,
            outline=cor_borda,
            fill=cor_preenchimento,
            width=tamanho_borda
        )
    # Pra finalizar, loop da janela

    
    def desenhar_retangulo_selecao(self, retangulo):

        self.obter_canvas().create_rectangle(
            retangulo.x1,
            retangulo.y1,
            retangulo.x2,
            retangulo.y2,
            outline="blue",
            fill="lightblue",
            stipple="gray25"
        )
            #ESSE STIPPLE FUNCIONA COMO UM PONTILHADO, E ESSE NUMERO É A % DE PONTILHADO
            #SIGNIFICA QUE É 25% PONTILHADO SENDO POSSIVEL VER ATRAVES DELE
        

    def iniciar(self):
        self.root.mainloop()
    
'''O método que estava aqui foi excluído. Pensando um pouco antes, vi que seria mais fácil fazer com que as próprias figuras
saibam se destacar do que criar um método aqui'''