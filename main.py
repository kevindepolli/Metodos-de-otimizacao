import copy
import random
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

        print("Sequencia dos vertices:", sequencia_vertices)
        while sequencia_vertices:
            vertice_atual = sequencia_vertices.popleft()
            candidatos = self.sucessores_viaveis(vertice_atual)
            print("-------------------------------")
            print("Solução:", self.solucao)
            print("Vértice analisado:", vertice_atual)

            if vertice_atual not in self.solucao:
                self.adicionar_vertice_solucao(vertice_atual)

            print("Candidatos:", candidatos)

            while candidatos:
                vertice_candidato_escolhido = escolha_aleatoria(candidatos)
                self.adicionar_vertice_solucao(vertice_candidato_escolhido)
                candidatos.remove(vertice_candidato_escolhido)

        self.fo = calcular_fo(self)

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
        match self.maquina_lotada():
            case 0:
                self.maquinas[-1].append(vertice)  # Adiciona vertice na máquina atual
            case 1:
                self.maquinas.append(deque([vertice]))  # Cria uma nova máquina

    def maquina_lotada(self):
        if (len(self.maquinas) == self.numero_maquinas  # Verifica se essa máquina é a última
                and len(self.maquinas[-1]) < self.vertices_maquinas + self.vertices_restantes):  # Se os restantes já adicionados
            return 0  # Última máquina ainda tem espaço

        if len(self.maquinas[-1]) >= self.vertices_maquinas:  # Verifica se a máquina atual atingiu o limite
            return 1  # Máquina lotada

        return 0  # Máquina atual ainda tem espaço

    def exibir_maquinas(self):
        maquinas = []
        for maquina in self.maquinas:
            maquinas.append(list(maquina))

        return maquinas

def salvar_solucao(nome_arquivo, solucao):
    with open(nome_arquivo, 'a') as arquivo:
        # Transforma a lista em uma string separada por vírgulas
        linha = ','.join(map(str, solucao)) + '\n'
        arquivo.write(linha)


def calcular_fo(heuristica):
    pesos = heuristica.grafo.pesos
    maquinas = heuristica.maquinas
    maquinas_pesos = []
    soma = 0
    for maquina in maquinas:
        for tarefa in maquina:
            soma += pesos[tarefa]
        maquinas_pesos.append(soma)
        soma = 0
    return max(maquinas_pesos)


def busca_local(heuristica):
    maquinas = heuristica.maquinas

    for maquina in range(len(maquinas) - 1):
        maquinas[maquina].append(maquinas[maquina+1].popleft())

    maquinas[-1].append(maquinas[0].popleft())


if __name__ == "__main__":
    nome_arquivo_grafo = "grafos/HAHN.IN2"
    # nome_arquivo_grafo = "grafos/grafo.txt"
    nome_arquivo_solucoes = "solucoes.txt"

    grafo = Grafo(nome_arquivo_grafo)

    print("Matriz de adjacência:")
    grafo.imprimir_matriz_adjacencia()

    print("Pesos dos vértices:")
    print(grafo.pesos)

    heuristicaConstrutiva = HeuristicaContrutivaAleatoria(grafo, 4)
    print("-------------------------------")
    print("Solução final:", heuristicaConstrutiva.exibir_maquinas(), "\n", calcular_fo(heuristicaConstrutiva))
    salvar_solucao(nome_arquivo_solucoes, heuristicaConstrutiva.exibir_maquinas())

    busca_local(heuristicaConstrutiva)
    print(heuristicaConstrutiva.exibir_maquinas(), "\n", calcular_fo(heuristicaConstrutiva))
