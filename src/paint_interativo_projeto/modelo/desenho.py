import json
import modelo.figuras as figuras

#Importação do módulo 'JSON' para conseguir salvar os arquivos em 'JSON'
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

    # A partir desta função 'obter' o controller irá ficar a par da lista de figuras
    def obter_figuras(self) :
        return self.figuras
    
     # ========= Para salvar os desenho contidos na lista em um arquivo ===========
    def salvar_desenhos(self, caminho):
        dados_desenhos = []
        
        for figura in self.figuras: 
            #Traansforma em dicionário e adicona na lista

            dados_desenhos.append(figura.transformar_figura_dicionario())
            
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
            

    '''Este método serve para, abirir um desenho salvo, e alem disso ele também percorre cada dicionário da lista, aliás após percorrer e identifi-
    car qual o tipo do objeto, ele pega os dados do dicionário e transforma em um objeto python (o desenho)'''     
    def abrir_arquivo_desenho(self, caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:

            lista_dados_figuras = json.load(arquivo)
            
            '''Observações :
            - r vem de read = leitura
            - json.load le o json e transforma em dicionario
            
            '''
            

        self.figuras = []

    
        ''''O dicionário construtor, tem por função, associar o nome da figura em questão e forma como ela deve
        ser inicializada, -Do meu ponto de vista, essa opção eh uma forma muito eficiente e adequada para
        substituir aqueles, ifs que tinhamos antes.'''
        
        construtor = {
            'Linha' : lambda d : figuras.Linha(d['x1'], d['y1'], d['x2'], d['y2'],
                                              d['cor_borda'], d['tamanho_borda']),
            'Retangulo' : lambda d : figuras.Retangulo(d['x1'], d['y1'], d['x2'], d['y2'],
                                              d['cor_borda'], d['cor_preenchimento'], d['tamanho_borda']),
            'Oval' : lambda d : figuras.Oval(d['x1'], d['y1'], d['x2'], d['y2'],
                                              d['cor_borda'], d['cor_preenchimento'], d['tamanho_borda']),
            'Circulo' : lambda d : figuras.Circulo(d['centro_x'], d['centro_y'], d['raio'],
                                                 d['cor_borda'], d['cor_preenchimento'], d['tamanho_borda']),
            'Poligono' : lambda d : figuras.Poligono(d['pontos'],
                                                    d['cor_borda'], d['cor_preenchimento'], d['tamanho_borda'], d['fechado']),
            'Rabisco' : lambda d : figuras.Rabisco(d['pontos'],
                                                 d['cor_borda'], d['tamanho_borda'])                      
        }
        
        '''Alterei a variável dados_desenho para dados  '''
        for dados in lista_dados_figuras :
            tipo = dados.get('tipo', 'Rabisco') # Aqui estamos utilizando o get para obter o tipo da figura, e "Rabisco" eh o valor defalt...
            if tipo in construtor :
                figura = construtor[tipo](dados)
                self.figuras.append(figura)

        '''Por fim, é aqui que a mágica acontece, primeiro para garantir, verificamos se 'tipo' realmente está naquele dicionário,
        "construtor", daí, chamamos a função lambda correspondente, passando o dicionário de dados como argumento'''

            
    
    def limpar_desenhos(self):
        self.figuras = []
        self.figura_atual = None
    