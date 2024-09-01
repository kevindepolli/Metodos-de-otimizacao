from collections import deque


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

    def encontrar_vertices_iniciais(self):
        vertices_inciais = []
        for i in range(self.vertices):
            if not self.tem_anterior(i):
                vertices_inciais.append(i)
        return vertices_inciais

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

    def busca_bf(self, vertices_iniciais):
        visitado = set()
        fila = deque(vertices_iniciais)

        # Adicionar todos os vértices iniciais ao conjunto de visitados
        visitado.update(vertices_iniciais)
        resultado = []

        while fila:
            vertice = fila.popleft()
            resultado.append(vertice)

            for vizinho in self.vertices_sucessores(vertice):
                if vizinho not in visitado:
                    visitado.add(vizinho)
                    fila.append(vizinho)

        return resultado
