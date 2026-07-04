import json
import modelo.figuras as figuras
#IMPORTAÇÃO DO MODULO JSON PARA CONSEGUIR SALVAR OS ARQUIVOS EM JSON
class Desenho :
    
    def __init__(self) :
        self.figuras = []
        self.figura_atual = None

    # ========= Para figuras em construção no momento do desenho ==========

    def inicializar_figura_atual(self, figura) :
        self.figura_atual = figura
    
    def obter_figura_atual(self) :
        return self.figura_atual
    
    # ========= Para as figuras que estão na lista self.figuras ===========

    def adicionar_figura_concluida(self) :
        if self.figura_atual :
            self.figuras.append(self.figura_atual)
            self.figura_atual = None

    # A partir desta função obter o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras
    
    #CRIAÇÃO DO MÉTODO SALVAR DESENHO
    def salvar_desenhos(self, caminho):
        dados_desenhos = [] #CRIADO PARA ARMAZENAR OS DADOS DOS DESENHOS
        
        for figura in self.figuras: #PERCORRE TODAS AS FIGURAS DO CANVAS
            dados_desenhos.append(figura.transformar_figura_dicionario()) #TRANSFORMA EM DICIONARIO E ADICIONA NA LISTA
            
        with open(caminho, "w", encoding="utf-8") as arquivo_desenho:
            
            '''
            - with open função do python
            - caminho ele pega o caminho (em qual pasta iremos salvar)
            - w = escreve do zero e apaga o conteudo antigo do arquivo
            - "as arquivo_desenho" representa o arquivo aberto (que no caso está sendo criado)
            
            '''
            
            json.dump(dados_desenhos, arquivo_desenho, indent=4)
            
            '''
            - json.dump escreve o dicionario em arquivo json
            - dados desenho é os dados do desenho que serão salvos
            - arquivo_desenho é o arquivo
            - indente função do json
            '''
            

            
    def abrir_arquivo_desenho(self, caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:

            lista_dados_figuras = json.load(arquivo)
            
            '''
            - método para abrir um desenho salvo.
            - r vem de read = leitura
            - json.load le o json e transforma em dicionario
            
            '''
            

        self.figuras = []

        
        
        #MÉTODO PARA PERCORRER CADA DICIONARIO DA LISTA - IMPLEMENTAR MELHORIA PARA DIMINUIR ESSES IF
        #APÓS PERCORRER E IDENTIFICAR QUAL O TIPO DO OBJETO ELE PEGA OS DADOS DO DICIONARIO E TRANSFORMA EM UM OBJETO PYTHON (O DESENHO)
        for dados_desenhos in lista_dados_figuras:
            tipo = dados_desenhos["tipo"]

            if tipo == "Linha":
                figura = figuras.Linha(
                    dados_desenhos["x1"], dados_desenhos["y1"], dados_desenhos["x2"], dados_desenhos["y2"], dados_desenhos["cor_borda"], dados_desenhos["tamanho_borda"]
                )

            elif tipo == "Retangulo":
                figura = figuras.Retangulo(
                    dados_desenhos["x1"], dados_desenhos["y1"], dados_desenhos["x2"], dados_desenhos["y2"], dados_desenhos["cor_borda"], dados_desenhos["cor_preenchimento"], dados_desenhos["tamanho_borda"]
                )

            elif tipo == "Oval":
                figura = figuras.Oval(
                    dados_desenhos["x1"], dados_desenhos["y1"], dados_desenhos["x2"], dados_desenhos["y2"], dados_desenhos["cor_borda"], dados_desenhos["cor_preenchimento"], dados_desenhos["tamanho_borda"]
                )

            elif tipo == "Circulo":
                figura = figuras.Circulo(
                    dados_desenhos["centro_x"], dados_desenhos["centro_y"], dados_desenhos["raio"], dados_desenhos["cor_borda"], dados_desenhos["cor_preenchimento"], dados_desenhos["tamanho_borda"]
                )

            elif tipo == "Poligono":
                figura = figuras.Poligono(
                    dados_desenhos["pontos"], dados_desenhos["cor_borda"], dados_desenhos["cor_preenchimento"], dados_desenhos["tamanho_borda"], dados_desenhos["fechado"]
                )
                

            else:
                
                figura = figuras.Rabisco(
                    dados_desenhos["pontos"], dados_desenhos["cor_borda"], dados_desenhos["tamanho_borda"]
                )

            self.figuras.append(figura)
            
    
    def limpar_desenhos(self):
        self.figuras = []
        self.figura_atual = None
    
    '''Sinceramente, acredito eu que, usar o padrão MVC, ajuda não so nós que estamos
    desenvolvendo, a enteder precisamente o código, como também outras pessoas que
    não participou do desenvolvimento, gostei de mais disso, apesar que da um pouco
    de trabalho também, mas nada vem de graça...'''