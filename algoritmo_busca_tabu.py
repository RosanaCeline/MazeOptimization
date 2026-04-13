import numpy as np

TAMANHO = 5 # 5 x 5 células (25 no total)

# BUSCA TABU : evita loops usando memória
# HEURISTICA : a distância entre a posição atual e a saída do labirinto

def tabu_search(labirinto, inicio, fim, tamanho_tabu=10, bt_max=100):
    # começa no início
    atual = inicio
      # guarda no caminho
    caminho = [atual]
    
     # guarda posições proibidas 
    lista_tabu = []
    visitados = set([atual])
 
     # evita loop infinito
    for _ in range(bt_max):
        yield {
            "atual": atual,
            "visitados": set(visitados),
            "abertos": set(), 
            "caminho": None
        }
          # chegou na saída
        if atual == fim:
            break
      # separa coordenadas
        x, y = atual
         # cria lista de vizinhos
        vizinhos = []
         # cima , baixo , esquerda , direita 
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
        # Verifica se está dentro do limite 5x5 e se não é uma parede (0 = caminho livre, 1 = parede)
            if 0 <= nx < TAMANHO and 0 <= ny < TAMANHO:
                if labirinto[nx][ny] == 0:
                    vizinhos.append((nx, ny))
       # Filtra quem não está na lista tabu
        vizinhos_validos = [v for v in vizinhos if v not in lista_tabu]
        # se todos são tabu permite (escapar de bloqueio)
        if not vizinhos_validos:
            vizinhos_validos = vizinhos 
        # escolhe o melhor vizinho (heurística)
        # escolhe o vizinho mais próximo da saída
        melhor = min( vizinhos_validos, key=lambda v: abs(v[0] - fim[0]) + abs(v[1] - fim[1]))

        # atualiza tabu
        lista_tabu.append(atual)
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)
         # atualiza lista tabu ( add posição atual )
        atual = melhor
        caminho.append(atual)
        visitados.add(atual)
     # anda
    for i in range(len(caminho)):
        yield {
            "atual": caminho[i],
            "visitados": set(visitados),
            "abertos": set(),
            "caminho": caminho[:i+1]
        }