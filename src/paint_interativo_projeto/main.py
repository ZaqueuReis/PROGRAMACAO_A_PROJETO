from modelo.desenho import Desenho
from visao.janela import Janela
from controlador.controlador import Controlador


def main():
    desenho = Desenho()
    janela = Janela()
    controlador = Controlador(desenho,janela)
    janela.registrar_controlador(controlador) # Registra o controlador responsável pelas ações da interface.
    janela.iniciar()

main()