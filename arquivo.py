from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y)) 
        
    elif tipo_figura_var.get() == 'Oval': # adicionada a figura oval
        figura_nova = ("oval", (event.x, event.y, event.x, event.y))

    elif tipo_figura_var.get() == 'Circulo': #adicionada a figura circulo
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y))
        
    elif tipo_figura_var.get() == 'Retangulo' : #adicionada a figura retangulo
        figura_nova = ('retangulo', (event.x, event.y, event.x, event.y))
        
    else :
        figura_nova = ("rabisco", [(event.x, event.y)])

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    
    global figura_nova
    
    tipo, valores = figura_nova # substituição para evitar o uso de indices em excesso no codigo abaixo

    if tipo == "rabisco":
        valores.append((event.x, event.y))
        figura_nova = (tipo, valores)
        
    elif tipo == 'circulo': #adicionado forma de armazenar coordenadas do circulo
        x1 = valores[0]
        y1 = valores[1]
        lado = event.x - x1  

        figura_nova = (tipo, (x1, y1, x1 + lado, y1 + lado))
    
    else:
        figura_nova = (tipo, (valores[0], valores[1], event.x, event.y))

    desenhar_figuras()
    desenhar_figura_nova()

    """Como são vários casos de figuras e, com exceção do rabisco e circulo, todas as outras recaem no mesmo caso, é melhor organizar
a função apenas para verificar se é rabisco ou circulo. Se for, já verifica e executa o trecho de código destinado a ela. Caso não seja, 
recai no mesmo caso para todas as outras figuras"""

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3])
        elif fig == "oval": #criado para desenhar ovais passadas
            canvas.create_oval(values[0], values[1], values[2], values[3])
        elif fig == 'retangulo' : #criado para desenhar retangulos passados
            canvas.create_rectangle(values[0], values[1], values[2], values[3])
        elif fig == 'circulo' : #criado para desenhar circulos passados
            canvas.create_oval(values[0], values[1], values[2], values[3])
        else : # fig == "rabisco"
            canvas.create_line(values)

def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "oval": #criado para desenhar oval novo
        canvas.create_oval(values[0], values[1], values[2], values[3], dash =(4, 2))
    elif fig == 'circulo': #criado para desenhar circulo novo, usando o mesmo metodo que oval
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4,2))
    elif fig == 'retangulo' : #criado para desenhar retangulo novo
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2))
    else : # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

def incompleta(figura): 
    fig, values = figura
    
    if fig == "rabisco":
        return len(values) <= 1

    return (values[0] == values[2] and values[1] == values[3])

"""Como existem vários casos de figuras e, com exceção do rabisco, todas as outras exigem que o código faça a mesma coisa, é melhor organizar
a função apenas para verificar se é rabisco ou não. Se for, já verifica. Caso não seja, recai no mesmo caso para todas as outras
figuras """




#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)
root.title('Paint Imperativo') # adicionado título a janela principal, para ficar visualmente bonito

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame, text='Formato da Figura:')
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
canvas.grid(column=0, row=2, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
