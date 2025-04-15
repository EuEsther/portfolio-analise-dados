import streamlit as st


def resetar_filtro_produto(df, filtros_default):
    produtos_validos = df["Produto"].unique().tolist()
    produtos_filtrados = [
        p for p in filtros_default["produtos"] if p in produtos_validos
    ]
    st.session_state["filtro_produto"] = produtos_filtrados


def resetar_filtro_ano(df, filtros_default):
    anos_validos = df["Ano"].unique().tolist()
    ano_default = filtros_default["ano"]
    st.session_state["filtro_ano"] = (
        ano_default if ano_default in anos_validos else anos_validos[0]
    )


def resetar_filtro_mes(df, filtros_default):
    meses_validos = df["Mês"].unique().tolist()
    mes_default = filtros_default["mes"]
    st.session_state["filtro_mes"] = (
        mes_default if mes_default in meses_validos else meses_validos[0]
    )


def resetar_filtro_quantidade(df, filtros_default):
    qtd_min, qtd_max = int(df["Quantidade"].min()), int(df["Quantidade"].max())
    q1, q2 = filtros_default["quantidade"]
    if qtd_min <= q1 <= qtd_max and qtd_min <= q2 <= qtd_max:
        st.session_state["filtro_quantidade"] = (q1, q2)
    else:
        st.session_state["filtro_quantidade"] = (qtd_min, qtd_max)


def resetar_filtros(df):
    filtros_default = st.session_state.filtros_default
    resetar_filtro_produto(df, filtros_default)
    resetar_filtro_ano(df, filtros_default)
    resetar_filtro_mes(df, filtros_default)
    resetar_filtro_quantidade(df, filtros_default)


def exibir_filtros(df):
    st.sidebar.header("Filtros")

    produtos = st.sidebar.multiselect(
        "Selecione os Produtos",
        df["Produto"].unique(),
        default=st.session_state.filtros_default["produtos"],
        key="filtro_produto",
    )

    ano = st.sidebar.selectbox(
        "Selecione o Ano", sorted(df["Ano"].unique()), key="filtro_ano"
    )

    mes = st.sidebar.selectbox(
        "Selecione o Mês", sorted(df["Mês"].unique()), key="filtro_mes"
    )

    quantidade = st.sidebar.slider(
        "Intervalo de Quantidade",
        int(df["Quantidade"].min()),
        int(df["Quantidade"].max()),
        st.session_state.filtros_default["quantidade"],
        key="filtro_quantidade",
    )
    

    return produtos, ano, mes, quantidade
