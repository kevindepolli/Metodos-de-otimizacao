import math
import random
import time

from Vizinho import Vizinho
from Maquina import calcular_fo


def gerar_vizinho(solucao_atual, grafo):
    novo_vizinho = Vizinho(solucao_atual, grafo)
    return novo_vizinho.solucao


def simulated_annealing(taxa_resfriamento,
                        equilibrio_termico,
                        temperatura_inicial,
                        temperatura_congelamento,
                        solucao_inicial,
                        tempo_parada,
                        grafo):
    inicio = time.time()

    melhor_solucao = solucao_inicial
    solucao_atual = solucao_inicial
    tempo_melhor_solucao = time.time() - inicio
    iteracoes_temperatura = 0
    temperatura_corrente = temperatura_inicial
    tempo_execucao = 0

    while temperatura_corrente > temperatura_congelamento and tempo_execucao <= tempo_parada:

        while iteracoes_temperatura < equilibrio_termico:
            iteracoes_temperatura += 1
            vizinho = gerar_vizinho(solucao_atual, grafo)
            delta = calcular_fo(vizinho, grafo.pesos) - calcular_fo(solucao_atual, grafo.pesos)

            if delta < 0:
                solucao_atual = vizinho
                if calcular_fo(vizinho, grafo.pesos) < calcular_fo(melhor_solucao, grafo.pesos):
                    melhor_solucao = vizinho
                    tempo_melhor_solucao = time.time() - inicio
            else:
                parcela_aleatoria = random.random()
                if parcela_aleatoria < math.exp(-delta/temperatura_corrente):
                    solucao_atual = vizinho

        temperatura_corrente = temperatura_corrente * taxa_resfriamento
        iteracoes_temperatura = 0

        fim = time.time()

        tempo_execucao = fim - inicio

    return melhor_solucao, tempo_melhor_solucao
