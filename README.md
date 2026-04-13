# Labirinto 5x5 com Busca de Caminho

## Descrição

Este projeto implementa a geração de um labirinto em grade 5x5, contendo células livres e bloqueadas, com o objetivo de encontrar um caminho entre a entrada e a saída.

A entrada está localizada na posição (0,0) e a saída na posição (4,4). O labirinto é gerado aleatoriamente, com aproximadamente 32% das células bloqueadas, garantindo que exista pelo menos um caminho válido entre os dois pontos.

## Funcionalidades

- Geração aleatória de labirinto 5x5
- Controle de células bloqueadas (32%)
- Verificação de existência de caminho utilizando BFS (Breadth-First Search)
- Visualização do labirinto com Matplotlib
- Integração com algoritmos de busca (A\*, entre outros)

## Estrutura do Projeto

- main.py: geração do labirinto, validação e visualização
- algoritmo_a_star.py: implementação do algoritmo A\*
- algoritmo_busca_tabu.py: implementação do algoritimo Busca tabu.

## Tecnologias Utilizadas

- Python
- NumPy
- Matplotlib

## Como Executar

1. Instale as dependências:

```bash
pip install numpy matplotlib
```

2. Execute o arquivo principal:

```bash
python main.py
```
