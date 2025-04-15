import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from filtros import resetar_filtros, exibir_filtros

# Configurações da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Título do dashboard
st.title("Dashboard de Análise de Vendas")

# Carregar o dataset limpo
df = pd.read_csv("vendas_limpo.csv")

# Inicializar variáveis de sessão para manter os filtros
if "filtros_default" not in st.session_state:
    st.session_state.filtros_default = {
        "ano": df["Ano"].min(),
        "produtos": list(df["Produto"].unique()),
        "mes": df["Mês"].min(),
        "quantidade": (int(df["Quantidade"].min()), int(df["Quantidade"].max())),
    }

# Filtros interativos na sidebar
st.sidebar.header("Filtros")

# Botão para resetar filtros
if st.sidebar.button("Resetar Fltros", use_container_width=True):
    resetar_filtros(df)

# Mostrar os filtros e capturar as seleções
produtos_selecionados, ano_selecionado, mes_selecionado, quantidade_range = (
    exibir_filtros(df)
)


# Aplicar todos os filtros
df_filtrado = df[
    (df["Produto"].isin(produtos_selecionados))
    & (df["Ano"] == ano_selecionado)
    & (df["Mês"] == mes_selecionado)
    & (df["Quantidade"] >= quantidade_range[0])
    & (df["Quantidade"] <= quantidade_range[1])
]

# Exibir dados filtrados
st.subheader("Dados Filtrados")

if df_filtrado.empty:
    st.info("Nenhum dado encontrado para os filtros selecionados.")
else:
    st.write(df_filtrado.assign(Ano=df_filtrado["Ano"].map(str)))

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
    vendas_produto = df_filtrado.groupby("Produto")["Total"].sum().sort_values()
    sns.barplot(
        x=vendas_produto.values, y=vendas_produto.index, palette="viridis", ax=ax1
    )
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
