import pandas as pd
from faker import Faker
from datetime import datetime
import random

# configurações
NUM_REGISTROS = 3000 #numero do registro (vendas) a serem gerados
PRODUTOS = ["Camiseta", "Calça", "Tênis", "Boné", "Mochila", "Sapato"]
DATA_INICIO = datetime.strptime("2023-01-01", "%Y-%m-%d").date()
DATA_FIM = datetime.strptime("2025-12-31", "%Y-%m-%d").date()

# inicializador Faker
fake = Faker('pt-BR') # configurar para dados em Portugues

# funcao para gerar dados sinteticos
def gerar_dados(num_registros):
    dados = []
    for _ in range(num_registros):
        data = fake.date_between(start_date=DATA_INICIO, end_date=DATA_FIM)
        produto = random.choice(PRODUTOS)
        quantidade = random.randint(1, 10)
        preco_unitario = round(random.uniform(50, 500), 2)
        total = quantidade * preco_unitario

        dados.append([data, produto, quantidade, preco_unitario, total])
    return dados

# criar DataFrame
colunas = ["Data", "Produto", "Quantidade", "Preço Unitário", "Total"]
dados = gerar_dados(NUM_REGISTROS)
df = pd.DataFrame(dados, columns=colunas)

# salvar em CSV
df.to_csv("vendas.csv", index=False)
print("Dataset gerado e salvo como 'vendas.csv'")
