import pickle # Substituição pela biblioteca vista em aula hoje

class Desenho :
    
    def __init__(self) :
        self.figuras = []
        self.figura_atual = None
        self.figura_selecionada = None # Adicionado atributo para verificar se uma figura está selecionada

    # ========= Para figuras em construção no momento do desenho ==========

    def inicializar_figura_atual(self, figura) :
        self.figura_atual = figura
    
    def obter_figura_atual(self) :
        return self.figura_atual
    
    # ========== Para permitir a seleção de figuras com o mouse ===========
    
    def obter_figura_selecionada(self):
        return self.figura_selecionada

    def definir_figura_selecionada(self, figura):
        self.figura_selecionada = figura

    def limpar_selecao(self):
        self.figura_selecionada = None
        
        
    #DELETAR FIGURAS SELECIONADAS =======================
    
    def deletar_selecionada(self):
        if self.figura_selecionada:
            self.figuras.remove(self.figura_selecionada)
            figura_apagada = self.figura_selecionada
            self.figura_selecionada = None
            return figura_apagada
        return None
    
    #FIM DESSA SEÇÃO DE DELETAR FIGURAS SELECIONADAS==========
    
    # ========= Para as figuras que estão na lista self.figuras ===========

    def adicionar_figura_concluida(self) :
        if self.figura_atual :
            self.figuras.append(self.figura_atual)
            self.figura_atual = None

    # A partir desta função 'obter' o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras
    
     # ========= Para salvar, abrir e limpar os desenho contidos na lista em um arquivo ===========
    def salvar_desenhos(self, caminho):
        with open(caminho, "wb") as arquivo:
            pickle.dump(self.figuras, arquivo)  

    def abrir_arquivo_desenho(self, caminho):
        with open(caminho, "rb") as arquivo:
            self.figuras = pickle.load(arquivo)
    
    def limpar_desenhos(self):
        if not self.figuras:
            return False

        self.figuras = []
        self.figura_atual = None
        return True
    
    '''Aqui, foram substituídos aqueles métodos complicados e trabalhosos do JSON. Agora, foram implementados os métodos conforme 
    os moldes do pickle (visto em aula hoje). Acredito que isso trará uma melhoria significativa no tamanho do código e na 
    simplificação do projeto'''
    