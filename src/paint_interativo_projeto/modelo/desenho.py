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
        
        
    # ========= Para as figuras que estão na lista self.figuras ===========

    def adicionar_figura_concluida(self) :
        if self.figura_atual :
            self.figuras.append(self.figura_atual)
            self.figura_atual = None

    # A partir desta função 'obter' o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras
    
     # ========= Para salvar, abrir e limpar os desenho contidos na lista em um arquivo ===========
      
     
    #======== DELETAR FIGURAS SELECIONADAS =======================
    
    def deletar_selecionada(self):
        if self.figura_selecionada:
            self.figuras.remove(self.figura_selecionada)
            figura_apagada = self.figura_selecionada
            self.figura_selecionada = None
            return figura_apagada
        return None
    
    #========== FIM DESSA SEÇÃO DE DELETAR FIGURAS SELECIONADAS==========  
    
    
      
    #========= MOVER PARA O TOPO DE VEZ =================
    
    def mover_para_topo(self):
        self.figuras.remove(self.figura_selecionada)
        self.figuras.append(self.figura_selecionada)
    
    #FIM DA SESSÃO DE MOVER PARA O TOPO DE VEZ =================
    
    
    #========= MOVER PARA O FUNDO DE VEZ =========
    
    def mover_para_fundo(self):
        self.figuras.remove(self.figura_selecionada)
        self.figuras.insert(0, self.figura_selecionada)
        
    #========== FIM DA SESSÃO DE MOVER PARA O FUNDO DE VEZ =================
    
    
    #============ MOVER PARA FRENTE 1 POR VEZ =================
    def mover_para_frente(self):
        
        #PERCORRE TODA LISTA DE FIGURAS, MENOS O ULTIMO INDICE
        for i in range(len(self.figuras) - 1):
            figura_atual = self.figuras[i] #SE FOR A FIGURA SELECIONADA TROCA DE LUGAR COM A DO INDICE DA FRENTE
            if figura_atual == self.figura_selecionada:
                self.figuras[i], self.figuras[i + 1] = self.figuras[i + 1], self.figuras[i]
                return
            
    #============ FIM DA SESSÃO DE MOVER PARA FRENTE 1 POR VEZ =================
    
    #===============COPIAR E COLAR FIGURA=========#
    
    def copiar_figura(self):
        if self.figura_selecionada:
            self.figura_copiada = self.figura_selecionada.copiar()
            
            
    def colar_figura(self):
        if self.figura_copiada:
            figura_nova_copiada = self.figura_copiada.copiar()
            figura_nova_copiada.mover(20, 20)
            self.figuras.append(figura_nova_copiada)
            self.figura_selecionada = figura_nova_copiada
        
    #============ COPIAR E COLAR FIGURA=========#    
        
        
        
        
    #========== MOVER PARA TRAS 1 POR VEZ =================
    def mover_para_tras(self):
           #PERCORRE TODA LISTA DE FIGURAS, MENOS O ULTIMO INDICE
        for i in range(1, len(self.figuras)):
            figura_atual = self.figuras[i] #SE FOR A FIGURA SELECIONADA TROCA DE LUGAR COM A DO INDICE DA DE TRAS
            if figura_atual == self.figura_selecionada:
                self.figuras[i], self.figuras[i - 1] = self.figuras[i - 1], self.figuras[i]
                return
    #========== FIM DA SESSÃO DE MOVER PARA TRAS 1 POR VEZ ================
        
        
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
    
   