import numpy as np

# heurística (distância de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def tabu_search(labirinto, inicio, fim, tamanho_tabu=5, bt_max=100):
    atual = inicio
    caminho = [atual]
    tamanho = len(labirinto)
    lista_tabu = []
    visitados = set([atual])
    melhor_global = atual 

    # limite de passos (evita loop infinito 
    for _ in range(bt_max):
        yield {
            "atual": atual,
            "visitados": set(visitados),
            "abertos": set(),
            "caminho": None
        }

        if atual == fim:
            break

        x, y = atual

        vizinhos = []
        # gera movimentos: cima, baixo, esquerda, direita
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # verifica limites e se não é parede
            if 0 <= nx < tamanho and 0 <= ny < tamanho:
                if labirinto[nx][ny] == 0:
                    vizinhos.append((nx, ny))

        # remove da lista de vizinhos aqueles que estão na lista tabu
        vizinhos_validos = [v for v in vizinhos if v not in lista_tabu]

        # evita voltar para o passo anterior 
        if len(caminho) > 1:
            ultimo = caminho[-2]
            vizinhos_validos = [v for v in vizinhos_validos if v != ultimo]

        # estratégia de escape
        if not vizinhos_validos:
            vizinhos_validos = vizinhos

        # escolhe o melhor vizinho
        melhor = min(vizinhos_validos, key=lambda v: heuristica(v, fim))

        # adiciona posição atual na lista tabu
        lista_tabu.append(atual)
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)
        
        # anda para o melhor vizinho
        atual = melhor
        caminho.append(atual)
        visitados.add(atual)
       
        # atualiza melhor posição já encontrada
        if heuristica(atual, fim) < heuristica(melhor_global, fim):
            melhor_global = atual

    
    for i in range(len(caminho)):
        yield {
            "atual": caminho[i],
            "visitados": set(visitados),
            "abertos": set(),
            "caminho": caminho[:i+1]
        }