import copy
import random
import time
from collections import deque
from functools import reduce


class Grafo:
    def __init__(self, nome_arquivo):
        self.matriz_adj = []
        self.pesos = []

        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        self.vertices = int(linhas[0].strip())  # Número de vértices
        self.pesos = list(map(int, linhas[1:self.vertices + 1]))  # Pesos dos vértices

        # Inicializa a matriz de adjacência com zeros
        self.matriz_adj = [[0] * self.vertices for _ in range(self.vertices)]

        index = self.vertices + 1
        while index < len(linhas):
            linha = linhas[index].strip()
            if linha == "-1,-1":
                break
            u, v = map(int, linha.split(','))
            self.adicionar_aresta(u - 1, v - 1)
            index += 1

    def adicionar_aresta(self, u, v):
        self.matriz_adj[u][v] = 1

    def imprimir_matriz_adjacencia(self):
        for row in self.matriz_adj:
            print(row)

    def tem_anterior(self, vertice):
        for i in range(self.vertices):
            if self.matriz_adj[i][vertice] == 1:
                return True
        return False

    def encontrar_vertice_inicial(self):
        for i in range(self.vertices):
            if not self.tem_anterior(i):
                return i

    def vertices_sucessores(self, vertice):
        sucessores = []
        for i in range(self.vertices):
            if self.matriz_adj[vertice][i] == 1:
                sucessores.append(i)
        return sucessores

    def vertices_anteriores(self, vertice):
        anteriores = []
        for i in range(self.vertices):
            if self.matriz_adj[i][vertice] == 1:
                anteriores.append(i)
        return anteriores

    def busca_bf(self, vertice_inicial):
        visitado = set()
        fila = deque([vertice_inicial])
        visitado.add(vertice_inicial)
        resultado = []

        while fila:
            vertice = fila.popleft()
            resultado.append(vertice)

            for vizinho in self.vertices_sucessores(vertice):
                if vizinho not in visitado:
                    visitado.add(vizinho)
                    fila.append(vizinho)
        return resultado


def escolha_aleatoria(lista):
    return random.choice(lista)


class HeuristicaContrutivaAleatoria:
    def __init__(self, grafo, numero_maquinas):
        self.grafo = grafo
        self.numero_maquinas = numero_maquinas
        vertice_inicial = grafo.encontrar_vertice_inicial()
        self.solucao = []
        self.solucao.append(vertice_inicial)
        sequencia_vertices = deque(grafo.busca_bf(vertice_inicial))  # Resultado da busca por largura
        candidatos = []

        self.fo = 0

        self.vertices_maquinas = self.grafo.vertices // numero_maquinas
        self.vertices_restantes = self.grafo.vertices - (self.vertices_maquinas * numero_maquinas)
        self.maquinas = [deque([vertice_inicial])]

        while sequencia_vertices:
            vertice_atual = sequencia_vertices.popleft()
            candidatos = self.sucessores_viaveis(vertice_atual)

            if vertice_atual not in self.solucao:
                self.adicionar_vertice_solucao(vertice_atual)

            while candidatos:
                vertice_candidato_escolhido = escolha_aleatoria(candidatos)
                self.adicionar_vertice_solucao(vertice_candidato_escolhido)
                candidatos.remove(vertice_candidato_escolhido)

        self.fo = calcular_fo(self.maquinas, self.grafo.pesos)

    def sucessores_viaveis(self, vertice):
        candidatos = self.grafo.vertices_sucessores(vertice)
        for candidato in candidatos:
            anteriores = self.grafo.vertices_anteriores(candidato)
            if candidato in self.solucao:
                candidatos.remove(candidato)
                continue
            for anterior in anteriores:
                if anterior not in self.solucao:
                    candidatos.remove(candidato)
                    break
        return candidatos

    def adicionar_vertice_solucao(self, vertice):
        self.solucao.append(vertice)
        self.adicionar_vertice_maquina(vertice)

    def adicionar_vertice_maquina(self, vertice):
        if len(self.maquinas) < self.numero_maquinas:
            # Se o número de máquinas é menor que o número total de máquinas
            if len(self.maquinas[-1]) >= self.vertices_maquinas:
                # Se a última máquina está cheia, cria uma nova máquina
                self.maquinas.append(deque([vertice]))
            else:
                # Caso contrário, adiciona o vértice à última máquina
                self.maquinas[-1].append(vertice)
        else:
            # Se o número de máquinas é igual ao número total de máquinas
            if len(self.maquinas[-1]) < self.vertices_maquinas + self.vertices_restantes:
                # Se a última máquina ainda pode receber mais vértices
                self.maquinas[-1].append(vertice)
            else:
                # Caso contrário, cria uma nova máquina
                self.maquinas.append(deque([vertice]))

    def maquina_lotada(self):
        if (len(self.maquinas) == self.numero_maquinas  # Verifica se essa máquina é a última
                and len(self.maquinas[-1]) < self.vertices_maquinas + self.vertices_restantes):  # Se os restantes já adicionados
            return 0  # Última máquina ainda tem espaço

        if len(self.maquinas[-1]) >= self.vertices_maquinas:  # Verifica se a máquina atual atingiu o limite
            return 1  # Máquina lotada

        return 0  # Máquina atual ainda tem espaço

    def exibir_resultado(self):
        for i, maquina in enumerate(self.maquinas, start=1):
            print(f"Máquina {i}: {list(maquina)}")
        print("FO: ", heuristicaConstrutiva.fo)

    def salvar_solucao(self, nome_arquivo):
        with open(nome_arquivo, 'a') as arquivo:
            for i, maquina in enumerate(self.maquinas, start=1):
                linha = f"Máquina {i}: {list(maquina)}" + '\n'
                arquivo.write(linha)
            fo = f"FO: {self.fo}"
            arquivo.write(fo)


def calcular_fo(maquinas, pesos):
    maquinas_pesos = [sum(pesos[tarefa] for tarefa in maquina) for maquina in maquinas]
    return max(maquinas_pesos)


def vizinho(maquinas, maquina):
    if maquina == len(maquinas) - 1:
        if len(maquinas[maquina]) < len(maquinas[0]):
            if maquinas[0]:
                maquinas[maquina].append(maquinas[0].popleft())
    else:
        if len(maquinas[maquina]) > 0:
            if maquinas[maquina + 1]:
                maquinas[maquina + 1].append(maquinas[maquina].popleft())
    return maquinas


def ultima_maquina(lista, indice):
    if indice == len(lista) - 1:
        return True
    else:
        return False


def busca_local(heuristica):
    pesos = heuristica.grafo.pesos
    melhor_solucao = heuristica.maquinas
    fo_melhor = heuristica.fo
    for i in range(len(heuristica.maquinas)):
        solucao_atual = vizinho(copy.deepcopy(melhor_solucao), i)
        fo_atual = calcular_fo(solucao_atual, pesos)
        fo_melhor = calcular_fo(melhor_solucao, pesos)
        if fo_atual < fo_melhor:
            melhor_solucao = solucao_atual
    heuristica.maquinas = melhor_solucao
    heuristica.fo = fo_melhor


if __name__ == "__main__":
    inicio = time.time()
    nome_arquivo_grafo = "grafos/HAHN.IN2"
    # nome_arquivo_grafo = "grafos/grafo.txt"
    nome_arquivo_solucoes = "solucoes.txt"

    grafo = Grafo(nome_arquivo_grafo)

    heuristicaConstrutiva = HeuristicaContrutivaAleatoria(grafo, 4)

    busca_local(heuristicaConstrutiva)
    heuristicaConstrutiva.fo = calcular_fo(heuristicaConstrutiva.maquinas, heuristicaConstrutiva.grafo.pesos)

    heuristicaConstrutiva.salvar_solucao(nome_arquivo_solucoes)
    heuristicaConstrutiva.exibir_resultado()

    fim = time.time()

    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")