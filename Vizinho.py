import random
from collections import deque
from copy import deepcopy

from Maquina import calcular_fo


class Vizinho:
    def __init__(self, solucao, grafo):
        self.solucao = deepcopy(solucao)
        self.grafo = grafo
        self.maquina = self.escolher_maquina(self.solucao)
        self.vertice = random.choice(self.maquina)
        maior_maquina_vertice_anterior = self.busca_maior_maquina_vertice_anterior(self.solucao, self.grafo, self.vertice)
        self.maquina_adotiva = self.solucao[random.randint(maior_maquina_vertice_anterior, len(self.solucao) - 1)]
        self.switch_maquina()

    def escolher_maquina(self, solucao):

        maquina_escolhida = random.choice(solucao)

        while len(maquina_escolhida) < 2:
            maquina_escolhida = random.choice(solucao)

        return maquina_escolhida

    # Grafo
    def buscar_maquina_vertice(self, maquinas, vertice):
        for i, maquina in enumerate(maquinas):
            if vertice in maquina:
                return i


    # Maquina
    def busca_maior_maquina_vertice_anterior(self, solucao, grafo, vertice):
        vertices_anteriores = grafo.vertices_anteriores(vertice)
        if not vertices_anteriores:
            return 0

        maior_maquina_vertice_anterior = -1
        for anterior in vertices_anteriores:
            maquina_anterior = self.buscar_maquina_vertice(solucao, anterior)
            if maquina_anterior > maior_maquina_vertice_anterior:
                maior_maquina_vertice_anterior = maquina_anterior

        return maior_maquina_vertice_anterior

    # Maquina
    def switch_maquina(self):
        self.maquina_adotiva.append(self.vertice)
        self.maquina.remove(self.vertice)
