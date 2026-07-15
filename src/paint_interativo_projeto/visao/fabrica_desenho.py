from modelo.figuras import FiguraComposta # importando a classe figura composta


class FabricaDesenho:

    def __init__(self, janela):
        self.janela = janela

    def desenhar(self, figura, selecionada=False):

        if isinstance(figura, FiguraComposta):
            for figuras in figura.figuras:
                self.desenhar(figuras, selecionada)
            return

        largura = figura.tamanho_borda

        if selecionada:
            largura += 2

        if figura.__class__.__name__ == "Linha":
            self.janela.desenhar_linha(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, largura)

        elif figura.__class__.__name__ == "Retangulo":
            self.janela.desenhar_retangulo(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, figura.cor_preenchimento, largura)

        elif figura.__class__.__name__ == "Oval":
            self.janela.desenhar_oval(figura.x1, figura.y1, figura.x2, figura.y2, figura.cor_borda, figura.cor_preenchimento, largura)

        elif figura.__class__.__name__ == "Circulo":
            self.janela.desenhar_circulo(figura.centro_x, figura.centro_y, figura.raio, figura.cor_borda, figura.cor_preenchimento, largura)

        elif figura.__class__.__name__ == "Rabisco":
            self.janela.desenhar_rabisco(figura.pontos, figura.cor_borda, largura)

        elif figura.__class__.__name__ == "Poligono":
            self.janela.desenhar_poligono(figura.pontos, figura.cor_borda, figura.cor_preenchimento, largura, figura.fechado)

        elif figura.__class__.__name__ == "PoligonoRegular" :
            self.janela.desenhar_poligono_regular(figura.pontos, figura.cor_borda, figura.cor_preenchimento, largura, figura.fechado)