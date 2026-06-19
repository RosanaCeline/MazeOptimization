from heapq import heappush, heappop

def labirinto_em_grafo(labirinto):
    grafo = {}
    tamanho = len(labirinto)

    for i in range(tamanho):
        for j in range(tamanho):
            if labirinto[i][j] == 0: # Se a célula é livre
                vizinhos = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < tamanho and 0 <= ny < tamanho and labirinto[nx][ny] == 0:
                        vizinhos.append((nx, ny))
                grafo[(i, j)] = vizinhos

    return grafo

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def algoritmo_a_star(labirinto, entrada, saida):
    grafo = labirinto_em_grafo(labirinto)

    fila = []
    heappush(fila, (0, entrada))

    veio_de = {}
    custo = {entrada: 0}

    visitados = set() # rastrear visitados
    abertos = {entrada} # rastrear a fila de abertos

    while fila:
        _, atual = heappop(fila)

        if atual in visitados:
            continue
            
        visitados.add(atual)
        abertos.discard(atual)

        if atual == saida:
            break

        for vizinho in grafo[atual]:
            novo_custo = custo[atual] + 1

            if vizinho not in custo or novo_custo < custo[vizinho]:
                custo[vizinho] = novo_custo
                prioridade = novo_custo + heuristica(vizinho, saida)
                heappush(fila, (prioridade, vizinho))
                veio_de[vizinho] = atual
                abertos.add(vizinho)
        
        yield {
            "atual": atual,
            "visitados": set(visitados),
            "abertos": set(abertos),
            "caminho": None
        }

    # reconstrução do caminho
    caminho = []
    atual = saida

    while atual != entrada:
        caminho.append(atual)
        atual = veio_de.get(atual)
        if atual is None:  # saida inalcançável
            break

    caminho.append(entrada)
    caminho.reverse()

    yield {
        "atual": saida,
        "visitados": set(visitados),
        "abertos": set(),
        "caminho": caminho
    }

    return caminho