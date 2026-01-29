import pandas as pd 

# carregar dataset
df = pd.read_csv("vendas.csv")

# exibir primeiras linhas
print("Primeiras 5 linhas do dataset:")
print(df.head())

# verificar dados nulos
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# verificar dados duplicados
print("\nNumero de linhas duplicadas:", df.duplicated().sum())

# remover linhas duplicados
df.drop_duplicates(inplace=True)

# ajustar o tipo da coluna 'Data
df["Data"] = pd.to_datetime(df["Data"]).dt.date

# criar uma nova coluna 'Ano'
df["Ano"] = pd.to_datetime(df["Data"]).dt.year

# exibir o dataser após as transformações
print("\nDataset após limpeza e transformação:")
print(df.head())

# salvar dataset limpo e transformado
df.to_csv("vendas_limpo.csv", index=False)
print("\nDataset limpo e transformado salvo como 'vendas_limpo.csv'")
