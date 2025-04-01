import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Título do dashboard
st.title("Dashboard de Análise de Vendas")

# Carregar o dataset limpo
df = pd.read_csv("vendas_limpo.csv")

# Converter colunas para os tipos corretos
df["Data"] = pd.to_datetime(df["Data"])
df["Ano"] = df["Data"].dt.year

# Filtros interativos na sidebar
st.sidebar.header("Filtros")

# Filtro de Produtos
produtos = df["Produto"].unique()
produtos_selecionados = st.sidebar.multiselect(
    "Selecione os Produtos", produtos, default=produtos
)
# Filtro de Ano
anos = df["Ano"].unique()
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos)

# Filtro de Mês
meses = df["Mês"].unique()
mes_selecionado = st.sidebar.selectbox("Selecione o Mês", meses)

# Filtro de Intervalo de Quantidade
min_quantidade = int(df["Quantidade"].min())
max_quantidade = int(df["Quantidade"].max())
quantidade_range = st.sidebar.slider(
    "Selecione o intervalo de quantidade",
    min_quantidade,
    max_quantidade,
    (min_quantidade, max_quantidade),
)


# Aplicar todos os filtros
df_filtrado = df[
    (df["Produto"].isin(produtos_selecionados))
    & (df["Ano"] == ano_selecionado)
    & (df["Mês"] == mes_selecionado)
    & (df["Quantidade"] >= quantidade_range[0])
    & (df["Quantidade"] <= quantidade_range[1])
]

# Métricas
st.write("### Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

metricas = {
    "Total de Vendas": "R$ 0.00",
    "Média de Vendas/dia": "R$ 0.00",
    "Quantidade Vendida": "0 unidades",
    "Produto Mais Vendido": "Nenhum",
}

if not df_filtrado.empty:
    metricas = {
        "Total de Vendas": f"R$ {df_filtrado['Total'].sum():,.2f}",
        "Média de Vendas/dia": f"R$ {df_filtrado['Total'].mean():,.2f}",
        "Quantidade Vendida": f"{df_filtrado['Quantidade'].sum():,} unidades",
        "Produto Mais Vendido": df_filtrado["Produto"].value_counts().idxmax(),
    }

for i, (k, v) in enumerate(metricas.items()):
    with eval(f"col{i+1}"):
        st.metric(k, v)


# Visualizações com verificações
def exibir_grafico(fig, titulo):
    if df_filtrado.empty:
        st.warning(f"Não há dados para exibir no gráfico: {titulo}")
        plt.close(fig)
    else:
        st.pyplot(fig)


# Gráfico Barras
st.write("### Vendas por Produto")
fig1, ax1 = plt.subplots(figsize=(20, 8))
if not df_filtrado.empty:
    vendas_produto = df_filtrado.groupby('Produto')['Total'].sum().sort_values()
    sns.barplot(x=vendas_produto.values, y=vendas_produto.index, palette="viridis", ax=ax1)
    plt.title("Vendas por Produto (Filtradas)")
    plt.xlabel("Total de Vendas (R$)")
exibir_grafico(fig1, "Vendas por Produto")

# Gráfico Evolução temporal
st.write("### Vendas ao Longo do Tempo")
fig2, ax2 = plt.subplots(figsize=(20, 6))
if not df_filtrado.empty:
    evolucao = df_filtrado.groupby("Data")["Total"].sum()
    sns.lineplot(x=evolucao.index, y=evolucao.values, marker="o", ax=ax2)
    plt.xticks(rotation=45)
    plt.title("Evolução das Vendas")
exibir_grafico(fig2, "Evolução Temporal")

# Mostrar dados filtrados
st.write("### Tabela de Dados Filtrados")
if df_filtrado.empty:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
else:
    st.write(df_filtrado)