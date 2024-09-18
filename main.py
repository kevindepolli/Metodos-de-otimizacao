import time

from Contrutiva import Construtiva
from Vizinho import Vizinho
from simulated_annealing import simulated_annealing

def calcular_fo(maquinas, pesos):
    maquinas_pesos = [sum(pesos[tarefa] for tarefa in maquina) for maquina in maquinas]
    return max(maquinas_pesos)

def execucao(numero_maquinas):
    inicio = time.time()

    # nome_arquivo_grafo = "grafos/grafo.txt"
    nome_arquivo_grafo = "grafos/HAHN.IN2"
    nome_arquivo_solucoes = "solucoes.txt"

    construtiva = Construtiva(nome_arquivo_grafo, numero_maquinas)
    construtiva.maquina.exibir_resultado()

    solucao = simulated_annealing(0.998, 20, 1000, 0.0001, construtiva.maquina.maquinas, construtiva.grafo)

    for i, maquina in enumerate(solucao, start=1):
        print(f"Máquina {i}: {list(maquina)}")
    print("FO: ", calcular_fo(solucao, construtiva.grafo.pesos))

    fim = time.time()

    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")


execucao(4)
# execucao(7)
# execucao(8)
# execucao(9)
# execucao(10)
