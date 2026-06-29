
from modelo.Figura import Figura


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
                canvas.create_polygon(coordenadas, 
                                      outline=self.cor_borda, 
                                      fill=self.cor_preenchimento, 
                                      width=self.tamanho_borda)
            return

        # Enquanto desenha, mostra os segmentos já desenhados no Canvas
        if len(self.pontos) >= 2:
            canvas.create_line(coordenadas, 
                               fill=self.cor_borda, 
                               width=self.tamanho_borda)

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