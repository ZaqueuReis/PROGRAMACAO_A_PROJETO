from tkinter import *
from tkinter import ttk, font # importar a fonte diferente da letra
from tkinter import colorchooser # importar espaço de selção de cor

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_borda_var.get(), cor_preenchimento_var.get()) 
        
    elif tipo_figura_var.get() == 'Oval': # adicionada a figura oval
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_borda_var.get(), cor_preenchimento_var.get())

    elif tipo_figura_var.get() == 'Circulo': #adicionada a figura circulo
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y, event.x, event.y), cor_borda_var.get(), cor_preenchimento_var.get())
        
    elif tipo_figura_var.get() == 'Retangulo' : #adicionada a figura retangulo
        figura_nova = ('retangulo', (event.x, event.y, event.x, event.y), cor_borda_var.get(), cor_preenchimento_var.get())
        
    else :
        figura_nova = ("rabisco", [(event.x, event.y)], cor_borda_var.get(), cor_preenchimento_var.get())

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    
    global figura_nova
    
    tipo, valores, borda, preenchimento = figura_nova # substituição para evitar o uso de indices em excesso no codigo abaixo

    if tipo == "rabisco": # seguir exatamente o que é pedido no colab
        valores.append((event.x, event.y))
        figura_nova = (tipo, valores, borda, preenchimento)
        
    elif tipo == 'circulo': #correção da forma de calcular círculo

        centro_x = valores[4]
        centro_y = valores[5]
        raio = ((event.x - centro_x) ** 2 + (event.y - centro_y) ** 2) ** 0.5

        figura_nova = (tipo, (centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio, centro_x, centro_y), borda, preenchimento)
    
    else:
        figura_nova = (tipo, (valores[0], valores[1], event.x, event.y), borda, preenchimento)

    desenhar_figuras()
    desenhar_figura_nova()

    """Como são vários casos de figuras e, com exceção do rabisco e circulo, todas as outras recaem no mesmo caso, é melhor organizar
a função apenas para verificar se é rabisco ou circulo. Se for, já verifica e executa o trecho de código destinado a ela. Caso não seja, 
recai no mesmo caso para todas as outras figuras"""

# Quando mouse é solto
'''Defini uma variavel global para definir o tamnaho da borda padrão para as figuras'''
tamanho_borda = 2

def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, borda, preenchimento in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill = borda, width=tamanho_borda) # alterei para fill = borda pois quando iniciava o programa a linha ficava invisivel
        elif fig == "oval": #criado para desenhar ovais passadas
            canvas.create_oval(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda)
        elif fig == 'retangulo' : #criado para desenhar retangulos passados
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda)
        elif fig == 'circulo' : #criado para desenhar circulos passados
            canvas.create_oval(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda)
        else : # fig == "rabisco"
            canvas.create_line(values, fill = borda, width=tamanho_borda) # altereii para fill = borda pois quando iniciava o programa a linha ficava invisivel

def desenhar_figura_nova():
    fig, values, borda, preenchimento = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], fill = borda, width=tamanho_borda, dash=(4, 2)) # alterei para fill = borda pois quando iniciava o programa a linha ficava invisivel
    elif fig == "oval": #criado para desenhar oval 
        canvas.create_oval(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda, dash =(4, 2))
    elif fig == 'circulo': #criado para desenhar retangulo novo
        canvas.create_oval(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda, dash=(4,2))
    elif fig == 'retangulo' : #criado para desenhar circulo novo
        canvas.create_rectangle(values[0], values[1], values[2], values[3], outline = borda, fill = preenchimento, width=tamanho_borda, dash=(4, 2))
    else : # fig == "rabisco"
        canvas.create_line(values, fill = borda, width=tamanho_borda, dash=(4, 2)) # alterei para fill = borda pois quando iniciava o programa a linha ficava invisivel

def incompleta(figura): 
    fig, values, borda, preenchimento = figura
    
    if fig == "rabisco":
        return len(values) <= 1

    return (values[0] == values[2] and values[1] == values[3])

"""Como existem vários casos de figuras e, com exceção do rabisco, todas as outras exigem que o código faça a mesma coisa, é melhor organizar
a função apenas para verificar se é rabisco ou não. Se for, já verifica. Caso não seja, recai no mesmo caso para todas as outras
figuras """

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
tamanho_borda = StringVar(root, value = "1")

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
