# Assessment – IMDb Top 250 (Python para Dados)

```md
Projeto desenvolvido como parte da disciplina "Python para Dados", com o objetivo de:
• Fazer web scraping da página IMDb Top 250
• Modelar classes em Python (TV, Movie, Series)
• Persistir os dados em um banco SQLite usando SQLAlchemy
• Ler e analisar os dados com Pandas
• Exportar resultados em formato CSV e JSON
• Organizar o código em módulos e em um repositório GitHub
```

---

## Estrutura do projeto

```text
assessment-imdb/
│
├─ src/
│ ├─ __init__.py
│ ├─ scraping.py
│ ├─ models.py
│ ├─ database.py
│ ├─ analysis.py
│ └─ main.py
│
├─ data/
│ ├─ imdb.db
│ ├─ movies.csv
│ ├─ series.csv
│ ├─ movies.json
│ └─ series.json
│
├─ config.json
├─ requirements.txt
├─ .gitignore
└─ README.md
```
Obs.: Na primeira execução, a pasta data/ pode estar vazia. Todos esses arquivos são gerados automaticamente pelo script principal.

---

## Dependências necessárias

```md
• **beautifulsoup4** – parsing HTML
• **pandas** – análise e manipulação de dados
• **SQLAlchemy** – ORM para persistência no SQLite
```
Todas estão listadas no arquivo requirements.txt.

---

## Instalação das dependências

No terminal, dentro da pasta raiz do projeto (assessment-imdb):

`pip install -r requirements.txt`

---

## Configuração

O arquivo config.json controla a URL do scraping e a quantidade de filmes coletados. Exemplo:
```json
{
"imdb_url": "https://www.imdb.com/pt/chart/top/?ref_=chttp_nv_menu",
"n_filmes": 250
}
```

---

## Como executar o projeto

Na pasta raiz do projeto execute:

`python -m src.main`

O script executa automaticamente todas as etapas:
1. Leitura do config.json
2. Scraping do IMDb Top 250
3. Criação dos objetos Movie e Series
4. Persistência dos dados no banco data/imdb.db
5. Leitura com Pandas
6. Exportação para CSV e JSON em data/
7. Classificação textual das notas
8. Resumo de filmes por categoria e ano

Todas as saídas são exibidas no terminal durante a execução.

---

## Descrição dos módulos
```md
**scraping.py** → coleta dados do IMDb
**models.py** → define classes TV, Movie, Series e cria catálogo
**database.py** → cria engine, tabelas e salva dados com SQLAlchemy
**analysis.py** → leitura com Pandas, exportação e resumo
**main.py** → orquestra todo o fluxo do projeto
```

---

## Agradecimento

Obrigado por avaliar este trabalho!
