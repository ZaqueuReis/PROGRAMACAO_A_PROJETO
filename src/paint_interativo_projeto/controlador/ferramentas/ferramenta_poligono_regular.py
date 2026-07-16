from modelo.figuras import Poligono_regular
from .ferramenta import Ferramenta

'''Classe responsável por controlar toda a interação do usuário com a ferramenta
de desenho do PoligonoRegular. Cada método representa um evento do mouse durante
a criação da figura (pressionar, mover e soltar o botão).'''

class FerramentaPoligonoRegular(Ferramenta) :
    def __init__(self, controlador) :
        super().__init__(controlador)
    
    def mouse_press(self, event) :
        botao = event.num # Adaptação para reformular metodo de desenhar poligono regular
        desenho = self.controlador.desenho
        janela = self.controlador.janela
        figura = desenho.obter_figura_atual()
        
        #Verificando se a alguma figura sendo feita
        if figura is not None and not isinstance(figura, Poligono_regular) :
            figura = None

        #Estado inicial -> poligono regular ainda não foi criado

        if figura is None :
            #Garantido que eh o botão esquerdo que está sendo pressionado
            if botao == 1:
                lados = 3
                figura = Poligono_regular(
                event.x, event.y,
                lados,
                janela.obter_cor_borda(),
                janela.obter_cor_preenchimento(),
                janela.obter_tamanho_borda()

            )
            desenho.inicializar_figura_atual(figura)

        #Estado intermediáio -> a figura já existe
        else :
            #Botão 1 = Esquerdo(Aumenta o número de lados); Botão 3 = Direito(Diminuí o número...)
            if botao == 1:
                figura.aumentar_lados()

            elif botao == 3:
                figura.diminuir_lados()

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