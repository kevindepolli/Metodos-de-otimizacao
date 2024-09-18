import time

from Contrutiva import Construtiva
from Vizinho import Vizinho
from simulated_annealing import simulated_annealing


def calcular_fo(maquinas, pesos):
    maquinas_pesos = [sum(pesos[tarefa] for tarefa in maquina) for maquina in maquinas]
    return max(maquinas_pesos)


def exibir_maquina(maquinas, pesos):
    for i, maquina in enumerate(maquinas, start=1):
        print(f"Máquina {i}: {list(maquina)}")
    print("FO: ", calcular_fo(maquinas, pesos))


def execucao(numero_maquinas):

    # nome_arquivo_grafo = "grafos/grafo.txt"
    nome_arquivo_grafo = "grafos/HAHN.IN2"
    nome_arquivo_solucoes = "solucoes.txt"
    tempo_parada = 9999999999
    iteracoes_refinamento = 5

    taxa_resfriamento = 0.998
    equilibrio_termico = 20
    temperatura_inicial = 1000
    temperatura_congelamento = 0.0001

    inicio_construtiva = time.time()

    construtiva = Construtiva(nome_arquivo_grafo, numero_maquinas)
    fim_construtiva = time.time()

    print("------------------------------------------")
    print("Solução Inicial:")
    construtiva.maquina.exibir_resultado()

    tempo_execucao_contrutiva = fim_construtiva - inicio_construtiva
    print(f"Tempo de execução: {tempo_execucao_contrutiva:.6f} segundos\n")

    for i in range(iteracoes_refinamento):
        inicio_refinamento = time.time()

        solucao, tempo_melhor_solucao = simulated_annealing(taxa_resfriamento, equilibrio_termico, temperatura_inicial, temperatura_congelamento, construtiva.maquina.maquinas, tempo_parada, construtiva.grafo)

        fim_refinamento = time.time()

        print("------------------------------------------")
        print(f"Melhor Solução Encontrada {i}:")

        exibir_maquina(solucao, construtiva.grafo.pesos)

        tempo_execucao_refinamento = fim_refinamento - inicio_refinamento
        print(f"Tempo de execução {i}: {tempo_execucao_refinamento:.6f} segundos")
        print(f"Instante em que a melhor solução foi encontrada: {tempo_melhor_solucao:.6f} segundos\n")


execucao(6)
execucao(8)
execucao(10)
