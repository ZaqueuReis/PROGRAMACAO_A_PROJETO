class Desenho :
    def __init__(self) :
        self.figuras = []
        self.figura_atual = None

    def adicionar_figura_concluida(self) :
        if self.figura_atual :
            self.figuras.append(self.figura_atual)
            self.figura_atual = None

    def inicializar_figura_atual(self, figura) :
        self.figura_atual = figura


    #Apartir desta função obter o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras

    def obter_figura_atual(self) :
        return self.figura_atual
    
    '''Sinceramente, acredito eu que, usar o padrão MVC, ajuda não so nós que estamos
    desenvolvendo, a enteder precisamente o código, como também outras pessoas que
    não participou do desenvolvimento, gostei de mais disso, apesar que da um pouco
    de trabalho também, mas nada vem de graça...'''