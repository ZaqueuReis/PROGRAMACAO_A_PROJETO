from paint_interativo_projeto.modelo.arquivo import *

dict_figuras_nova = {
    'Oval' : Oval,
    'Circulo' : Circulo,
    'Retangulo' : Retangulo,
    'Rabisco' : Rabisco,
    'Linha' : Linha,
    'Poligono' : Poligono
}

figuras = []
figura_nova = None

def iniciar_figura_nova(tipo, x, y, cor_borda, cor_preenchimento, tamanho) : 
    global figura_nova
    
    cls_figura = dict_figuras_nova.get(tipo)
    
    #Trava de segurança
     
    if not cls_figura :
        return None
    
    if tipo == 'Poligono' :
        
        if figura_nova is None:
            # Primeiro ponto do polígono
            figura_nova = cls_figura([(x,y)],
                                     cor_borda,
                                     cor_preenchimento,
                                     int(tamanho))
        else:
            # Calcula a distância geométrica (Pitágoras) entre o clique atual e o ponto inicial.
            p_inicio_x, p_inicio_y = figura_nova.pontos[0]
            distancia = ((x - p_inicio_x)**2 + (y - p_inicio_y)**2)**0.5
            
            if distancia < 10 and len(figura_nova.pontos) >= 2:
                '''Fecha o polígono se deixou o vértice final perto do inicial (para isso o polígono
                deve ter o mínimo de 3 vértices no total, porque o menor polígono é um triangulo obviamente)


                Mesmo que no modelo, 'fechar'exija o atributo canvas, ele nao faz nada com ele'''
                figura_nova.fechar(None)
                figuras.append(figura_nova)
                figura_nova = None
            else:
                # Caso contrário, apenas adiciona o ponto normalmente
                figura_nova.adicionar_ponto(x, y)

    elif tipo in ['Oval', 'Retangulo'] :
        figura_nova = cls_figura(x, y, x, y,
                                 cor_borda, cor_preenchimento, int(tamanho))
    elif tipo == 'Linha' :
        figura_nova = cls_figura(x, y, x, y,
                                 cor_borda, int(tamanho))
    elif tipo == 'Rabisco' :
        figura_nova = cls_figura([(x, y)],
                                 cor_borda, int(tamanho))
    elif tipo == 'Circulo' :
        figura_nova = cls_figura(x, y, 0,
                                  cor_borda, cor_preenchimento, int(tamanho))
    return figura_nova

def atualizar_figura_em_andamento(x, y) :
    global figura_nova

    '''Atualiza uma figura, se e somente se ela de fato existir'''

    if figura_nova :
        figura_nova.atualizar(x, y)
        return figura_nova
    else :
        return None

def finalizar_figura() :
    global figura_nova

    #Travamento extra para não finalizar o polígono antes do momento correto

    if figura_nova and not isinstance(figura_nova, Poligono) :
        if not figura_nova.incompleta() :
            figuras.append(figura_nova)
        figura_nova = None
