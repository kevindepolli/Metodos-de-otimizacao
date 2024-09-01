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


def busca_local(heuristica):
    pesos = heuristica.grafo.pesos
    solucao = heuristica.maquinas
    melhor_solucao = solucao
    fo = heuristica.fo
    fo_melhor = fo
    for i in range(len(heuristica.maquinas)):
        solucao_atual = vizinho(copy.deepcopy(solucao), i)
        fo_atual = calcular_fo(solucao_atual, pesos)
        fo_melhor = calcular_fo(melhor_solucao, pesos)
        if fo_atual < fo_melhor:
            melhor_solucao = solucao_atual
    heuristica.maquinas = melhor_solucao
    heuristica.fo = fo_melhor
