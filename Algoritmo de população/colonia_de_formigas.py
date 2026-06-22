from heapq import heappush, heappop
import random

def labirinto_em_grafo(labirinto):
    grafo = {}
    tamanho = len(labirinto)

    for i in range(tamanho):
        for j in range(tamanho):
            if labirinto[i][j] == 0: 
                vizinhos = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < tamanho and 0 <= ny < tamanho and labirinto[nx][ny] == 0:
                        vizinhos.append((nx, ny))
                grafo[(i, j)] = vizinhos

    return grafo

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def colonia_de_formigas(labirinto, entrada, saida):
    PESO_HEURISTICA = 1.0
    PESO_FEROMONIO = 1.0
    TAXA_EVAPORACAO = 0.1 

    grafo = labirinto_em_grafo(labirinto)
    tamanho = len(labirinto)
    feromonio = [[1 for _ in range(tamanho)] for _ in range(tamanho)]
    melhor_caminho = None
    iteracoes = 0
    count_solucoes_iguais = 0

    while iteracoes < 100 and count_solucoes_iguais < 10: # número de iterações
        iteracoes += 1
        formigas_aptas = []

        for _ in range(20): # número de formigas
            ordem = [entrada]
            visitados = set()
            atual = entrada

            while atual != saida:
                visitados.add(atual)
                vizinhos = []

                for vizinho in grafo[atual]:
                    if vizinho not in visitados:
                        heuristica_valor = 1 / (heuristica(vizinho, saida) + 1)
                        peso = (feromonio[vizinho[0]][vizinho[1]] ** PESO_FEROMONIO) * (heuristica_valor ** PESO_HEURISTICA)
                        vizinhos.append((peso, vizinho))
                
                if len(vizinhos) == 0:
                    break

                atual = random.choices(vizinhos, weights=[v[0] for v in vizinhos], k=1)[0][1]
                ordem.append(atual)

            if atual != saida:
                continue

            formigas_aptas.append((len(ordem), ordem))

        # Evaporação global
        for i in range(tamanho):
            for j in range(tamanho):
                feromonio[i][j] = max(0.1, feromonio[i][j] * (1 - TAXA_EVAPORACAO))

        # Depósito apenas das formigas que chegaram à saída
        for tamanho_caminho, caminho in formigas_aptas:
            for x, y in caminho:
                feromonio[x][y] += 1.0 / tamanho_caminho
        
        if len(formigas_aptas) > 0:
            formigas_aptas.sort(key=lambda x: x[0])
            if melhor_caminho is not None and formigas_aptas[0][0] == melhor_caminho[0]:
                count_solucoes_iguais += 1
            else:
                count_solucoes_iguais = 0
            melhor_caminho = formigas_aptas[0]
            
        yield {
            "feromonio": feromonio,
            "formiga_atual": None,
            "caminho_formiga": [],
            "melhor_caminho": melhor_caminho,
            "iteracao": iteracoes,
            "fase": "iteracao_concluida"
        }
