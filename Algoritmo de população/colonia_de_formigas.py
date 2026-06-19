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

    grafo = labirinto_em_grafo(labirinto)
    feromonio = [[1 for _ in range(len(labirinto))] for _ in range(len(labirinto))]
    melhor_caminho = None
    iteracoes = 0
    count_solucoes_iguais = 0

    while iteracoes < 100 and count_solucoes_iguais < 10: # número de iterações
        iteracoes += 1
        formigas_aptas = []

        for _ in range(20): # número de formigas
            print(f"\nFormiga {_ + 1}")
            ordem = [entrada]
            visitados = set()
            atual = entrada
            print(f"Atual: {atual}")

            while atual != saida:
                visitados.add(atual)
                vizinhos = []

                for vizinho in grafo[atual]:
                    if vizinho not in visitados:
                        heuristica_valor = 1 / (heuristica(vizinho, saida) + 1)
                        peso = (PESO_HEURISTICA * heuristica_valor) * (PESO_FEROMONIO * feromonio[vizinho[0]][vizinho[1]])
                        vizinhos.append((peso, vizinho))
                
                if len(vizinhos) == 0:
                    break

                print("Vizinhos:")
                for peso, vizinho in vizinhos:
                    print(f"  {vizinho} peso={peso:.4f}")
                atual = random.choices(vizinhos, weights=[v[0] for v in vizinhos], k=1)[0][1]
                ordem.append(atual)
                print(f"Escolhido: {atual}")

            if atual != saida:
                continue

            print("\nSaída encontrada!")
            print(f"Caminho: {ordem}")
            print(f"Tamanho: {len(ordem)}")

            # Atualiza feromônio
            for i in range(len(ordem)):
                x, y = ordem[i]
                feromonio[x][y] += 1.0 / len(ordem)

            print("\nFeromônio atualizado:")
            for pos in ordem:
                print(pos, feromonio[pos[0]][pos[1]])

            formigas_aptas.append((len(ordem), ordem))
        
        if len(formigas_aptas) > 0:
            formigas_aptas.sort(key=lambda x: x[0])
            if melhor_caminho is not None and formigas_aptas[0][0] == melhor_caminho[0]:
                count_solucoes_iguais += 1
            else:
                count_solucoes_iguais = 0
            melhor_caminho = formigas_aptas[0]
            print(f"\nMelhor caminho até agora: {melhor_caminho[1]} (tamanho {melhor_caminho[0]}) Geração: {iteracoes} Soluções iguais: {count_solucoes_iguais}")
        
