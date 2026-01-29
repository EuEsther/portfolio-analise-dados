# Análise de Vendas

Este projeto tem como objetivo analisar dados de vendas de uma empresa de varejo, utilizando técnicas de análise de dados e visualização. O projeto inclui a geração de um dataset sintético, limpeza e transformação dos dados, análise exploratória e a criação de um dashboard interativo.

## ⚙️ Funcionalidades

- **Geração de Dados Sintéticos**: Cria um dataset fictício de vendas.
- **Limpeza e Transformação**: Remove dados duplicados, ajusta formatos e cria novas colunas.
- **Análise Exploratória**: Calcula métricas básicas e gera visualizações.
- **Dashboard Interativo**: Permite filtrar dados e visualizar gráficos em tempo real.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Pandas**: Manipulação e análise de dados.
- **Faker**: Geração de dados sintéticos.
- **Matplotlib/Seaborn**: Visualização de dados estáticos.
- **Plotly**: Visualização de dados interativos.
- **Streamlit**: Criação do dashboard interativo.

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/EuEsther/portfolio-analise-dados.git
   cd portfolio-analise-dados/analise-vendas

   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate    # Windows

   ```

3. Instale as dependências:

   ```bash
   pip install -r ../requirements.txt

   ```

4. Execute o script de geração de dados:

   ```bash
   python gerar_dados.py

   ```

5. Execute o script de limpeza e transformação:

   ```bash
   python limpeza_transformacao.py

   ```

6. Execute o dashboard interativo:
   ```bash
   streamlit run dashboard.py
   ```
