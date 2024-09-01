import time

from Contrutiva import Construtiva


def execucao(numero_maquinas):
    inicio = time.time()

    # nome_arquivo_grafo = "grafos/grafo.txt"
    nome_arquivo_grafo = "grafos/HAHN.IN2"
    nome_arquivo_solucoes = "solucoes.txt"

    construtiva = Construtiva(nome_arquivo_grafo, numero_maquinas)
    construtiva.maquina.exibir_resultado()

    fim = time.time()

    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")


execucao(6)
# execucao(7)
# execucao(8)
# execucao(9)
# execucao(10)
