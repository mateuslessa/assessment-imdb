import os
import json

# Scraping (src/scraping.py)
from src.scraping import obter_filmes_top

# Classes/objetos (src/models.py)
from src.models import criar_catalogo

# Manipulação do banco (src/database)
from src.database import criar_engine, criar_tabelas, salvar_catalogo_no_banco

# Funções de análise e exportação (src/analysis.py)
from src.analysis import (
    carregar_dataframe_movies,
    carregar_dataframe_series,
    exportar_csv_json,
    adicionar_categoria,
    resumo_categoria_ano,
)


def carregar_config(caminho_config = "config.json"):
    """
    Lê o arquivo de configuração JSON e devolve um dicionário
    com os parâmetros do projeto.

    Parâmetros:
        caminho_config (str, opcional): Caminho até o arquivo config.json.
            Padrão: "config.json".

    Retorno:
        dict: Dicionário contendo pelo menos:
            - "imdb_url": URL da página do IMDb Top 250.
            - "n_filmes": quantidade de filmes a coletar (opcional).
    """
    with open(caminho_config, mode='r', encoding='utf-8') as arquivo:
        config = json.load(arquivo)
    return config


def main():
    """
    Executa o fluxo completo do trabalho:

        1. Lê o arquivo de configuração (config.json).
        2. Faz o scraping da página do IMDb (Exercícios 1 e 2).
        3. Cria os objetos Movie e Series e monta a lista catalog (Ex. 3, 4 e 5).
        4. Cria o banco de dados e grava os dados (Ex. 6).
        5. Lê os dados do banco com Pandas (Ex. 7).
        6. Filtra, ordena e exporta filmes/séries (Ex. 8).
        7. Cria a coluna de categoria textual das notas (Ex. 9).
        8. Gera o resumo de filmes por categoria e ano (Ex. 10).

    Ao longo da execução, imprime no terminal saídas que respondem
    diretamente ao enunciado de cada exercício.
    """
    # 1. Lê o arquivo de configuração (config.json)
    config = carregar_config()
    url = config.get("imdb_url")
    n_filmes = config.get("n_filmes", 250)  # default 250

    # 2. Faz o scraping da página do IMDb (Exercícios 1 e 2)
    lista_filmes = obter_filmes_top(url, n_filmes=n_filmes)
    


    # EXERCÍCIO 1 - Scraping básico do IMDb Top 250
    print('EXERCÍCIO 1 - Scraping básico do IMDb Top 250\n')

    # Extraindo apenas os títulos para exibir os 10 primeiros
    titulos_filmes = [filme['titulo'] for filme in lista_filmes]

    print('10 primeiros títulos:')
    for i, titulo in enumerate(titulos_filmes[:10]):
        print(f'{i+1}) "{titulo}"')
    


    # EXERCÍCIO 2 - Título, ano e nota dos filmes
    print('\n\nEXERCÍCIO 2 - Título, ano e nota dos filmes\n')

    print('5 primeiros filmes:')
    for i, filme in enumerate(lista_filmes[:5]):
        titulo = filme['titulo']
        ano = filme['ano_lancamento']
        nota = filme['nota']
        print(f'{i+1}) "{titulo}" ({ano}) - Nota: {nota}')
    


    # EXERCÍCIO 3 - Classe base TV
    print('\n\nEXERCÍCIO 3 - Classe base TV')
    # (Classes estão definidas em src/models.py)
    print('\nClasse TV criada com sucesso!')



    # EXERCÍCIO 4 - Classes Movie e Series
    print('\n\nEXERCÍCIO 4 - Classes Movie e Series')
    # (Classes Movie e Series também estão em src/models.py)
    print('\nClasses Movie e Series criadas com sucesso!')


    # EXERCÍCIO 5 - Lista de objetos a partir do scraping
    print('\n\nEXERCÍCIO 5 - Lista de objetos a partir do scraping\n')

    # 3. Cria os objetos Movie e Series e monta a lista catalog (Ex. 3, 4 e 5)
    catalog = criar_catalogo(lista_filmes)

    print('Todos os itens na lista catalog:')
    for item in catalog:
        print(item)



    # EXERCÍCIO 6 - Banco de dados imdb.db com SQLAlchemy
    print('\n\nEXERCÍCIO 6 - Banco de dados imdb.db com SQLAlchemy')

    # 4. Cria o banco de dados e grava os dados (Ex. 6)
    # Garante que a pasta 'data' exista antes de criar o banco
    os.makedirs("data", exist_ok=True)

    # Usa o caminho padrão configurado em criar_engine: sqlite:///data/imdb.db
    engine = criar_engine()
    criar_tabelas(engine)
    salvar_catalogo_no_banco(catalog, engine)

    print('\nBanco data/imdb.db criado com sucesso!')
    print('Registros inseridos nas tabelas com sucesso!')



    # EXERCÍCIO 7 - Lendo os dados do banco com Pandas
    print('\n\nEXERCÍCIO 7 - Lendo os dados do banco com Pandas\n')

    # 5. Lê os dados do banco com Pandas (Ex. 7)
    df_movies = carregar_dataframe_movies() # Usa o caminho default para o banco
    df_series = carregar_dataframe_series() # Usa o caminho default para o banco

    # Exibindo as 5 primeiras linhas do DataFrame com filmes
    print('\n5 primeiras linhas do DataFrame com filmes:')
    print(df_movies.head(5))

    # Exibindo as 5 primeiras linhas do DataFrame com séries
    print('\n5 primeiras linhas do DataFrame com séries:')
    print(df_series.head(5))



    # EXERCÍCIO 8 - Análise e exportação de filmes e séries
    print('\n\nEXERCÍCIO 8 - Análise e exportação de filmes e séries\n')

    # 6. Filtra, ordena e exporta filmes/séries (Ex. 8)

    # Filtrando filmes com nota maior que 9.0
    df_melhores_filmes = df_movies[df_movies['rating'] > 9.0]

    # Ordenando filmes filtrados pela nota (do maior para o menor)
    df_melhores_filmes_sorted = df_melhores_filmes.sort_values(
        by=['rating'], ascending=False
    )

    # Exibindo os 5 filmes com melhor avaliação após o filtro
    print('5 filmes com melhor avaliação:')
    print(df_melhores_filmes_sorted.head(5))

    # Exportando CSV e JSON (com mensagens e tratamento de erro) para a pasta data/
    exportar_csv_json(df_movies, df_series, pasta_saida="data")



    # EXERCÍCIO 9 - Classificação textual das notas (no DataFrame)
    print('\n\nEXERCÍCIO 9 - Classificação textual das notas (no DataFrame)\n')

    # 7. Cria a coluna de categoria textual das notas (Ex. 9).

    # Criando a coluna 'categoria' que recebe a categoria textual correspondente ao 'rating'
    df_movies = adicionar_categoria(df_movies)

    # Exibindo os 10 primeiros filmes com title, rating e categoria
    print('10 primeiros filmes:')
    print(df_movies[['title', 'rating', 'categoria']].head(10))



    # EXERCÍCIO 10 - Resumo de filmes por categoria
    print('\n\nEXERCÍCIO 10 - Resumo de filmes por categoria\n')

    #  8. Gera o resumo de filmes por categoria e ano (Ex. 10).
    resumo = resumo_categoria_ano(df_movies)
    
    print('Resumo de quantidade de filmes por categoria e ano de lançamento:')
    print(resumo)


if __name__ == "__main__":
    main()

