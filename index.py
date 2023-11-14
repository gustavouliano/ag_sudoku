import random
from sudoku import Sudoku

sudoku_modelo = Sudoku()

# Quais quadrantes deve-se comparar a linha entre eles
comparacao_linha = {0: [1, 2], 1: [2], 2: [], 3: [4, 5], 4: [5], 5: [], 6: [7, 8], 7: [8], 8: []}
# Quais quadrantes deve-se comparar a coluna entre eles
comparacao_coluna = {0: [3, 6], 1: [4, 7], 2: [5, 8], 3: [6], 4: [7], 5: [8], 6: [], 7: [], 8: []}

valor_possivel = [1, 2, 3, 4, 5, 6, 7, 8, 9]
tamanho_populacao = 100
num_geracoes = 1000

# Realiza a avaliação de fitness do indivíduo
def fitness(sudoku: Sudoku):
    cromossomo = sudoku.cromossomo
    fitness = 0
    for quadrante in range(9):
        # Avalia a regra de linhas
        for linha_quadrante in comparacao_linha[quadrante]:
            for index, linha in enumerate(cromossomo[quadrante]):
                for i in range(3):
                    if linha[i] != 0 and linha[i] in cromossomo[linha_quadrante][index]:
                        fitness += 1
        # Avalia a regra de colunas
        for i in range(3):
            coluna = [cromossomo[quadrante - 1][linha][i] for linha in range(3)]
            for coluna_quadrante in comparacao_coluna[quadrante]:
                coluna_compara = [cromossomo[coluna_quadrante - 1][linha][i] for linha in range(3)]
                for valor in coluna_compara:
                    if valor != 0 and valor in coluna:
                        fitness += 1
        # Avalia a regra de quadrante
        for valor in valor_possivel:
            contador = 0
            for linha in cromossomo[quadrante]:
                contador += linha.count(valor)
            if contador > 1:
                fitness += contador - 1
    sudoku.fitness = fitness

# Inicializa a população inicial com valores aleatórios
def geraPopulacaoInicial():
    populacao = []
    for _ in range(tamanho_populacao):
        sudoku = Sudoku()
        cromossomo = sudoku.cromossomo
        for quadrante in range(9):
            for i in range(3):
                for j in range(3):
                    if cromossomo[quadrante][i][j] == 0:
                        cromossomo[quadrante][i][j] = random.choice(valor_possivel)
                        fitness(sudoku)
        populacao.append(sudoku)
    return populacao

# Seleciona um indivíduo utiliazando o método da roleta (quanto melhor o fitness, maior a chance)
def selecao_pais_roleta(populacao) -> Sudoku:
    fitness_total = sum(1 / (abs(individuo.fitness) + 1) for individuo in populacao)
    roleta = random.uniform(0, fitness_total)
    soma_fitness = 0
    for index, individuo in enumerate(populacao):
        probabilidade = 1 / (abs(individuo.fitness) + 1)
        soma_fitness += probabilidade
        if soma_fitness >= roleta:
            return populacao.pop(index)

# Realiza o método de mutação, com 0,5% de chance para cada gene do indivíduo
def mutacao(filho: Sudoku, sudoku_modelo: Sudoku):
    for i in range(9):
        for j in range(3):
            for k in range(3):
                if filho.cromossomo[i][j][k] != sudoku_modelo.cromossomo[i][j][k] and random.randint(1, 200) == 1:
                    novo_valor = random.choice([valor for valor in valor_possivel if valor != filho.cromossomo[i][j][k]])
                    filho.cromossomo[i][j][k] = novo_valor

# Realiza o método uniforme de crossover
def crossover_uniforme(pai1: Sudoku, pai2: Sudoku):
    filho1 = Sudoku()
    filho2 = Sudoku()
    for i in range(9):
        for j in range(3):
            for k in range(3):
                # Escolhe aleatoriamente de qual pai herdar o valor para filho1
                if random.choice([True, False]):
                    filho1.cromossomo[i][j][k] = pai1.cromossomo[i][j][k]
                else:
                    filho1.cromossomo[i][j][k] = pai2.cromossomo[i][j][k]

                # Escolhe aleatoriamente de qual pai herdar o valor para filho2
                if random.choice([True, False]):
                    filho2.cromossomo[i][j][k] = pai1.cromossomo[i][j][k]
                else:
                    filho2.cromossomo[i][j][k] = pai2.cromossomo[i][j][k]
    return filho1, filho2

# Realiza o crossover na população
def crossover(populacao, sudoku_modelo):
    pai1 = selecao_pais_roleta(populacao)
    pai2 = selecao_pais_roleta(populacao)
    filho1, filho2 = crossover_uniforme(pai1, pai2)
    mutacao(filho1, sudoku_modelo)
    mutacao(filho2, sudoku_modelo)
    return filho1, filho2

# Realiza o método de elitismo, selecionado os melhores pais da população conforme proporção especificada
def elitismo(populacao, tamanho_populacao, proporcao_elitismo = 0.1):
    num_elites = int(tamanho_populacao * proporcao_elitismo)
    return sorted(populacao, key=lambda x: x.fitness)[:num_elites]

# Retorna o indivíduo com o melhor fitness
def menorFitness(populacao: list[Sudoku]) -> Sudoku:
    return min(populacao, key=lambda x: x.fitness)

populacao = geraPopulacaoInicial()
for geracao in range(num_geracoes):
    populacao_pais = populacao.copy()
    populacao = []
    populacao.extend(elitismo(populacao_pais, tamanho_populacao))
    for i in range(int(tamanho_populacao / 2)):
        filho1, filho2 = crossover(populacao_pais, sudoku_modelo)
        fitness(filho1)
        fitness(filho2)
        populacao.append(filho1)
        populacao.append(filho2)

melhor_individuo = menorFitness(populacao)
print(f"Fitness: {melhor_individuo.fitness}")
print(melhor_individuo.cromossomo)
