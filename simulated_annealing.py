import math
import random

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
                        grafo):

    melhor_solucao = solucao_inicial
    solucao_atual = solucao_inicial
    iteracoes_temperatura = 0
    temperatura_corrente = temperatura_inicial

    while temperatura_corrente > temperatura_congelamento:
        while iteracoes_temperatura < equilibrio_termico:
            iteracoes_temperatura += 1
            vizinho = gerar_vizinho(solucao_atual, grafo)
            delta = calcular_fo(vizinho, grafo.pesos) - calcular_fo(solucao_atual, grafo.pesos)
            if delta < 0:
                solucao_atual = vizinho
                if calcular_fo(vizinho, grafo.pesos) < calcular_fo(melhor_solucao, grafo.pesos):
                    melhor_solucao = vizinho
            else:
                parcela_aleatoria = random.random()
                if parcela_aleatoria < math.exp(-delta/temperatura_corrente):
                    solucao_atual = vizinho

        temperatura_corrente = temperatura_corrente * taxa_resfriamento
        iteracoes_temperatura = 0

    return melhor_solucao
