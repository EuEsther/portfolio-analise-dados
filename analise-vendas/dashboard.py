import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# configurações da pagina
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# titulo do dashboard
st.title("Análise de Vendas")

# carregar o dataset limpo
df = pd.read_csv("vendas_limpo.csv")

# exibir o dataset
st.subheader("Dados de Vendas")
st.write(df)

# filtros interativos
st.sidebar.header("Filtros")
produtos = df['Produto'].unique()
produto_selecionado = st.sidebar.selectbox("Selecione um Produto", produtos)

meses = df['Mês'].unique()
mes_selecionado = st.sidebar.selectbox("Selecione um Mês", meses)

# filtrar os dados
df_filtrado = df[(df['Produto'] == produto_selecionado) & (df['Mês'] == mes_selecionado)]

# exibir os dados filtrados
st.subheader(f"Dados Filtrados para {produto_selecionado} no Mês {mes_selecionado}")
st.write(df_filtrado)

# graficos
st.subheader("Visualizações")

# grafico de barras: Vendas por Produto
st.write("### Vendas por Produto")
vendas_por_produto = df_filtrado.groupby('Produto')['Total'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=vendas_por_produto.index, y=vendas_por_produto.values,palette="viridis" , ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# grafico de linhas: Vendas ao longo do tempo
st.write("### Vendas ao longo do Tempo")
vendas_por_data = df_filtrado.groupby('Data')['Total'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=vendas_por_data.index, y=vendas_por_data.values, marker="o" ,ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)