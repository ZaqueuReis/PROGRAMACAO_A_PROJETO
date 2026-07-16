from abc import ABC, abstractmethod
from modelo.calcular_distancia_fornecido import distancia # Importação do arquivo fornecido por Giovanny
import math
from copy import deepcopy # Importei para permir copiar figuras compostas

#CLASSE ABSTRATA FIGURA =====================
class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda

    @abstractmethod
    def atualizar(self, *args): 
        pass

    @abstractmethod
    def incompleta(self):
        pass

    @abstractmethod
    def mover(self, dx, dy):
        pass

    @abstractmethod
    def contem(self, x, y):
        pass  
    
    def alterar_cor_borda(self, cor):
        self.cor_borda = cor

    def alterar_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor

    def alterar_tamanho_borda(self, tamanho):
        self.tamanho_borda = tamanho

    # Métodos responsáveis por alterar as propriedades visuais da figura.
    # O controlador apenas solicita a alteração, sem acessar diretamente
    # os atributos internos da classe (encapsulamento).


#CLASSE LINHA ==========================
class Linha(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem(self, x, y):
        return distancia(self.x1, self.y1, self.x2, self.y2, x, y) <= 5 # Onde o 5 é a tolerância para a linha, como visto em sala
    
#CLASSE RABISCO ==========================
class Rabisco(Figura):

    def __init__(self, pontos, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.pontos = pontos

    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1
    
    def mover(self, dx, dy):
        for i in range(len(self.pontos)):
            x, y = self.pontos[i]
            self.pontos[i] = (x + dx, y + dy)

    def contem(self, x, y):
        for i in range(len(self.pontos)-1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i+1]

            if distancia(x1, y1, x2, y2, x, y) <= 5:
                return True
            
        return False
    
    '''Como o rabisco é um conjunto de linhas, então foi adaptado o metodo usado em linha para este caso'''


#CLASSE RETANGULO =============================
class Retangulo(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem(self, x, y):
        menor_x = min(self.x1, self.x2)
        maior_x = max(self.x1, self.x2)
        menor_y = min(self.y1, self.y2)
        maior_y = max(self.y1, self.y2)

        return menor_x <= x <= maior_x and menor_y <= y <= maior_y

    # Tava dando bug por causa da ordem, já consertei


#CLASSE OVAL ====================================
class Oval(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem(self, x, y):
        centro_x = (self.x1 + self.x2) / 2
        centro_y = (self.y1 + self.y2) / 2

        raio_x = abs(self.x2 - self.x1) / 2
        raio_y = abs(self.y2 - self.y1) / 2

        if raio_x == 0 or raio_y == 0:
            return False

        return (((x - centro_x) / raio_x) ** 2 + ((y - centro_y) / raio_y) ** 2) <= 1




#CLASSE CIRCULO =================================
class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio

    def atualizar(self, x, y) :
        self.raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5 # substituição aqui, pois estava redundante

    def incompleta(self):
        return self.raio <= 0

    def mover(self, dx, dy):
        self.centro_x += dx
        self.centro_y += dy

    def contem(self, x, y):
        distancia = ((x - self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5
        return distancia <= self.raio


# CLASSE POLIGONO_IRREGULAR=====================================
class Poligono_irregular(Figura):
    def __init__(self, pontos, cor_borda, cor_preenchimento, tamanho_borda, fechado=False):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.pontos = pontos
        self.fechado = fechado 

    def atualizar(self, x, y):
        """
        Mantido apenas para preservar a interface da classe Figura, já que o polígono 
        é atualizado adicionando novos vértices. Como foi sugerido por Giovanny em sala
        """
        pass

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))


    def fechar(self): # Tirado canvas porque ele está na view
        self.fechado = True
        # Tirado o movimento de rastreio do mouse, pois é função do controler

    def incompleta(self):
        return len(self.pontos) < 3

    def mover(self, dx, dy):
        for i in range(len(self.pontos)):
            x, y = self.pontos[i]
            self.pontos[i] = (x + dx, y + dy)

    def contem(self, x, y):
        """
        Verifica se o ponto (x, y) está dentro de um polígono.
        O polígono está especificado na lista de tuplas self.pontos: [(x1, y1), (x2, y2), ...].
        """
        dentro = False
        n = len(self.pontos)

        # Se o polígono não tiver pelo menos 3 vértices, não é um polígono válido
        if n < 3:
            return False

        # Inicializa o último vértice do polígono como ponto de partida
        p1x, p1y = self.pontos[0]

        for i in range(n + 1):
            # Avança para o próximo vértice
            p2x, p2y = self.pontos[i % n]

            # Verifica se o raio horizontal intercepta a aresta do polígono
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Calcula a interceptação X exata da aresta
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Se o ponto estiver à esquerda da interceptação, inverte o estado
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

'''Tive que fazer uma breve alteração nesta função, dado que ao invés de copiar, ela apenas movia o poligono,
 isso porque, pelo que entendi, estavamos usando a mesma lista de pontos, da figura original, para copiar e 
 depois colar, dai na hora de colar, ela apenas somava aquele deslocamento na coordenada da figura original,
 o segredo eh fazer uma cópia da figura, para deixar a orignal na sua posicão inicial, sem deslocar a mesma, 
 observei que rabisco, estava com o mesmo bug, daí a solução foi a mesma...'''


# CLASSE POLIGONO REGULARES =====================================
class Poligono_regular(Figura) :
    def __init__(self, centro_x, centro_y, lados, cor_borda, cor_preenchimento, tamanho_borda, fechado=True):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.lados = lados
        self.raio = 0
        self.pontos = [] 
        
        #Um poligono regular eh sempre fechado, talvez não seja necessário manter isto aqui
        self.fechado = fechado 

    def atualizar(self, x, y):
        self.pontos = []

        '''A figura precisa saber se redesenhar, caso o usuáio altere a quantidade de lados durante a sua constr-
        ução'''

        self.ultimo_x = x
        self.ultimo_y = y 
        
        self.raio = math.hypot(x - self.centro_x, y - self.centro_y)

        if self.raio == 0 :
            return
        
        angulo_inicial = math.atan2(y - self.centro_y, x - self.centro_x)
        
        # 4. Calcula o tamanho do ângulo entre um vértice e outro
        passo_angulo = (2 * math.pi) / self.lados
        
        # 5. Calcula as coordenadas (X, Y) de cada vértice
        for i in range(self.lados):
            angulo_atual = angulo_inicial + (i * passo_angulo)
            
            # Fórmulas trigonométricas para encontrar um ponto na circunferência
            ponto_x = self.centro_x + self.raio * math.cos(angulo_atual)
            ponto_y = self.centro_y + self.raio * math.sin(angulo_atual)

            self.pontos.append((ponto_x, ponto_y))

    
    def aumentar_lados(self) :
        self.lados += 1
        self.atualizar(self.ultimo_x, self.ultimo_y)

    def diminuir_lados(self) :
        if self.lados > 3 :
            self.lados -= 1
            self.atualizar(self.ultimo_x, self.ultimo_y)

    def incompleta(self) :
        #Na real, isso não eh necessário, porém, deixei aqui...
        return self.raio == 0

    def mover(self, dx, dy):
        self.centro_x += dx
        self.centro_y += dy
        self.atualizar(self.ultimo_x + dx, self.ultimo_y + dy)
    
    #Ainda bem que o método contém, de poligono irregular serve perfeitamente aqui
    def contem(self, x, y):
        """
        Verifica se o ponto (x, y) está dentro de um polígono.
        O polígono está especificado na lista de tuplas self.pontos: [(x1, y1), (x2, y2), ...].
        """
        dentro = False
        n = len(self.pontos)

        # Se o polígono não tiver pelo menos 3 vértices, não é um polígono válido
        if n < 3:
            return False

        # Inicializa o último vértice do polígono como ponto de partida
        p1x, p1y = self.pontos[0]

        for i in range(n + 1):
            # Avança para o próximo vértice
            p2x, p2y = self.pontos[i % n]

            # Verifica se o raio horizontal intercepta a aresta do polígono
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Calcula a interceptação X exata da aresta
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Se o ponto estiver à esquerda da interceptação, inverte o estado
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

# CLASSE FIGURAS COMPOSTAS ======================

class FiguraComposta(Figura):

    def __init__(self, figuras):
        super().__init__("", "", 1)
        self.figuras = figuras

    def atualizar(self, *args):
        for figura in self.figuras:
            figura.atualizar(*args)

    def incompleta(self):
        return False

    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)

    def contem(self, x, y):
        for figura in self.figuras:
            if figura.contem(x, y):
                return True
        return False

    def copiar(self):
        return deepcopy(self)
    
    def alterar_cor_borda(self, cor):
        for figura in self.figuras:
            figura.alterar_cor_borda(cor)

    def alterar_cor_preenchimento(self, cor):
        for figura in self.figuras:
            figura.alterar_cor_preenchimento(cor)

    def alterar_tamanho_borda(self, tamanho):
        for figura in self.figuras:
            figura.alterar_tamanho_borda(tamanho)

'''
POR QUE FOI PRECISO IMPLEMENTAR ESSES MÉTODOS NA FIGURA COMPOSTA?
A FIGURA COMPOSTA NAO PODE SIMPLESMENTE FAZER 
SELF.COR_BORDA = COR

PORQUE A FIGURA COMPOSTA NAO É UM DESENHO PRÓPRIO, ELA SAO VÁRIAS FIGURAS.
POR ISSO É PRECISO PERCORRER TODAS DO GRUPO PARA ALTERAR TUDO, ISSO RESOLVE
O BUG DE FIGURAS COMPOSTAS QUE NAO ALTERAVAM COR DE BORDA, PREENCHIMENTO E ESPESSURA.

NOVAMENTE NAO FOI IMPLEMENTADO COMO MÉTODO ABSTRATO PORQUE TODOS OS OUTROS 
TERIAM QUE TER O METODO, E COMO SAO FIGURAS PROPRIAS CONSEGUEM SE SETAR SEUS ATRIBUTOS.

'''
