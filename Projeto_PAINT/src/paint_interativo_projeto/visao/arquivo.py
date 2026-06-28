from tkinter import *
from tkinter import ttk, font, colorchooser

#importando as funções do controlador
from paint_interativo_projeto.controlador.arquivo import(
    iniciar_figura_nova,
    atualizar_figura_em_andamento,
    finalizar_figura, 
    figuras
)
#ESCOLHENDO A COR................

def escolher_cor_borda() :
    cor = colorchooser.askcolor(title='Escolha a cor da borda')
    if cor[1] :
        cor_borda_var.set(cor[1])

def escolher_cor_preenchimento() :
    cor = colorchooser.askcolor(title='Escolha a cor de preencimento')
    if cor[1] :
        cor_preenchimento_var.set(cor[1])



#CRIAÇÃO DE JANELA E BOTOÊS

root = Tk()
frame = Frame(root)
root.title('Paint em POO + Polígono') 

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
negrito = font.Font(family= 'Arial', size=10, weight='bold')

label = ttk.Label(frame, text='Formato:', font=negrito)
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu( #acrescentadas as outras opções de figuras definidas acima
    frame,
    tipo_figura_var,
    'Linha',
    'Linha',
    'Retangulo',
    'Oval',
    'Circulo',
    'Rabisco',
    'Poligono'
)
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=4, columnspan=3, sticky=W, **paddings) # modificação de onde o canvas está para acrescentar o botão de escolher espessura

frame.pack()

# Criação do widget de texto para a parte da borda
label_2 = ttk.Label(frame, text='Cor da borda:', font=negrito)
label_2.grid(column=0, row=1, sticky=W, **paddings)


# Criação do widgtet para selecionar a cor da borda
cor_borda_var = StringVar(root, value = 'black') # definição do valor default aqui

botao_borda = ttk.Button(frame, text="Escolher cor da borda", command=escolher_cor_borda) # implementação do botão para borda

botao_borda.grid(column=1, row=1, sticky=W, **paddings)


# Criação do widget de texto para o preenchimento das figuras
label_3 = ttk.Label(frame, text = 'Cor Preenchimento:', font=negrito)
label_3.grid(column=0, row=2, sticky=W, **paddings)


# Criação do widgtet para selecionar a cor do preenchimento
cor_preenchimento_var = StringVar(root, value = 'white') # definição do valor default aqui

botao_preenchimento = ttk.Button(frame, text="Escolher cor do preenchimento", command=escolher_cor_preenchimento) # implementação do botão para preenchimento

botao_preenchimento.grid(column=1, row=2, sticky=W, **paddings)

# Criação do label para a espessura da borda
label_4 = ttk.Label(frame, text = 'Espessura da Borda:', font=negrito)
label_4.grid(column=0, row=3, sticky=W, **paddings)

# Criação do widget para selecionar a espessura da borda
tamanho_borda = StringVar(root, value = '1')

option_menu_2 = ttk.OptionMenu( 
    frame,
    tamanho_borda,
    '1',
    '1',
    '2',
    '3',
    '4',
    '5'
)

option_menu_2.grid(column=1, row=3, sticky=W, **paddings)


def tratar_clique_inicial(event) :
    tipo = tipo_figura_var.get()
    cor_b = cor_borda_var.get()
    cor_p = cor_preenchimento_var.get()
    tam = tamanho_borda.get()

    #Passando os dados obtidos para o controlador
    figura = iniciar_figura_nova(tipo, event.x, event.y,
                               cor_b, cor_p, tam)

    #Atualizando tela

    desenhar_tudo()
    if figura :
        figura.desenhar(canvas)

def tratar_movimento(event) :
    tipo = tipo_figura_var.get()
    
    #Verificando se eh poligono ou se o mouse esta sendo precionado enquanto eh arrastado

    if tipo == 'Poligono' or (event.state & 0x0100) :
        figura = atualizar_figura_em_andamento(event.x, event.y)

        desenhar_tudo()
        if figura :
            figura.desenhar(canvas)

def tratar_fim_clique(event) :

    #Avisa que o controle que o usuário soltou o mouse

    finalizar_figura()
    desenhar_tudo()

def desenhar_tudo() :
    canvas.delete('all')
    for f in figuras :
        f.desenhar(canvas)

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', tratar_clique_inicial)
canvas.bind('<B1-Motion>', tratar_movimento)  
canvas.bind('<Motion>', tratar_movimento)     
canvas.bind('<ButtonRelease-1>', tratar_fim_clique)

'''EFIM A FUNÇÃO QUE IRA ATIVAR NOSSO SISTEMA, APARTIR DO ARQUIVO MAIN...'''

def iniciar_interface() :
    mainloop()
