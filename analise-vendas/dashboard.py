import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# configurações da pagina
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# titulo do dashboard
st.title("Dashboard de Análise de Vendas")

# carregar o dataset limpo
df = pd.read_csv("vendas_limpo.csv")

# exibir o dataset
st.subheader("Dados de Vendas")
st.write(df)

# Filtros interativos
st.sidebar.header("Filtros")

# Filtro de produtos (permite seleção múltipla)
produtos = df["Produto"].unique()
produtos_selecionados = st.sidebar.multiselect(
    "Selecione um ou mais Produtos", produtos, default=produtos
)

# Filtro de mês
meses = df["Mês"].unique()
mes_selecionado = st.sidebar.selectbox("Selecione um Mês", meses)

# Converter a coluna 'Data' para o tipo datetime
df["Data"] = pd.to_datetime(df["Data"])

# Filtro de data
st.sidebar.subheader("Filtro de Datas")
data_inicio = st.sidebar.date_input("Data Inicial", df["Data"].min())
data_fim = st.sidebar.date_input("Data Final", df["Data"].max())

# Filtrar os dados
df_filtrado = df[
    (df["Produto"].isin(produtos_selecionados))  # Filtro de produtos
    & (df["Mês"] == mes_selecionado)  # Filtro de mês
    & (df["Data"] >= pd.to_datetime(data_inicio))  # Filtro de data inicial
    & (df["Data"] <= pd.to_datetime(data_fim))  # Filtro de data final
]

# Exibir os dados filtrados
st.subheader(
    f"Dados Filtrados no Mês {mes_selecionado} para {', '.join(produtos_selecionados)}  "
)
st.write(df_filtrado)

# cartoes com metricas relevantes
st.write("### Métricas Principais")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if not df_filtrado.empty:
        total_vendas = df_filtrado["Total"].sum()
        st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")
    else:
        st.metric("Total de Vendas", "R$ 0.00")

with col2:
    if not df_filtrado.empty:
        media_vendas = df_filtrado["Total"].mean()
        st.metric("Média de Vendas por Dia", f"R$ {media_vendas:,.2f}")
    else:
        st.metric("Média de Vendas por Dia", "R$ 0.00")

with col3:
    if not df_filtrado.empty:
        quantidade_vendas = df_filtrado["Quantidade"].sum()
        st.metric("Quantidade Total Vendida", f"{quantidade_vendas:,.2f} unidades")
    else:
        st.metric("Quantidade Total Vendida", "0.00 unidades")

with col4:
    if not df_filtrado.empty:
        produto_mais_vendido = df_filtrado["Produto"].value_counts().idxmax()
        st.metric("Produto Mais Vendido", produto_mais_vendido)
    else:
        st.metric("Produto Mais Vendido", "Nenhum")

# grafico de funil: Vendas por produto
st.write("### Vendas por Produto")
if not df_filtrado.empty:
    vendas_por_produto = df_filtrado.groupby("Produto")["Total"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=vendas_por_produto.values, y =vendas_por_produto.index, palette="viridis", ax=ax)
    plt.title("Vendas por Produto")
    plt.xlabel("Total de Vendas (R$)")
    plt.ylabel("Produto")
    st.pyplot(fig)
else:
    st.write("Nenhum dado disponível para exibir o gráfico de vendas por produto.")

# grafico de linhas: Vendas ao longo do tempo
st.write("### Vendas ao longo do Tempo")
if not df_filtrado.empty:
    vendas_por_data = df_filtrado.groupby('Data')['Total'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=vendas_por_data.index, y=vendas_por_data.values, marker="o" ,ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("Nenhum dado disponível para exibir o gráfico de vendas ao longo do tempo.")
