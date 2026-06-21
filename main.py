from tkinter import *
from tkinter import ttk, font # importar a fonte diferente da letra nativa do tkinter
from tkinter import colorchooser # importar espaço de selção de cor nativo do tkinter
from figuras import * # importar as classes do arquivo figuras.py

# Associa as strings do OptionMenu diretamente as classes de figuras.py
dict_figuras_nova = {'Oval' : Oval,
                     'Circulo' : Circulo,
                     'Retangulo' : Retangulo,
                     'Rabisco' : Rabisco,
                     'Poligono' : Poligono,
                     'Linha' : Linha}

#Quando o mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    tipo = tipo_figura_var.get()
    cls_figura = dict_figuras_nova.get(tipo)

    # Trava de segurança para evitar erros caso nenhum tipo válido esteja selecionado, bom se quisermos ampliar a quantidade de tipos de figura no futuro.
    if not cls_figura:
        return

    if tipo == 'Poligono':
        if figura_nova is None:
            # Primeiro ponto do polígono
            figura_nova = cls_figura([(event.x, event.y)],
                                     cor_borda_var.get(),
                                     cor_preenchimento_var.get(),
                                     int(tamanho_borda.get()))
        else:
            ''' Irei entitular essa parte como mecânica de fechamento semelhante a um imã. 
            Se você largar dois imãs próximos, ele irão se juntar. O mesmo acontece quando o vértice inicial e final ficam próximos no polígono. Legal né?'''
            
            # Calcula a distância geométrica (Pitágoras) entre o clique atual e o ponto inicial.
            p_inicio_x, p_inicio_y = figura_nova.pontos[0]
            distancia = ((event.x - p_inicio_x)**2 + (event.y - p_inicio_y)**2)**0.5
            
            if distancia < 10 and len(figura_nova.pontos) >= 2:
                # Fecha o polígono se deixou o vértice final perto do inicial (para isso o polígono deve ter o mínimo de 3 vértices no total, porque o menor polígono é um triangulo obviamente)
                figura_nova.fechar(canvas)
                figuras.append(figura_nova)
                figura_nova = None
            else:
                # Caso contrário, apenas adiciona o ponto normalmente
                figura_nova.adicionar_ponto(event.x, event.y)

        desenhar_figuras()
        if figura_nova:
            figura_nova.desenhar(canvas)
        return
        
    # Criação das outras figuras normais
    if tipo in ['Oval', 'Retangulo']:
        figura_nova = cls_figura(event.x, event.y, event.x, event.y,
                                 cor_borda_var.get(), 
                                 cor_preenchimento_var.get(),
                                 int(tamanho_borda.get()))
        
    elif tipo == 'Linha': 
        figura_nova = cls_figura(event.x, event.y, event.x, event.y,
                                 cor_borda_var.get(), 
                                 int(tamanho_borda.get()))
            
    elif tipo == 'Rabisco':
        figura_nova = cls_figura([(event.x, event.y)],
                                 cor_borda_var.get(), 
                                 int(tamanho_borda.get()))
        
    elif tipo == 'Circulo':
        figura_nova = cls_figura(event.x, event.y, 0, 
                                 cor_borda_var.get(),
                                 cor_preenchimento_var.get(),
                                 int(tamanho_borda.get()))
            
# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    
    if figura_nova:
        if isinstance(figura_nova, Poligono):
            # Polígono: atualiza com o movimento livre do mouse (botão solto)
            figura_nova.atualizar(event.x, event.y)
            desenhar_figuras()
            figura_nova.desenhar(canvas)
        else:
            # Outras figuras: só atualiza se o botão 1 estiver pressionado (arrastando)
            if event.state & 0x0100: # ao ver o manual do tkinter, descobri isso. Essa verificação de estado mostra se botão esquerdo do mouse estava pressionado no momento em que o evento de movimento aconteceu.
                figura_nova.atualizar(event.x, event.y)
                desenhar_figuras()
                figura_nova.desenhar(canvas)

# Quando mouse é solto

def incluir_figura_nova(event):
    global figura_nova

    # Como se fosse uma trava de segurança, pois polígonos não devem ser incluídos ou resetados aqui
    if figura_nova and not isinstance(figura_nova, Poligono):
        if not figura_nova.incompleta():
            figuras.append(figura_nova)
        figura_nova = None 
        desenhar_figuras()

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

'''------------------------------------------------------------------------------'''

#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)
root.title('Paint em POO + Polígono') # adicionado título a janela principal, para ficar visualmente bonito

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

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)  # Arrastar para Retângulo, Círculo, etc
canvas.bind('<Motion>', atualizar_figura_nova)     # Movimento livre para a linha guia do Polígono
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
