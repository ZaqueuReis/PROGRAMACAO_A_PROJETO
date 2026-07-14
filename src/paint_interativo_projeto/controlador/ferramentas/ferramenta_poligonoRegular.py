from modelo.figuras import PoligonoRegular
from .ferramenta import Ferramenta

'''Classe responsável por controlar toda a interação do usuário com a ferramenta
de desenho do PoligonoRegular. Cada método representa um evento do mouse durante
a criação da figura (pressionar, mover e soltar o botão).'''

class FerramentaPoligonoRegular(Ferramenta) :
    def __init__(self, controlador) :
        super().__init__(controlador)
    
    def mouse_press(self, event) :
        desenho = self.controlador.desenho
        janela = self.controlador.janela
        figura = desenho.obter_figura_atual()
        
        #Verificando se a alguma figura sendo feita
        if figura is not None and not isinstance(figura, PoligonoRegular) :
            figura = None

        #Estado inicial -> poligono irregular ainda não foi criado

        if figura is None :
            #Garantido que eh o botão esquerdo que está sendo pressionado
            if getattr(event, 'num', 1) == 1 :
                lados = 3
                figura = PoligonoRegular(
                event.x, event.y,
                lados,
                janela.obter_cor_borda(),
                janela.obter_cor_preenchimento(),
                janela.obter_tamanho_borda()

            )
            desenho.inicializar_figura_atual(figura)
            self.controlador.desenhar_figuras()

        #Estado intermediáio -> a figura já existe
        else :
            #Botão 1 = Esquerdo(Aumenta o número de lados); Botão 3 = Direito(Diminuí o número...)
            if getattr(event, 'num', 1) == 1 :
                shift_pressionado = (event.state & 0x0001) != 0
                if shift_pressionado :
                    figura.diminuir_lados()

                else :
                    figura.aumentar_lados()
        self.controlador.desenhar_figuras()


    def mouse_move(self, event) :
        figura = self.controlador.desenho.obter_figura_atual()
        
        #Verificando se ah figuras sendo desenhadas
        if figura is None :
            return

        figura.atualizar(event.x, event.y) 
        self.controlador.desenhar_figuras()

    def mouse_double_click(self, event) :
        desenho = self.controlador.desenho
        figura = desenho.obter_figura_atual()

        if figura is not None :
            desenho.adicionar_figura_concluida()
            self.controlador.desenhar_figuras()

    def mouse_release(self, event):
        pass