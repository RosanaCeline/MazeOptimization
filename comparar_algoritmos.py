import os
import sys
import time
import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np

import algoritmo_a_star as star
import algoritmo_busca_tabu as tabu

sys.path.append(os.path.join(os.path.dirname(__file__), "Algoritmo de população"))
import colonia_de_formigas as formigas

TAMANHO = 10
PORCENTAGEM_BLOQUEIOS = 0.32
ENTRADA = (0, 0)
SAIDA = (TAMANHO - 1, TAMANHO - 1)


def gerar_labirinto():
    while True:
        labirinto = np.zeros((TAMANHO, TAMANHO))
        quantidade_bloqueios = int(TAMANHO * TAMANHO * PORCENTAGEM_BLOQUEIOS)

        bloqueios = set()
        while len(bloqueios) < quantidade_bloqueios:
            celula = (random.randint(0, TAMANHO - 1), random.randint(0, TAMANHO - 1))
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


def executar_a_star(labirinto):
    inicio = time.perf_counter()
    estado_final = None
    for estado in star.algoritmo_a_star(labirinto, ENTRADA, SAIDA):
        estado_final = estado
    tempo = time.perf_counter() - inicio

    caminho = estado_final["caminho"] or []
    return {
        "nome": "A*",
        "tempo": tempo,
        "passos": len(caminho) - 1 if caminho else None,
        "visitados": len(estado_final["visitados"]),
        "sucesso": bool(caminho) and caminho[-1] == SAIDA,
    }


def executar_tabu(labirinto):
    inicio = time.perf_counter()
    estado_final = None
    for estado in tabu.tabu_search(labirinto, ENTRADA, SAIDA):
        estado_final = estado
    tempo = time.perf_counter() - inicio

    caminho = estado_final["caminho"] or []
    return {
        "nome": "Busca Tabu",
        "tempo": tempo,
        "passos": len(caminho) - 1 if caminho else None,
        "visitados": len(estado_final["visitados"]),
        "sucesso": bool(caminho) and caminho[-1] == SAIDA,
    }


def executar_colonia(labirinto):
    inicio = time.perf_counter()
    estado_final = None
    for estado in formigas.colonia_de_formigas(labirinto, ENTRADA, SAIDA):
        estado_final = estado
    tempo = time.perf_counter() - inicio

    melhor = estado_final["melhor_caminho"]
    tamanho_caminho, caminho = melhor if melhor else (None, [])
    return {
        "nome": "Colônia de Formigas",
        "tempo": tempo,
        "passos": tamanho_caminho - 1 if tamanho_caminho else None,
        "visitados": len(estado_final.get("visitados", set())),
        "sucesso": bool(caminho) and caminho[-1] == SAIDA,
    }


def mostrar_resultados(resultados):
    print(f"\n{'Algoritmo':<22} | {'Sucesso':<7} | {'Tempo (s)':>10} | {'Passos':>7} | {'Visitados':>9}")
    print("-" * 70)
    for r in resultados:
        sucesso = "Sim" if r["sucesso"] else "Não"
        passos = r["passos"] if r["passos"] is not None else "-"
        print(f"{r['nome']:<22} | {sucesso:<7} | {r['tempo']:>10.5f} | {str(passos):>7} | {r['visitados']:>9}")

    nomes = [r["nome"] for r in resultados]
    tempos = [r["tempo"] for r in resultados]
    passos = [r["passos"] or 0 for r in resultados]
    visitados = [r["visitados"] for r in resultados]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].bar(nomes, tempos, color="skyblue")
    axs[0].set_title("Tempo de execução (s)")

    axs[1].bar(nomes, passos, color="orange")
    axs[1].set_title("Tamanho do caminho final (passos)")

    axs[2].bar(nomes, visitados, color="salmon")
    axs[2].set_title("Células exploradas")

    for ax in axs:
        ax.tick_params(axis="x", rotation=20)

    plt.tight_layout()
    plt.show()


def rodar_multiplas_execucoes(n_execucoes):
    execucoes = {"A*": [], "Busca Tabu": [], "Colônia de Formigas": []}

    for i in range(n_execucoes):
        labirinto = gerar_labirinto()
        for resultado in (
            executar_a_star(labirinto),
            executar_tabu(labirinto),
            executar_colonia(labirinto),
        ):
            execucoes[resultado["nome"]].append(resultado)
        print(f"Execução {i + 1}/{n_execucoes} concluída")

    return execucoes


def calcular_estatisticas(execucoes):
    nomes = list(execucoes.keys())

    tempos_media = [np.mean([r["tempo"] for r in execucoes[n]]) for n in nomes]
    tempos_std = [np.std([r["tempo"] for r in execucoes[n]]) for n in nomes]

    passos_validos = [[r["passos"] for r in execucoes[n] if r["passos"] is not None] for n in nomes]
    passos_media = [np.mean(p) if p else 0 for p in passos_validos]
    passos_std = [np.std(p) if p else 0 for p in passos_validos]

    visitados_media = [np.mean([r["visitados"] for r in execucoes[n]]) for n in nomes]
    visitados_std = [np.std([r["visitados"] for r in execucoes[n]]) for n in nomes]

    taxa_sucesso = [100 * np.mean([r["sucesso"] for r in execucoes[n]]) for n in nomes]

    return {
        "nomes": nomes,
        "tempos_media": tempos_media,
        "tempos_std": tempos_std,
        "passos_media": passos_media,
        "passos_std": passos_std,
        "visitados_media": visitados_media,
        "visitados_std": visitados_std,
        "taxa_sucesso": taxa_sucesso,
    }


def salvar_grafico_metrica(nomes, valores, std, titulo, cor, caminho_png, ylim=None):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(nomes, valores, yerr=std, color=cor, capsize=5)
    ax.set_title(titulo)
    ax.tick_params(axis="x", rotation=20)
    if ylim:
        ax.set_ylim(*ylim)
    plt.tight_layout()
    plt.savefig(caminho_png)
    plt.close(fig)
    print(f"Gráfico salvo em: {caminho_png}")


def salvar_tabela_comparativa(stats, caminho_png):
    nomes = stats["nomes"]
    colunas = ["Algoritmo", "Tempo médio (s)", "Passos médios", "Visitados (médio)", "Sucesso (%)"]
    linhas = [
        [
            nomes[i],
            f"{stats['tempos_media'][i]:.5f}",
            f"{stats['passos_media'][i]:.1f}",
            f"{stats['visitados_media'][i]:.1f}",
            f"{stats['taxa_sucesso'][i]:.1f}",
        ]
        for i in range(len(nomes))
    ]

    fig, ax = plt.subplots(figsize=(9, 1 + 0.6 * len(nomes)))
    ax.axis("off")
    tabela = ax.table(cellText=linhas, colLabels=colunas, loc="center", cellLoc="center")
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(11)
    tabela.scale(1, 1.8)
    plt.tight_layout()
    plt.savefig(caminho_png, bbox_inches="tight")
    plt.close(fig)
    print(f"Tabela salva em: {caminho_png}")


if __name__ == "__main__":
    N_EXECUCOES = 20
    PASTA_SAIDA = "output"
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    execucoes = rodar_multiplas_execucoes(N_EXECUCOES)
    stats = calcular_estatisticas(execucoes)

    salvar_grafico_metrica(
        stats["nomes"], stats["tempos_media"], stats["tempos_std"],
        "Tempo médio de execução (s)", "skyblue",
        os.path.join(PASTA_SAIDA, "tempo_execucao.png"),
    )
    salvar_grafico_metrica(
        stats["nomes"], stats["passos_media"], stats["passos_std"],
        "Tamanho médio do caminho final (passos)", "orange",
        os.path.join(PASTA_SAIDA, "passos_caminho.png"),
    )
    salvar_grafico_metrica(
        stats["nomes"], stats["visitados_media"], stats["visitados_std"],
        "Média de células exploradas", "salmon",
        os.path.join(PASTA_SAIDA, "celulas_exploradas.png"),
    )
    salvar_grafico_metrica(
        stats["nomes"], stats["taxa_sucesso"], None,
        "Taxa de sucesso (%)", "seagreen",
        os.path.join(PASTA_SAIDA, "taxa_sucesso.png"), ylim=(0, 100),
    )
    salvar_tabela_comparativa(stats, os.path.join(PASTA_SAIDA, "tabela_comparativa.png"))
