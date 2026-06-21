from tkinter import *
from tkinter import ttk, font # importar a fonte diferente da letra
from tkinter import colorchooser # importar espaço de selção de cor
from figuras import *

# Quando mouse é pressionado
dict_figuras_nova = {'Oval' : Oval,
                     'Circulo' : Circulo,
                     'Retangulo' : Retangulo,
                     'Rabisco' : Rabisco,
                     'Poligono' : Poligono,
                     'Linha' : Linha}

#Quando o mouse eh pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    tipo = tipo_figura_var.get()
    cls_figura = dict_figuras_nova.get(tipo)

    if cls_figura :
        if tipo in ['Oval', 'Retangulo', 'Linha'] :
            figura_nova = cls_figura(event.x, event.y, event.x, event.y,
                                     cor_borda_var.get(), 
                                     cor_preenchimento_var.get(),
                                     tamanho_borda.get()
                                     )
        elif tipo == 'Rabisco' :
            figura_nova = cls_figura([(event.x, event.y)],
                                     cor_borda_var.get(), 
                                     tamanho_borda.get()
                                     )
        
        elif tipo == 'Circulo' :
            figura_nova = cls_figura(event.x, event.y, 0, 
                                     cor_borda_var.get(),
                                     cor_preenchimento_var.get(),
                                     tamanho_borda.get()
                                     )
        else :
            figura_nova = cls_figura([(event.x, event.y, event.x, event.y)],
                                     cor_borda_var.get(),
                                     cor_preenchimento_var.get(),
                                     tamanho_borda.get()
                                     )
# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event) :
    global figura_nova

    if figura_nova :
        figura_nova.atualizar(event.x, event.y)
        desenhar_figuras()
        figura_nova.desenhar(canvas)


# Quando mouse é solto



def incluir_figura_nova(event): 
    if figura_nova and not figura_nova.incompleta() :
        figuras.append(figura_nova)
    desenhar_figuras()

def incompleta(figura): 
    return figura.incompelta()

def desenhar_figuras() :
    canvas.delete('all')
    for figura in figuras :
        figura.desenhar(canvas)

def desenhar_figura_nova():
    if figura_nova :
        figura_nova.desenhar(canvas)

'''------------------------------------------------------------------------------'''

def escolher_cor_borda():
    cor = colorchooser.askcolor(title="Escolha a cor da borda")
    if cor[1]:
        cor_borda_var.set(cor[1])


def escolher_cor_preenchimento():
    cor = colorchooser.askcolor(title="Escolha a cor de preenchimento")
    if cor[1]:
        cor_preenchimento_var.set(cor[1])

'''Funções para colocar em funcionamento o método de selecão de cor arbitrária importada pelo tkinter'''


#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)
root.title('Paint Imperativo') # adicionado título a janela principal, para ficar visualmente bonito

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
    'Rabisco'
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

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
