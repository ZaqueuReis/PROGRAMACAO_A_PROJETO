from modelo.desenho import Desenho
from visao.janela import Janela
from controlador.controlador import Controlador


def main():
    desenho = Desenho()
    janela = Janela()
    controlador = Controlador(desenho,janela)
    janela.iniciar()

main()