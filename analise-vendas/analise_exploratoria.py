import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# carregar dataset limpo
df = pd.read_csv("vendas_limpo.csv")

# exibir informacoes basicas do dataset
print("Informações do dataset")
print(df.info())
print("\nEstatísticas descritivas")
print(df.describe())

# total de vendas
total_vendas = df['Total'].sum()
print(f"\nTotal de vendas: R$ {total_vendas:.2f}")

# medias de precos unitarios
media_preco_unitario = df['Preço Unitário'].mean()
print(f"\nPreço unitário médio: R$ {media_preco_unitario:.2f}")

# produtos mais vendidos
produtos_mais_vendidos = df['Produto'].value_counts()
print("\nProdutos mais vendidos")
print(produtos_mais_vendidos)

# vendas por mes
vendas_por_mes = df.groupby('Mês')['Total'].sum()
print("\nVendas por mês")
print(vendas_por_mes)

# visualizacoes
sns.set_style("whitegrid")

# grafico de barras: Produtos mais vendidos
plt.figure(figsize=(12,6))
sns.barplot(x=produtos_mais_vendidos.index, y=produtos_mais_vendidos.values, palette="viridis")
plt.title("Produtos mais vendidos")
plt.xlabel("Produto")
plt.ylabel("Quantidade vendida")
plt.xticks(rotation=45)
plt.show()

# grafico de linha: Vendas por mes
plt.figure(figsize=(12,6))
sns.lineplot(x=vendas_por_mes.index, y=vendas_por_mes.values, marker="o")
plt.title("Vendas por mês")
plt.xlabel("Mês")
plt.ylabel("Total de vendas (R$)")
plt.xticks(range(1,13))
plt.show()



