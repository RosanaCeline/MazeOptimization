import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import random
from collections import deque

import colonia_de_formigas as formigas

CMAP = LinearSegmentedColormap.from_list(
    "feromonio",
    ["white", "#FFFF66", "#FFD700", "#FFA500"]
)

TAMANHO = 10
PORCENTAGEM_BLOQUEIOS = 0.32
ENTRADA = (0, 0)
SAIDA = (TAMANHO-1, TAMANHO-1)

def gerar_labirinto():
    while True:
        labirinto = np.zeros((TAMANHO, TAMANHO)) 
        quantidade_bloqueios = int(TAMANHO * TAMANHO * PORCENTAGEM_BLOQUEIOS)

        bloqueios = set()

        while len(bloqueios) < quantidade_bloqueios:
            celula = (random.randint(0, TAMANHO-1), random.randint(0, TAMANHO-1))
            if celula != ENTRADA and celula != SAIDA:
                bloqueios.add(celula)

        for (i, j) in bloqueios:
            labirinto[i][j] = 1 
        
        if existe_caminho(labirinto):
            return labirinto

def existe_caminho(labirinto):
    visitados = set()
    fila = deque([ENTRADA])

    visitados.add(ENTRADA)

    while fila:
        x, y = fila.popleft()

        if (x, y) == SAIDA:
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < TAMANHO and 0 <= ny < TAMANHO:
                if labirinto[nx][ny] == 0 and (nx, ny) not in visitados:
                    fila.append((nx, ny))
                    visitados.add((nx, ny))

    return False

def on_close(event):
    global running
    running = False

def mostrar_labirinto(labirinto, title = f"Labirinto {TAMANHO}x{TAMANHO}", gerador_factory=None, intervalo=0.3):
    global running
    running = True
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.canvas.mpl_connect('close_event', on_close)

    legenda = [
        Patch(facecolor='white',   edgecolor='gray', label='Sem feromônio'),
        Patch(facecolor='#FFFF99', edgecolor='gray', label='Feromônio fraco'),
        Patch(facecolor='#FFD700', edgecolor='gray', label='Feromônio forte'),
        Patch(facecolor='orange',  alpha=0.9,        label='Formiga atual'),
        Patch(facecolor='red',     alpha=0.9,        label='Melhor caminho'),
        Patch(facecolor='black',                     label='Parede'),
    ]

    # Desenhar grade
    ax.imshow(labirinto, cmap='gray_r')
    ax.set_xticks(np.arange(-0.5, TAMANHO, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, TAMANHO, 1), minor=True)
    ax.grid(which="minor", linestyle='-', linewidth=2)

    # Entrada e saída
    ax.text(ENTRADA[1], ENTRADA[0], 'E', ha='center', va='center')
    ax.text(SAIDA[1], SAIDA[0], 'S', ha='center', va='center')

    gerador = gerador_factory()
    ultimo_estado = None
        
    for estado in gerador:
        if not running:
            break

        ultimo_estado = estado
        ax.clear()

        feromonio = estado["feromonio"]
        formiga   = estado["formiga_atual"]
        caminho_f = estado["caminho_formiga"]
        melhor    = estado["melhor_caminho"]
        iteracao  = estado["iteracao"]
        fase      = estado["fase"]
        tamanho   = len(labirinto)

        ax.imshow(labirinto, cmap='gray_r')

        # Normalização do feromônio sobre células livres
        valores_livres = [
            feromonio[i][j]
            for i in range(tamanho)
                for j in range(tamanho)
                    if labirinto[i][j] == 0
        ]
           
        f_min = min(valores_livres)
        f_max = max(valores_livres)
        if f_max == f_min:
            f_max = f_min + 0.001

        norm = mcolors.Normalize(vmin=f_min, vmax=f_max)
        cmap = CMAP
            
        # Colorir células livres pelo feromônio
        for i in range(tamanho):
            for j in range(tamanho):
                if labirinto[i][j] == 0:
                    valor = feromonio[i][j]
                    if valor <= f_min + 0.001:
                        cor = 'white'
                    else:
                        cor = cmap(norm(valor))
                    ax.add_patch(plt.Rectangle(
                        (j - 0.5, i - 0.5), 1, 1,
                        color=cor, alpha=0.85, zorder=2
                    ))

        # Trilha da formiga em movimento
        if fase == "movimento" and caminho_f:
            for (x, y) in caminho_f[:-1]:
                ax.add_patch(plt.Rectangle(
                    (y - 0.5, x - 0.5), 1, 1,
                    color='orange', alpha=0.4, zorder=3
                ))
            if formiga:
                fx, fy = formiga
                ax.add_patch(plt.Rectangle(
                    (fy - 0.5, fx - 0.5), 1, 1,
                    color='orange', alpha=0.95, zorder=4
                ))

        # Melhor caminho em vermelho
        if melhor:
            for (x, y) in melhor[1]:
                ax.plot(y, x, marker='o', color='red', markersize=6, zorder=5)

        # Desenhar grade
        ax.set_xticks(np.arange(-0.5, TAMANHO, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, TAMANHO, 1), minor=True)
        ax.grid(which="minor", linestyle='-', linewidth=1.5, color='gray')

        # Entrada e saída
        ax.text(ENTRADA[1], ENTRADA[0], 'E', ha='center', va='center')
        ax.text(SAIDA[1], SAIDA[0], 'S', ha='center', va='center')
            
        ax.set_title(f"{title} | Iteração {iteracao}")
        ax.legend(handles=legenda, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)

        plt.pause(intervalo)

    if ultimo_estado and ultimo_estado["melhor_caminho"]:
        ax.clear()
        melhor = ultimo_estado["melhor_caminho"]
        feromonio = ultimo_estado["feromonio"]
        tamanho = len(labirinto)

        ax.imshow(labirinto, cmap='gray_r')

        # Feromônio (igual ao loop)
        valores_livres = [
            feromonio[i][j]
            for i in range(tamanho)
            for j in range(tamanho)
            if labirinto[i][j] == 0
        ]
        f_min = min(valores_livres)
        f_max = max(valores_livres) if max(valores_livres) != min(valores_livres) else f_min + 0.001
        norm = mcolors.Normalize(vmin=f_min, vmax=f_max)
        for i in range(tamanho):
            for j in range(tamanho):
                if labirinto[i][j] == 0:
                    valor = feromonio[i][j]
                    cor = 'white' if valor <= f_min + 0.001 else CMAP(norm(valor))
                    ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, color=cor, alpha=0.85, zorder=2))

        # Melhor caminho em vermelho destacado
        for (x, y) in melhor[1]:
            ax.plot(y, x, marker='o', color='red', markersize=10, zorder=5)

        ax.set_xticks(np.arange(-0.5, tamanho, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, tamanho, 1), minor=True)
        ax.grid(which="minor", linestyle='-', linewidth=1.5, color='gray')
        ax.text(ENTRADA[1], ENTRADA[0], 'E', ha='center', va='center', fontweight='bold')
        ax.text(SAIDA[1],   SAIDA[0],   'S', ha='center', va='center', fontweight='bold')
        ax.set_title(f"{title} | Melhor caminho encontrado: {melhor[0]} passos")
        ax.legend(handles=legenda, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
        plt.draw()
        
    plt.show()

labirinto = gerar_labirinto()

mostrar_labirinto(
    labirinto,
    gerador_factory=lambda: formigas.colonia_de_formigas(labirinto, ENTRADA, SAIDA),
    title="Colônia de Formigas",
    intervalo=0.3
)