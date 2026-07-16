import pickle # Substituição pela biblioteca vista em aula hoje
import copy #Importação do método copy que o professor apresentou na aula.
from modelo.figuras import FiguraComposta # Importando figura composta, acredito que isso é permitido no MVC

class Desenho :
    
    def __init__(self) :
        self.figuras = []
        self.figura_atual = None
        self.figuras_selecionadas = [] # Transformação em figuras selecionadas, ou seja, uma lista.
        self.figura_copiada = None # Adicionado atributo para verificar se uma figura está selecionada
        self.deslocamento_colar = 0 #Adição de um deslocamento ao colar as figuras para sempre que eu der CTRL V varias vezes nao sair uma em cima da outra

    # ========= Para figuras em construção no momento do desenho ==========

    def inicializar_figura_atual(self, figura) :
        self.figura_atual = figura
    
    def obter_figura_atual(self) :
        return self.figura_atual
    
    # ========== Para permitir a seleção de figuras com o mouse ===========
    
    def obter_figuras_selecionadas(self):
        return self.figuras_selecionadas

    def definir_figuras_selecionadas(self, figuras):
        self.figuras_selecionadas = figuras

    def limpar_selecao(self):
        self.figuras_selecionadas.clear()
        #FUNÇÃO CLEAR SERVE PARA ESVAZIAR UMA LISTA


    #ADICIONANDO NOVOS MÉTODOS PARA SELEÇAO MULTIPLA DE FIGURAS:
    def adicionar_selecao(self, figura):
        if figura not in self.figuras_selecionadas:
            self.figuras_selecionadas.append(figura)
            #ESSA FUNÇÃO ACIMA FAZ O SEGUINTE: SE CASO VOCE CLICAR EM UMA FIGURA QUE NAO ESTÁ SELECIONADA ELE 
            #ADICIONA NA LISTA DE FIGURAS SELECIONADAS
    
    def remover_selecao(self, figura):
        if figura in self.figuras_selecionadas:
            self.figuras_selecionadas.remove(figura)
            #SE CLICAR NUMA FIGURA QUE JA ESTA NA LISTA DE FIGURAS SELECIONADAS
            #REMOVA DA LISTA DE FIGURAS SELECIONADAS A FIGURA CLICADA
    
    
    #FIM NOVOS MÉTODOS
    
    
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
        if not self.figuras_selecionadas:
            return None

        for figura in self.figuras_selecionadas:
            if figura in self.figuras:
                self.figuras.remove(figura)

        self.figuras_selecionadas.clear()
        #FUNÇÃO CLEAR SERVE PARA ESVAZIAR UMA LISTA

        return True
    
    #========= MOVER PARA O TOPO DE VEZ =================
    
    def mover_para_topo(self):
        if not self.figuras_selecionadas:
            return

        for figura in self.figuras_selecionadas:
            self.figuras.remove(figura)

        self.figuras.extend(self.figuras_selecionadas)
    
    #========= MOVER PARA O FUNDO DE VEZ =========
    
    def mover_para_fundo(self):
        if not self.figuras_selecionadas:
            return

        for figura in self.figuras_selecionadas:
            self.figuras.remove(figura)

        self.figuras = self.figuras_selecionadas + self.figuras
    
    #============ MOVER PARA FRENTE 1 POR VEZ =================

    def mover_para_frente(self):
        if not self.figuras_selecionadas:
            return

        for i in range(len(self.figuras)-2, -1, -1):

            if (self.figuras[i] in self.figuras_selecionadas and
                self.figuras[i+1] not in self.figuras_selecionadas):

                self.figuras[i], self.figuras[i+1] = self.figuras[i+1], self.figuras[i]
            

    #========== MOVER PARA TRAS 1 POR VEZ =================
    def mover_para_tras(self):
        if not self.figuras_selecionadas:
            return

        for i in range(1, len(self.figuras)):

            if (self.figuras[i] in self.figuras_selecionadas and
                self.figuras[i-1] not in self.figuras_selecionadas):

                self.figuras[i], self.figuras[i-1] = self.figuras[i-1], self.figuras[i]

    #===============COPIAR E COLAR FIGURA=========#
    
    def copiar_figura(self):
        if self.figuras_selecionadas:
            self.figura_copiada = copy.deepcopy(self.figuras_selecionadas)
            self.deslocamento_colar = 15

    def colar_figura(self):
            if not self.figura_copiada:
                return

            novas_figuras = copy.deepcopy(self.figura_copiada)

            for figura in novas_figuras:
                figura.mover(self.deslocamento_colar, self.deslocamento_colar)
                self.figuras.append(figura)

            self.figuras_selecionadas = novas_figuras

            self.deslocamento_colar += 10
    
    # Agrupar figuras ===========
    def agrupar_figuras(self):
        if len(self.figuras_selecionadas) < 2:
            return

        grupo = FiguraComposta(self.figuras_selecionadas)

        for figura in self.figuras_selecionadas:
            self.figuras.remove(figura)

        self.figuras.append(grupo)
        self.figuras_selecionadas = [grupo]
    
    # Desagrupar figuras ===========
    def desagrupar_figuras(self):
        if len(self.figuras_selecionadas) != 1:
            return

        grupo = self.figuras_selecionadas[0]

        if not isinstance(grupo, FiguraComposta):
            return

        self.figuras.remove(grupo)

        for figura in grupo.figuras:
            self.figuras.append(figura)

        self.figuras_selecionadas = list(grupo.figuras)

     # ========= Para salvar, abrir e limpar os desenho contidos na lista em um arquivo ===========  

    def salvar_desenhos(self, caminho):
        with open(caminho, "wb") as arquivo:
            pickle.dump(self.figuras, arquivo)  

    def abrir_arquivo_desenho(self, caminho):
        with open(caminho, "rb") as arquivo:
            self.figuras = pickle.load(arquivo)
            
        self.figura_atual = None
        self.figuras_selecionadas = []
        self.figura_copiada = None
    
    def limpar_desenhos(self):
        if not self.figuras:
            return False

        self.figuras = []
        self.figura_atual = None
        self.figuras_selecionadas = []
        self.figura_copiada = None

        return True
