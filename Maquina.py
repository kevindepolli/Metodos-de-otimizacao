import random
from collections import deque

class Maquina:
    def __init__(self, grafo, numero_maquinas):
        self.grafo = grafo
        self.numero_maquinas = numero_maquinas
        self.vertices_iniciais = grafo.encontrar_vertices_iniciais()
        self.solucao = []
        self.maquinas = deque([])
        self.fo = 0

        self.vertices_maquinas = self.grafo.vertices // numero_maquinas
        self.vertices_restantes = self.grafo.vertices - (self.vertices_maquinas * numero_maquinas)

    def adicionar_vertice_solucao(self, vertice):
        self.solucao.append(vertice)
        self.adicionar_vertice_maquina(vertice)

    def adicionar_vertice_maquina(self, vertice):

        if len(self.maquinas) > self.numero_maquinas:
            return

        if len(self.maquinas) == 0:
            self.maquinas.append(deque([vertice]))

        elif len(self.maquinas[-1]) < self.vertices_maquinas:
            # adiciona o vértice à última máquina
            self.maquinas[-1].append(vertice)

        elif len(self.maquinas[-1]) == self.vertices_maquinas and self.vertices_restantes:
            self.maquinas[-1].append(vertice)
            self.vertices_restantes -= 1

        elif not len(self.maquinas) == self.numero_maquinas:
            # Se a última máquina está cheia, cria uma nova máquina
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
        print("FO: ", self.fo)

    def salvar_solucao(self, nome_arquivo):
        with open(nome_arquivo, 'a') as arquivo:
            for i, maquina in enumerate(self.maquinas, start=1):
                linha = f"Máquina {i}: {list(maquina)}" + '\n'
                arquivo.write(linha)
            fo = f"FO: {self.fo}"
            arquivo.write(fo)

    def sucessores_viaveis(self, vertice):
        candidatos = self.grafo.vertices_sucessores(vertice)
        candidatos_viaveis = []
        for candidato in candidatos:
            candidato_apto = True
            anteriores = self.grafo.vertices_anteriores(candidato)
            if candidato in self.solucao:
                continue
            for anterior in anteriores:
                if anterior not in self.solucao:
                    candidato_apto = False
                    break
            if candidato_apto:
                candidatos_viaveis.append(candidato)
        return candidatos_viaveis

    def ultima_maquina(self, lista, indice):
        if indice == len(lista) - 1:
            return True
        else:
            return False


def calcular_fo(maquinas, pesos):
    maquinas_pesos = [sum(pesos[tarefa] for tarefa in maquina) for maquina in maquinas]
    return max(maquinas_pesos)


def escolha_aleatoria(lista):
    return random.choice(lista)
