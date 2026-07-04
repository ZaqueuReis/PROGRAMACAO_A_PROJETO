from modelo.desenho import Desenho
from visao.janela import Janela
from controlador.controlador import Controlador


def main():
    desenho = Desenho()
    janela = Janela()
    controlador = Controlador(desenho,janela)

    '''injetar o controller dentro da view para que os botões da interface
    consigam chamar salvar, abrir e limpar'''
    
    janela.controller = controlador
    janela.iniciar()

main()