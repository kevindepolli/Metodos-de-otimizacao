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
