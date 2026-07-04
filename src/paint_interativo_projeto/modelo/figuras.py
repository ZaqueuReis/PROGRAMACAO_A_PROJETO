from abc import ABC, abstractmethod


#CLASSE ABSTRATA FIGURA =====================
class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda

    @abstractmethod
    def desenhar(self, janela):
        pass
    
    @abstractmethod
    def atualizar(self, *args): 
        pass

    @abstractmethod
    def incompleta(self):
        pass
    
    
    @abstractmethod
    def transformar_figura_dicionario(self):
        pass
    
    '''
    UM ARQUIVO JSON NAO CONSEGUE ENTENDER O QUE É UM OBJETO EM PYTHON
    ELE NÃO LÊ UM OBJETO COMO UM OBJETO, ELE CONSEGUE LER APENAS OUTRAS
    MANEIRAS, E UMA DELAS É >>DICIONÁRIO<<, É PRECISO TRANSFORMAR TUDO
    EM DICIONARIO, ENTÃO PARA NÃO TER QUE MEXER EM TUDO E BAGUNÇAR O CÓDIGO
    A MELHOR OPÇÃO É CRIAR MÉTODO QUE TRANSFORMA OS DADOS DA FIGURA EM DICIONÁRIO
    '''
    
    
    


#CLASSE LINHA ==========================
class Linha(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, janela):
        janela.desenhar_linha(self.x1, self.y1, self.x2, self.y2, self.cor_borda, self.tamanho_borda)
    
    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2
    
    def transformar_figura_dicionario(self):
        return {
        "tipo": "Linha",
        "x1": self.x1,
        "y1": self.y1,
        "x2": self.x2,
        "y2": self.y2,
        "cor_borda": self.cor_borda,
        "tamanho_borda": self.tamanho_borda
    }
        


#CLASSE RABISCO ==========================
class Rabisco(Figura):

    def __init__(self, pontos, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.pontos = pontos

    def desenhar(self, janela):
        janela.desenhar_rabisco(self.pontos, self.cor_borda, self.tamanho_borda)

    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1
    
    def transformar_figura_dicionario(self):
        return{
            "tipo": "Rabisco",
            "pontos": self.pontos,
            "cor_borda": self.cor_borda,
            "tamanho_borda": self.tamanho_borda
        }

#CLASSE RETANGULO =============================
class Retangulo(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, janela):
        janela.desenhar_retangulo(self.x1, self.y1, self.x2, self.y2, self.cor_borda, self.cor_preenchimento, self.tamanho_borda)

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y

    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2
    
    
    def transformar_figura_dicionario(self):
        return {
            "tipo": "Retangulo",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamanho_borda": self.tamanho_borda
        }
        


#CLASSE OVAL ====================================
class Oval(Figura):

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, janela):
        janela.desenhar_oval(self.x1, self.y1, self.x2, self.y2, self.cor_borda, self.cor_preenchimento, self.tamanho_borda)

    def atualizar(self, x, y) :
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2
    
    def transformar_figura_dicionario(self):
        return {
            "tipo": "Oval",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamanho_borda": self.tamanho_borda
            
        }


#CLASSE CIRCULO =================================
class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio
    
    def desenhar(self, janela):
        janela.desenhar_circulo(self.centro_x, self.centro_y, self.raio, self.cor_borda, self.cor_preenchimento, self.tamanho_borda)
    
    def atualizar(self, x, y) :
        self.raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5 # substituição aqui, pois estava redundante

    def incompleta(self):
        return self.raio <= 0
    
    
    def transformar_figura_dicionario(self):
        return {
            "tipo": "Circulo",
            "centro_x": self.centro_x,
            "centro_y": self.centro_y,
            "raio": self.raio,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamanho_borda": self.tamanho_borda
            
        }


# CLASSE POLIGONO =====================================
class Poligono(Figura):
    #ALTERAÇÃO NA CLASSE POLIGONO, AGORA ELA ATUALIZA SE FECHARMOS O POLIGONO, E JA INICIA COMO FALSO CASO NAO FECHEMOS
    def __init__(self, pontos, cor_borda, cor_preenchimento, tamanho_borda, fechado=False):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.pontos = pontos
        self.fechado = fechado # Tirei o self.mouse pois está função é do controler

    def desenhar(self, janela):
        janela.desenhar_poligono(self.pontos, self.cor_borda, self.cor_preenchimento, self.tamanho_borda, self.fechado)

    def atualizar(self, x, y):
        """
        Mantido apenas para preservar a interface da classe Figura, já que o polígono 
        é atualizado adicionando novos vértices. Como foi sugerido por Giovanny em sala
        """
        pass

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    # Função desenhar tirada, pois está no view

    def fechar(self): # Tirado canvas porque ele está na view
        self.fechado = True
        # Tirado o movimento de rastreio do mouse, pois é função do controler

    def incompleta(self):
        return len(self.pontos) < 3
    
    def transformar_figura_dicionario(self):
        return {
            "tipo": "Poligono",
            "pontos": self.pontos,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamanho_borda": self.tamanho_borda,
            "fechado": self.fechado
            
        }
        