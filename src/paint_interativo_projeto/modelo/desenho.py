import pickle # Substituição pela biblioteca vista em aula hoje
import copy #Importação do método copy que o professor apresentou na aula.

class Desenho :
    
    def __init__(self) :
        self.figuras = []
        self.figura_atual = None
        self.figura_selecionada = None # Adicionado atributo para verificar se uma figura está selecionada
        self.figura_copiada = None # Adicionado atributo para verificar se uma figura está selecionada
        self.deslocamento_colar = 0 #Adição de um deslocamento ao colar as figuras para sempre que eu der CTRL V varias vezes nao sair uma em cima da outra

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
        
    # ========= Para as figuras que estão na lista self.figuras ===========

    def adicionar_figura_concluida(self) :
        if self.figura_atual :
            self.figuras.append(self.figura_atual)
            self.figura_atual = None

    # A partir desta função 'obter' o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras

    #======== DELETAR FIGURAS SELECIONADAS =======================
    
    def deletar_selecionada(self):
        if self.figura_selecionada:
            self.figuras.remove(self.figura_selecionada)
            figura_apagada = self.figura_selecionada
            self.figura_selecionada = None
            return figura_apagada
        return None
    
    #========= MOVER PARA O TOPO DE VEZ =================
    
    def mover_para_topo(self):
        if self.figura_selecionada is None:
            return
        
        self.figuras.remove(self.figura_selecionada)
        self.figuras.append(self.figura_selecionada)
    
    #========= MOVER PARA O FUNDO DE VEZ =========
    
    def mover_para_fundo(self):
        if self.figura_selecionada is None:
            return
        
        self.figuras.remove(self.figura_selecionada)
        self.figuras.insert(0, self.figura_selecionada)
    
    #============ MOVER PARA FRENTE 1 POR VEZ =================

    def mover_para_frente(self):
        if self.figura_selecionada is None:
            return
        
        #PERCORRE TODA LISTA DE FIGURAS, MENOS O ULTIMO INDICE
        for i in range(len(self.figuras) - 1):
            figura_atual = self.figuras[i] #SE FOR A FIGURA SELECIONADA TROCA DE LUGAR COM A DO INDICE DA FRENTE
            if figura_atual == self.figura_selecionada:
                self.figuras[i], self.figuras[i + 1] = self.figuras[i + 1], self.figuras[i]
                return
            
    #===============COPIAR E COLAR FIGURA=========#
    
    def copiar_figura(self):
        if self.figura_selecionada:
            self.figura_copiada = copy.deepcopy(self.figura_selecionada)
            self.deslocamento_colar = 15

    def colar_figura(self):
        if self.figura_copiada:
            figura = copy.deepcopy(self.figura_copiada)
            figura.mover(self.deslocamento_colar, self.deslocamento_colar)
            self.figuras.append(figura)
            self.figura_selecionada = figura
            self.deslocamento_colar += 10


    #========== MOVER PARA TRAS 1 POR VEZ =================

    def mover_para_tras(self):
        if self.figura_selecionada is None:
            return
    
           #PERCORRE TODA LISTA DE FIGURAS, MENOS O ULTIMO INDICE
        for i in range(1, len(self.figuras)):
            figura_atual = self.figuras[i] #SE FOR A FIGURA SELECIONADA TROCA DE LUGAR COM A DO INDICE DA DE TRAS
            if figura_atual == self.figura_selecionada:
                self.figuras[i], self.figuras[i - 1] = self.figuras[i - 1], self.figuras[i]
                return

     # ========= Para salvar, abrir e limpar os desenho contidos na lista em um arquivo ===========  

    def salvar_desenhos(self, caminho):
        with open(caminho, "wb") as arquivo:
            pickle.dump(self.figuras, arquivo)  

    def abrir_arquivo_desenho(self, caminho):
        with open(caminho, "rb") as arquivo:
            self.figuras = pickle.load(arquivo)
            
        self.figura_atual = None
        self.figura_selecionada = None
        self.figura_copiada = None
    
    def limpar_desenhos(self):
        if not self.figuras:
            return False

        self.figuras = []
        self.figura_atual = None
        self.figura_selecionada = None
        self.figura_copiada = None

        return True
    
   