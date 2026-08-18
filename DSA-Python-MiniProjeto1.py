# Manipulação de dados
from matplotlib import ticker
import pandas as pd

# operações matemáticas e arrays
import numpy as np

# geração de gráficos
import matplotlib.pyplot as plt

# visualização estatística de dados - roda por cima do matplotlib
import seaborn as sns

# numeros aleatórios
import random

# manipulação de datas e intervalos de tempo
from datetime import datetime, timedelta

def dsa_gera_dados_ficticios(num_registros = 600):
    # Gera um DataFrame do Pandas com dados de vendas fictícios

    print(f"\nIniciando geração de {num_registros} registros de vendas...")

    #Dicionário com produtos, suas categorias e preços
    produtos = {
        'LaptopGamer': {'categoria': 'Eletrônicos', 'preco': 7500.00},
        'Mouse Vertical': {'categoria': 'Acessórios', 'preco': 250.00},
        'Teclado Mecânico' : {'categoria': 'Eletrônicos', 'preco': 550.00},
        'Monitor Ultrawide': {'categoria': 'Eletrônicos', 'preco': 2800.00},
        'Cadeira Gamer': {'categoria': 'Móveis', 'preco': 1200.00},
        'Headset 7.1': {'categoria': 'Acessórios', 'preco': 800.00},
        'Placa de Vídeo': {'categoria': 'Hardware', 'preco': 4500.00},
        'SSD 1TB': {'categoria': 'Hardware', 'preco': 600.00}
    }

    # nomes dos produtos
    lista_produtos = list(produtos.keys())

    cidades_estados = {
        'São Paulo': 'SP', 'Rio de Janeiro': 'RJ', 'Belo Horizonte': 'MG', 'Porto Alegre': 'RS', 'Salvador': 'BA', 'Curitiba': 'PR', 'Fortaleza': 'CE'
    }

    lista_cidades = list(cidades_estados.keys())

    dados_vendas = []

    data_inicial = datetime(2026,1,1)

    for i in range(num_registros):
        produto_nome = random.choice(lista_produtos)

        cidade = random.choice(lista_cidades)

        quantidade = np.random.randint(1, 8)

        #calcula a data do pedido a partir da data inicial
        data_pedido = data_inicial + timedelta(days = int(i/5), hours = random.randint(0,23))

        #se produtor for mouse ou teclado, aplica desconto aleatório de até 10%
        if produto_nome in ['Mouse Vertical', 'Teclado Mecânico']:
            # usa numeros aleatórios pelo pacote no numpy - np
            preco_unitario = produtos[produto_nome]['preco'] * np.random.uniform(0.9, 1.0) 
        else:
            preco_unitario = produtos[produto_nome]['preco']

        #adiciona o registro à lista de venda
        dados_vendas.append({
            'ID_Pedido': 1000 + i,
            'Data_Pedido': data_pedido,
            'Nome_Produto':  produto_nome,
            'Categoria': produtos[produto_nome]['categoria'],
            'Preco_Unitario': round(preco_unitario, 2),
            'Quantidade': quantidade,
            'ID_Cliente': np.random.randint(100,150),
            'Cidade': cidade,
            'Estado': cidades_estados[cidade]
        })

    print('Geração de dados concluída')

    return pd.DataFrame(dados_vendas) 
    #data frame do pandas é formato tabela


df_vendas = dsa_gera_dados_ficticios(500)

#shape mostra a quantidade de linhas e colunas do dataframe
print('shape')
print(df_vendas.shape)

#exibe as 5 primeiras linhas do dataframe
print('5 primeiras linhas')
print(df_vendas.head())

#exibe as 5 ultimas linhas
print('5 ultimas linhas')
print(df_vendas.tail())

#exibe informações gerais do dataframe
print('informações gerais')
print(df_vendas.info())

#resumo estatístico das colunas numéricas do dataframe - numéricas ou tipo data - colunas do tipo object não entram no resumo estatístico
print('resumo estatístico')
print(df_vendas.describe())

#tipos de dados das colunas do dataframe - os tratamentos serão de acordo com o tipo de dado da coluna
print('tipos de dados')
print(df_vendas.dtypes)

# se a coluna Data_Pedido não estiver no formato datetime, converte para datetime
# essa coluna pode ser usada para fazer análises de séries temporais, como vendas por mês, por trimestre, etc.
df_vendas['Data_Pedido'] = pd.to_datetime(df_vendas['Data_Pedido'])

# Engenharia de atributos - criação da coluna 'Faturamento' (preço x quantidade)
df_vendas['Faturamento'] = df_vendas['Preco_Unitario'] * df_vendas['Quantidade']
# um dos objetivos do projeto, era analisar a receita, quis categorias de produtos geram a maior parte da receita. E receita significa faturamento
# e nos dados originais não havia uma coluna de faturamento, então criamos essa coluna a partir do preço unitário e da quantidade vendida

# Engenharia de atributos 2
#Usando uma função lambda para criar uma coluna de status de entrega
df_vendas['Status_Entrega'] = df_vendas['Estado'].apply(lambda estado: 'Rápida' if estado in ['SP', 'RJ', 'MG'] else 'Normal')
# para cada item da coluna estado, se o estado for SP, RJ ou MG, a entrega é rápida, caso contrário, é normal.

# exibe informações gerais do dataframe após a engenharia de atributos
print('informações gerais após engenharia de atributos')
print(df_vendas.info()) 

# #Analise 1 - Top 10 produtos mais vendidos
# #agruda por nome do produto,soma a quantidade e ordena para encontrar os mais vendidos
# top_10_produtos = df_vendas.groupby('Nome_Produto')['Quantidade'].sum().sort_values(ascending=False).head(10) # imprime so os 10 primeiros produtos mais vendidos

# print('Top 10 produtos mais vendidos')
# print(top_10_produtos)

# #define um estilo para os gráficos
# sns.set(style="whitegrid")

# #cria a figura e os eixos
# plt.figure(figsize=(12,7))

# # cria o graficos de barras horizontais
# top_10_produtos.sort_values(ascending=True).plot(kind='barh', color='skyblue') #barh - barra horizontal

# # adiciona titulo e rótulos
# plt.title('Top 10 Produtos Mais Vendidos', fontsize=16)
# plt.xlabel('Quantidade Vendida', fontsize=12)
# plt.ylabel('Produto', fontsize=12)

# # exibe o gráfico
# plt.tight_layout()
# plt.show()


# #Analise 2 - Qual foi o faturamento mensal?
# #criar coluna mes para facilitar o agrupamento mensal
# df_vendas['Mes'] = df_vendas['Data_Pedido'].dt.to_period('M') #dt.to_period('M') converte a data para o período mensal

# #agruda por mês e soma o faturamento - soma o faturamento de cada mes
# faturamento_mensal = df_vendas.groupby('Mes')['Faturamento'].sum()

# #converte o índice para string para facilitar a plotagem
# faturamento_mensal.index = faturamento_mensal.index.strftime('%Y-%m') #converte o índice para string no formato ano-mês

# #formata para duas casas decimais - Deu erro
# print(faturamento_mensal.map('R$ {:,.2f}'.format))
# # esse map é da biblioteca pandas, não é o map do python 
# # a diferença é que o map do pandas aplica a função a cada elemento da série, enquanto o map do python aplica a função a cada elemento de um iterável

# #cria uma nova figura com tamanho 12 por 6 polegadas
# plt.figure(figsize=(12,6))

# #plota os dados de faturamento mensal em formato de linha
# faturamento_mensal.plot(kind='line', marker='o', linestyle='-', color='green')

# #defin e o título com fonte 16
# plt.title('Evolução do Faturamento Mensal', fontsize=16)

# #roluto x
# plt.xlabel('Mês', fontsize=12)

# #rótulo y
# plt.ylabel('Faturamento', fontsize=12)

# #rotaciona os rótulos do eixo x em 45 graus para melhor visualização
# plt.xticks(rotation=45)

# # adiciona uma grade com estilo tracejado e linhas finas
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# #ajusta automaticamente os elementos para evitar sobreposição
# plt.tight_layout()

# #exibe o gráfico
# plt.show()

# Análise 3 - total de vendas por cada estado
vendas_estado = df_vendas.groupby('Estado')['Faturamento'].sum().sort_values(ascending=False)

# formata para duas casas decimais

print('Faturamento por estado')
print(vendas_estado.map('R$ {:,.2f}'.format))

# https://seaborn.pydata.org/generated/seaborn.color_palette.html

#cria uma nova figura com tamanho de 12 por 7
plt.figure(figsize=(12,7))

#Plota os dados de faturamento por estado em formato de gráfico de barras
# usando a paleta de cores "rocket do Seaborn"
#husl - cores diferentes para cada barra
vendas_estado.plot(kind='bar', color=sns.color_palette("husl", 7)) 


#titulo
plt.title('Faturamento por Estado', fontsize=16)

plt.xlabel('Estado', fontsize=12)
plt.ylabel('Faturamento', fontsize=12)

plt.xticks(rotation=0) #rotaciona os rótulos do eixo x em 0 graus para melhor visualização
plt.tight_layout()

plt.show()

# Análise 4 - Faturamento por categoria