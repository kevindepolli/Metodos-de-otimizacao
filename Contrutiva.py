from collections import deque

from Grafo import Grafo
from Maquina import Maquina, calcular_fo


class Construtiva:
    def __init__(self, nome_arquivo_grafo, numero_maquinas):
        self.grafo = Grafo(nome_arquivo_grafo)
        self.maquina = Maquina(self.grafo, numero_maquinas)
        self.candidatos = deque([])

        for vertice in self.maquina.vertices_iniciais:
            self.adicionar_vertice_solucao_atualizar_candidatos(vertice)

        escolher_maior_peso = True
        while len(self.maquina.solucao) < self.grafo.vertices:
            if escolher_maior_peso:
                self.adicionar_vertice_solucao_atualizar_candidatos(self.candidatos.pop())
                escolher_maior_peso = False
            else:
                self.adicionar_vertice_solucao_atualizar_candidatos(self.candidatos.popleft())
                escolher_maior_peso = True

        self.maquina.fo = calcular_fo(self.maquina.maquinas, self.grafo.pesos)

    def adicionar_vertice_solucao_atualizar_candidatos(self, vertice):
        # TODO: implementar um exception handler para quando o vertice não for adicionado try catch
        self.maquina.adicionar_vertice_solucao(vertice)
        [self.adicionar_candidato(_) for _ in self.maquina.sucessores_viaveis(vertice)]

    def adicionar_candidato(self, vertice):
        self.insercao_ordenada(vertice, self.candidatos, self.grafo.pesos)

    def insercao_ordenada(self, vertice, lista, lista_pesos, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(lista)
        while lo < hi:
            mid = (lo+hi)//2
            if lista_pesos[vertice] < lista_pesos[lista[mid]]:
                hi = mid
            else:
                lo = mid+1
        lista.insert(lo, vertice)