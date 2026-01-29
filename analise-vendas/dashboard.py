import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from filtros import resetar_filtros, exibir_filtros
from pathlib import Path    

# Configurações da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Título do dashboard
st.title("Dashboard de Análise de Vendas")

# Carregar o dataset limpo
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "vendas_limpo.csv")

# Inicializar variáveis de sessão para manter os filtros
if "filtros_default" not in st.session_state:
    st.session_state.filtros_default = {
        "ano": df["Ano"].min(),
        "produtos": list(df["Produto"].unique()),
        "quantidade": (int(df["Quantidade"].min()), int(df["Quantidade"].max())),
    }

# Botão para resetar filtros
if st.sidebar.button("Resetar Fltros", use_container_width=True):
    resetar_filtros(df)

# Mostrar os filtros e capturar as seleções
produtos_selecionados, ano_selecionado, quantidade_range = (
    exibir_filtros(df)
)


# Aplicar todos os filtros
df_filtrado = df[
    (df["Produto"].isin(produtos_selecionados))
    & (df["Ano"] == ano_selecionado)
    & (df["Quantidade"] >= quantidade_range[0])
    & (df["Quantidade"] <= quantidade_range[1])
]

# Abas
aba1, aba2, aba3 = st.tabs(["Métricas", "Gráficos", "Tabela de dados"])


# Aba de metricas
with aba1:
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


# Aba de gráficos
with aba2:

    col1, col2 = st.columns(2)

    # Gráfico Barras
    with col1:
        st.write("### Vendas por Produto")
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        if not df_filtrado.empty:
            vendas_produto = df_filtrado.groupby("Produto")["Total"].sum().sort_values()
            sns.barplot(
                x=vendas_produto.values,
                y=vendas_produto.index,
                palette="Blues",
                ax=ax1,
            )
            plt.title("Vendas por Produto (Filtradas)")
            plt.xlabel("Total de Vendas (R$)")
            plt.tight_layout()
        exibir_grafico(fig1, "Vendas por Produto")

    with col2:
        st.write("### Vendas por Mês")
        fig2, ax2 = plt.subplots(figsize=(10, 8))

        if not df_filtrado.empty:
            df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"])

            df_filtrado["MesAnoFormatado"] = df_filtrado["Data"].dt.strftime("%b/%y")

            df_filtrado["Ordem"] = df_filtrado["Data"].dt.to_period("M")

            evolucao = (
                df_filtrado.groupby(["Ordem", "MesAnoFormatado"])["Total"]
                .sum()
                .reset_index()
                .sort_values("Ordem")
            )

            sns.lineplot(
                x="MesAnoFormatado",
                y="Total",
                data=evolucao,
                marker="o",
                ax=ax2,
                color="Blue"
            )

            ax2.set_title("Evolução de Vendas por Mês")
            ax2.set_xlabel("Mês")
            ax2.set_ylabel("Total de Vendas (R$)")
            plt.xticks(rotation=45)
            plt.tight_layout()

        exibir_grafico(fig2, "Evolução por Mês")

        
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    # Gráfico de Pizza
    with col3:
        st.write("### Proporção de Vendas por Categoria")
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        if not df_filtrado.empty:
            proporcao = df_filtrado.groupby("Produto")["Total"].sum()
            ax3.pie(
                proporcao,
                labels=proporcao.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=sns.color_palette(palette="Blues")
            )
            ax3.axis("equal")
            plt.title("Proporção de Vendas por Produto")
            plt.tight_layout()
        exibir_grafico(fig3, "Gráfico de Pizza")

    # Histograma
    with col4:
        st.write("### Distribuicão de Dados por Quantidade")

        fig4, ax4 = plt.subplots(figsize=(10, 8))
        if not df_filtrado.empty:
            sns.histplot(
                df_filtrado["Quantidade"], bins=20, kde=True, ax=ax4, color="blue"
            )
            plt.xlabel("Quantidade")
            plt.ylabel("Frequência")
            plt.title("Distribuicão de Quantidade")
            plt.tight_layout()
        exibir_grafico(fig4, "Histograma")

# Aba de tabela
with aba3:
    st.subheader("Dados Filtrados")

    if df_filtrado.empty:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
    else:
        df_filtrado["Data"] = df_filtrado["Data"].dt.strftime("%Y-%m-%d")
        df_filtrado_final = df_filtrado.drop(
            columns=["Ordem"], errors="ignore"
        )
        st.write(df_filtrado_final.assign(Ano=df_filtrado_final["Ano"].map(str)))
        st.download_button(
            label="Baixar dados filtrados",
            data=df_filtrado_final.to_csv(index=False).encode("utf-8"),
            file_name="vendas_filtradas.csv",
            mime="text/csv",
        )
