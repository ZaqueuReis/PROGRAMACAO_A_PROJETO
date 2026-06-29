from abc import ABC, abstractmethod


#CLASSE ABSTRATA FIGURA =====================
class Figura(ABC):

    def __init__(self, cor_borda, cor_preenchimento, tamanho_borda):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.tamanho_borda = tamanho_borda
    
    @abstractmethod
    def desenhar(self,canvas):
        pass

    @abstractmethod
    def incompleta(self):
        pass


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
    
    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill = self.cor_borda, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


#CLASSE RABISCO ==========================
class Rabisco(Figura):

    def __init__(self, pontos, cor_borda, tamanho_borda):
        super().__init__(cor_borda, '', tamanho_borda)
        self.pontos = pontos
    
    def atualizar(self, x, y) :
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill = self.cor_borda, width = self.tamanho_borda)
    
    def incompleta(self):
        return len(self.pontos) <= 1

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

    def desenhar(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill = self.cor_preenchimento, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


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

    def desenhar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill = self.cor_preenchimento, width = self.tamanho_borda)
    
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2


#CLASSE CIRCULO =================================
class Circulo(Figura):

    def __init__(self, centro_x, centro_y, raio, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.raio = raio
    
    def atualizar(self, x, y) :
        raio = ((x- self.centro_x) ** 2 + (y - self.centro_y) ** 2) ** 0.5
        self.raio = raio

    def desenhar(self, canvas):
        canvas.create_oval(self.centro_x - self.raio, self.centro_y - self.raio, self.centro_x + self.raio, self.centro_y + self.raio, outline=self.cor_borda, fill=self.cor_preenchimento, width = self.tamanho_borda)

    def incompleta(self):
        return self.raio <= 0



#CLASSE POLIGONO FINAL BOSS =====================================
class Poligono(Figura):

    def __init__(self, pontos, cor_borda, cor_preenchimento, tamanho_borda):
        super().__init__(cor_borda, cor_preenchimento, tamanho_borda)
        self.pontos = pontos
        self.mouse_x = None  # Rastreia o movimento livre do mouse
        self.mouse_y = None # Rastreia o movimento livre do mouse
        self.fechado = False # Rastreia se o polígono foi concluído

    def atualizar(self, x, y):
        # Atualiza a posição da linha guia enquanto o usuário move o mouse
        self.mouse_x = x
        self.mouse_y = y

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas):
        if len(self.pontos) < 1:
            return

        coordenadas = []
        for x, y in self.pontos:
            coordenadas.extend([x, y])

        # Se o polígono foi finalizado, desenha preenchido
        if self.fechado:
            if len(self.pontos) >= 3:
                canvas.create_polygon(coordenadas, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.tamanho_borda)
            return

        # Enquanto desenha, mostra os segmentos já desenhados no Canvas
        if len(self.pontos) >= 2:
            canvas.create_line(coordenadas, fill=self.cor_borda, width=self.tamanho_borda)

        # Vai mostrando na tela a linha guia dinâmica conforme vontade do usuário
        if self.mouse_x is not None and not self.fechado:
            ultimo_x, ultimo_y = self.pontos[-1]
            canvas.create_line(ultimo_x, ultimo_y, self.mouse_x, self.mouse_y, fill=self.cor_borda, width=self.tamanho_borda, dash=(4, 4))
            
            # Se o mouse estiver perto do ponto inicial, desenha uma caixinha vermelha para dizer aos usuários que está perto de fechar o polígono
            p_inicio_x, p_inicio_y = self.pontos[0]
            distancia = ((self.mouse_x - p_inicio_x)**2 + (self.mouse_y - p_inicio_y)**2)**0.5
            if distancia < 10 and len(self.pontos) >= 2: # 10 pixels de tolerância
                canvas.create_rectangle(p_inicio_x - 5, p_inicio_y - 5, p_inicio_x + 5, p_inicio_y + 5, outline="red", fill="white")

    def fechar(self, canvas):
        self.fechado = True
        self.mouse_x = None
        self.mouse_y = None

    def incompleta(self):
        return len(self.pontos) < 3
    
   