import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import random
from collections import deque

import algoritmo_a_star as star
import algoritmo_x as x

TAMANHO = 5 # 5 x 5 células (25 no total)
PORCENTAGEM_BLOQUEIOS = 0.32
ENTRADA = (0, 0)
SAIDA = (TAMANHO-1, TAMANHO-1)

# Cria um labirinto
def gerar_labirinto():
    while True:
        labirinto = np.zeros((TAMANHO, TAMANHO)) # Cria uma matriz 5x5 com zeros (células livres)
        quantidade_bloqueios = int(TAMANHO * TAMANHO * PORCENTAGEM_BLOQUEIOS)

        bloqueios = set()

        # Sorteia células bloqueadas
        while len(bloqueios) < quantidade_bloqueios:
            celula = (random.randint(0, TAMANHO-1), random.randint(0, TAMANHO-1))
            if celula != ENTRADA and celula != SAIDA:
                bloqueios.add(celula)

        for (i, j) in bloqueios:
            labirinto[i][j] = 1 # 1 - célula bloqueada
        
        if existe_caminho(labirinto):
            return labirinto

# Verifica se existe caminho (BFS)
def existe_caminho(labirinto):
    visitados = set()
    fila = deque([ENTRADA])

    visitados.add(ENTRADA)

    while fila:
        x, y = fila.popleft()

        # Se chegou na saída = existe caminho
        if (x, y) == SAIDA:
            return True

        # Movimentos possíveis: cima, baixo, esquerda, direita
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # Verifica se está dentro do labirinto
            if 0 <= nx < TAMANHO and 0 <= ny < TAMANHO:
                
                # Verifica se é livre e não foi visitado
                if labirinto[nx][ny] == 0 and (nx, ny) not in visitados:
                    fila.append((nx, ny))
                    visitados.add((nx, ny))

    # Se explorou tudo e não chegou = não existe caminho
    return False

# Apenas vai controlar quando fechar a janela do matplotlib para parar a animação
def on_close(event):
    global running
    running = False

# Mostra o labirinto com matplotlib
def mostrar_labirinto(labirinto, caminho=None, title="Labirinto 5x5", gerador_factory=None, intervalo=0.3):
    # Variável global para controlar o loop da animação
    global running
    running = True
    
    # Define o tamanho da figura e conecta o evento de fechamento
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.canvas.mpl_connect('close_event', on_close)

    # Desenhar grade
    ax.imshow(labirinto, cmap='gray_r')
    ax.set_xticks(np.arange(-0.5, TAMANHO, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, TAMANHO, 1), minor=True)
    ax.grid(which="minor", linestyle='-', linewidth=2)

    # Entrada e saída
    ax.text(ENTRADA[1], ENTRADA[0], 'E', ha='center', va='center')
    ax.text(SAIDA[1], SAIDA[0], 'S', ha='center', va='center')

    # Caminho
    if caminho:
        for (x, y) in caminho:
            ax.plot(y, x, marker='o')

    # modo animado (se usar algoritmo)
    if gerador_factory:

        # Define a legenda das cores para cada estado do algoritmo
        legenda = [
            Patch(facecolor='skyblue', alpha=0.6, label='Visitado'),
            Patch(facecolor='yellow',  alpha=0.7, label='Vizinho (na fila/ em aberto)'),
            Patch(facecolor='orange',  alpha=0.9, label='Expandindo agora'),
            Patch(facecolor='red',     alpha=0.9, label='Caminho final'),
            Patch(facecolor='black',   alpha=0.9, label='Parede'),
        ]

        # Enquanto a janela estiver aberta, continua a animação
        while running:

            # Cria o gerador do algoritmo (que vai produzindo os estados passo a passo)
            gerador = gerador_factory()

            # Para cada estado produzido pelo algoritmo, atualiza a visualização
            for estado in gerador:
                # Se a janela foi fechada, para a animação
                if not running:
                    break

                # Limpa o gráfico para desenhar o próximo estado (pra poder mudar de cor devidamente em cada quadradinho)
                ax.clear()

                # Desenhar grade
                ax.imshow(labirinto, cmap='gray_r')
                ax.set_xticks(np.arange(-0.5, TAMANHO, 1), minor=True)
                ax.set_yticks(np.arange(-0.5, TAMANHO, 1), minor=True)
                ax.grid(which="minor", linestyle='-', linewidth=2)

                # Entrada e saída
                ax.text(ENTRADA[1], ENTRADA[0], 'E', ha='center', va='center')
                ax.text(SAIDA[1], SAIDA[0], 'S', ha='center', va='center')

                # Animar caminho com as cores (vai pintar o quadradinho de acordo com o estado do algoritmo)
                # Bloco Visitados = azul
                for (x, y) in estado["visitados"]:
                    ax.add_patch(plt.Rectangle((y-0.5, x-0.5), 1, 1, color='skyblue', alpha=0.6, zorder=2))

                # Bloco Abertos (na fila) = amarelo 
                for (x, y) in estado["abertos"]:
                    ax.add_patch(plt.Rectangle((y-0.5, x-0.5), 1, 1, color='yellow', alpha=0.7, zorder=2))

                # Bloco Expandindo agora = laranja
                if estado["caminho"] is None:
                    cx, cy = estado["atual"]
                    ax.add_patch(plt.Rectangle((cy-0.5, cx-0.5), 1, 1, color='orange', alpha=0.9, zorder=3))

                # Bloco Caminho final = pontinho vermelho
                if estado["caminho"]:
                    for (x, y) in estado["caminho"]:
                        ax.plot(y, x, marker='o', color='red', zorder=4)

                # Adiciona a legenda do gráfico 
                ax.legend(handles=legenda, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
                # Pausa para criar a animação (acelerar ou desacelerar a animação)
                plt.pause(intervalo)
            
            # Pausa final para mostrar o caminho final, logo após começa o loop novamente
            plt.pause(1)

    ax.set_title(title)
    plt.show()

labirinto = gerar_labirinto()
print(labirinto)

mostrar_labirinto(labirinto)
mostrar_labirinto(labirinto, gerador_factory=lambda: star.algoritmo_a_star(labirinto, ENTRADA, SAIDA), title="Labirinto com A*")

# caminho_x = x.funcao(labirinto, ENTRADA, SAIDA)
# mostrar_labirinto(labirinto, caminho_x, "Labirinto com o Algoritmo X")
