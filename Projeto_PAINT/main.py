'''Tive que definir um arquvio __init__.py em todas as pastas, para que assim o python enxergue
que elas estão no mesmo 'pacote' apesar de o nosso senso dizer que o ideal seria usar o 
(from src.paint_interativo_projeto.visao.arquivo import iniciar_interface), eu tentei assim e não
deu certo, a janela não abriu, alias a outras formas de contornar está situação sem ter que definir
esses arquvios vazios lá, admito que não entendi muito bem isto, então recomendo pesquisar um pouco
sobre, aliás isso vale para mim também, OBS: definir arquivos váios também não funcionou '''

'======================================================================================================='
import sys
import os

# Adiciona a pasta 'src' ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from paint_interativo_projeto.visao.arquivo import iniciar_interface 
'======================================================================================================='


'''Realmente tivi que recorrer a opção que eu queria evitar..., mas enfim, as outras alternativas existem,
mas, essa foi a única que funcionou, ainda assim deixei o comentário acima, para contextualizar vcs'''


if __name__ == '__main__':
    iniciar_interface()  
