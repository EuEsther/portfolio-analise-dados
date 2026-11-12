# Análise de Retenção e Comportamento de Usuários de uma Plataforma de Streaming

## Sobre o projeto

Este projeto constrói uma base de dados fictícia para uma plataforma de streaming e desenvolve análises exploratórias sobre o perfil e o comportamento de seus clientes. O objetivo é demonstrar um fluxo de trabalho de análise de dados, da criação do banco e preparação dos dados à consulta SQL, organização dos resultados e interpretação de negócio.

Os principais objetivos são:

- Analisar o perfil dos clientes e a distribuição por plano.
- Avaliar o consumo de conteúdos e os gêneros com mais minutos assistidos.
- Observar o tempo de visualização registrado.
- Identificar clientes ativos sem visualizações recentes.
- Gerar hipóteses e recomendações que possam apoiar decisões de negócio.

> **Nota sobre os dados:** todos os registros são fictícios. A base contém 50 clientes e 50 eventos de visualização, com um evento por cliente. Os eventos vão de janeiro de 2022 a novembro de 2025. Os resultados servem para demonstrar as consultas e não representam usuários reais nem permitem conclusões sobre o mercado.

## Tecnologias e ferramentas

| Tecnologia ou ferramenta | Uso no projeto |
| --- | --- |
| Python | Scripts de criação e carga do banco, além do ambiente das análises. |
| `sqlite3` | Biblioteca padrão do Python usada pelos scripts para acessar o SQLite. |
| SQLite | Armazenamento local dos dados em `streaming.db`. |
| SQL | Consultas, filtros, junções, agrupamentos e agregações. |
| SQLAlchemy | Conexão do notebook com o banco SQLite. |
| Pandas | Organização dos resultados em DataFrames. |
| Jupyter Notebook | Desenvolvimento e documentação das análises. |
| VS Code | Edição do projeto e execução do notebook. |
| Codex | Ferramenta de inteligência artificial utilizada no desenvolvimento integral do projeto. |

## Estrutura do projeto

```text
.
├── README.md
├── analise_streaming.ipynb
└── database/
    ├── create_database.py
    ├── populate_database.py
    └── streaming.db
```

- `database/streaming.db`: banco SQLite com as tabelas e os dados fictícios.
- `database/create_database.py`: cria as tabelas e índices se ainda não existirem.
- `database/populate_database.py`: carrega e valida o lote de dados fictícios; evita duplicar um lote completo.
- `analise_streaming.ipynb`: conexão SQLAlchemy, consultas, DataFrames e interpretações de negócio.
- `README.md`: documentação e instruções de execução.

O projeto não possui um arquivo `requirements.txt`; as dependências podem ser instaladas com o comando indicado abaixo.

## Banco de dados

O banco contém as tabelas `clientes` e `historico_visualizacao`.

### `clientes`

| Campo | Descrição e restrições |
| --- | --- |
| `id` | Identificador inteiro, chave primária com incremento automático. |
| `nome` | Nome do cliente; obrigatório. |
| `data_adesao` | Data de adesão, armazenada como texto no padrão ISO 8601. |
| `tipo_plano` | Plano contratado, como Básico, Padrão ou Premium. |
| `status_assinatura` | Status obrigatório, limitado a `Ativo` ou `Cancelado`. |

### `historico_visualizacao`

| Campo | Descrição e restrições |
| --- | --- |
| `id_evento` | Identificador inteiro, chave primária com incremento automático. |
| `id_cliente` | Cliente responsável pelo evento; chave estrangeira para `clientes.id`, obrigatório. |
| `data` | Data e horário da visualização em formato ISO 8601. |
| `titulo_conteudo` | Nome do filme, série ou outro conteúdo. |
| `genero` | Gênero do conteúdo. |
| `minutos_assistidos` | Minutos assistidos; quando preenchido, deve ser numérico e não negativo. |
| `dispositivo_utilizado` | Dispositivo usado para assistir. |

O relacionamento é de um para muitos: um cliente pode ter vários eventos, e cada evento pertence a um cliente existente. A chave estrangeira define `ON DELETE CASCADE`, removendo os eventos do cliente quando ele é excluído. No SQLite, a aplicação precisa habilitar `PRAGMA foreign_keys = ON` em cada conexão para que a integridade referencial seja aplicada; os scripts de banco fazem essa configuração.

## Análises desenvolvidas

O notebook contém as seguintes análises:

1. **Clientes Premium:** lista os 16 clientes com plano Premium. Eles representam 32% dos 50 registros; 11 estão ativos e 5 cancelados. Os planos estão distribuídos de forma próxima: Básico 17, Padrão 17 e Premium 16.
2. **Consumo por gênero:** soma os minutos assistidos por categoria e ordena do maior para o menor. Suspense lidera com 466 minutos, seguido de Ação com 442 e Animação com 415. Os oito gêneros totalizam 3.165 minutos.
3. **Clientes ativos sem visualizações recentes:** identifica clientes sem eventos nos 30 dias anteriores à execução. No conjunto atual, os 37 clientes ativos atendem ao filtro, pois os eventos mais recentes são de novembro de 2025.
4. **Média histórica de minutos por cliente:** a consulta de clientes sem atividade recente calcula `AVG()` individualmente usando os registros anteriores à janela recente. Como a base tem somente um evento por cliente, os valores atuais correspondem a esse único evento, e não a uma média comportamental robusta.

As contagens e interpretações refletem o banco incluído neste projeto. Por ser uma amostra fictícia, pequena e desatualizada para uma janela de atividade em tempo real, os resultados demonstram métodos analíticos, não padrões reais de retenção ou preferência.

## Como executar no Windows e no VS Code

1. Clone o repositório usando o endereço fornecido pelo responsável pelo projeto, ou baixe e extraia seus arquivos.
2. Abra a pasta raiz do projeto no VS Code. Se o comando `code` estiver disponível, também é possível abri-la pelo terminal:

   ```powershell
   code .
   ```

3. Crie e ative um ambiente virtual PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Instale as bibliotecas usadas pelo notebook e o suporte ao kernel Jupyter:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install pandas sqlalchemy jupyter ipykernel
   ```

5. Confirme que o banco incluído está presente:

   ```powershell
   Test-Path .\database\streaming.db
   ```

   O resultado esperado é `True`. Se estiver iniciando uma base vazia, crie o esquema e carregue a amostra, nesta ordem:

   ```powershell
   python .\database\create_database.py
   python .\database\populate_database.py
   ```

   O projeto já inclui o banco populado; esses comandos não são necessários para a execução normal. O script de carga evita duplicar o lote completo e interrompe a execução se encontrar dados parciais ou diferentes.

6. Abra `analise_streaming.ipynb` no VS Code. Instale as extensões Python e Jupyter, se solicitado.
7. Selecione o interpretador `.venv` e o kernel correspondente no notebook.
8. Execute as células na ordem, mantendo como diretório de trabalho a raiz do projeto. O notebook procura o banco em `database/streaming.db` por caminho relativo.

## Resultados e finalidade
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Análise de Retenção e Comportamento de Usuários de uma Plataforma de Streaming](#análise-de-retenção-e-comportamento-de-usuários-de-uma-plataforma-de-streaming)
  - [Sobre o projeto](#sobre-o-projeto)
  - [Tecnologias e ferramentas](#tecnologias-e-ferramentas)
  - [Estrutura do projeto](#estrutura-do-projeto)
  - [Banco de dados](#banco-de-dados)
    - [`clientes`](#clientes)
    - [`historico_visualizacao`](#historico_visualizacao)
  - [Análises desenvolvidas](#análises-desenvolvidas)
  - [Como executar no Windows e no VS Code](#como-executar-no-windows-e-no-vs-code)
  - [Resultados e finalidade](#resultados-e-finalidade)
  - [Desenvolvimento com inteligência artificial](#desenvolvimento-com-inteligência-artificial)

<!-- /code_chunk_output -->



As consultas mostram como relacionar cadastro e comportamento, comparar o consumo entre gêneros, observar a composição por plano e localizar assinantes ativos sem eventos recentes. Em um contexto real, informações desse tipo poderiam orientar investigações sobre engajamento, catálogo e ações de retenção.

Essas recomendações são hipóteses de uso, não efeitos comprovados pelos dados simulados. Para decisões reais, seria necessário trabalhar com uma base maior, atualizada e representativa, além de medir resultados de eventuais ações.

## Desenvolvimento com inteligência artificial

Este projeto foi desenvolvido integralmente com auxílio de inteligência artificial, utilizando o Codex. A criação da estrutura do banco, a geração dos dados fictícios, o desenvolvimento das consultas SQL, a implementação das análises em Python e a elaboração desta documentação foram realizados com suporte da ferramenta.
