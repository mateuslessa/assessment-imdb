import os
import pandas as pd
from sqlalchemy import create_engine


def carregar_dataframe_movies(db_url = "sqlite:///data/imdb.db"):
    """
    Lê todos os registros da tabela 'movies' do banco de dados
    e devolve um DataFrame com esses dados.

    Parâmetros:
        db_url (str, opcional): URL de conexão com o banco.
            Padrão: 'sqlite:///data/imdb.db'.

    Retorno:
        pandas.DataFrame: DataFrame contendo todos os registros da tabela 'movies'.
    """
    engine = create_engine(db_url)
    df_movies = pd.read_sql("SELECT * FROM movies", con=engine)
    return df_movies


def carregar_dataframe_series(db_url = "sqlite:///data/imdb.db"):
    """
    Lê todos os registros da tabela 'series' do banco de dados
    e devolve um DataFrame com esses dados.

    Parâmetros:
        db_url (str, opcional): URL de conexão com o banco.
            Padrão: 'sqlite:///data/imdb.db'.

    Retorno:
        pandas.DataFrame: DataFrame contendo todos os registros da tabela 'series'.
    """
    engine = create_engine(db_url)
    df_series = pd.read_sql("SELECT * FROM series", con=engine)
    return df_series


def exportar_csv_json(df_movies, df_series, pasta_saida = 'data'):
    """
    Exporta os DataFrames de filmes e séries para arquivos CSV e JSON.

    Arquivos gerados (dentro de pasta_saida):
        - movies.csv
        - series.csv
        - movies.json
        - series.json

    Parâmetros:
        df_movies (pandas.DataFrame): DataFrame com os filmes.
        df_series (pandas.DataFrame): DataFrame com as séries.
        pasta_saida (str, opcional): Pasta onde os arquivos serão salvos.
            Padrão: 'data'.

    Em caso de erro (por exemplo, permissão ou caminho inválido),
    exibe uma mensagem no terminal.
    """
    # Garante que a pasta de saída existe
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_movies_csv = os.path.join(pasta_saida, 'movies.csv')
    caminho_series_csv = os.path.join(pasta_saida, 'series.csv')
    caminho_movies_json = os.path.join(pasta_saida, 'movies.json')
    caminho_series_json = os.path.join(pasta_saida, 'series.json')

    # Exportando movies.csv
    try:
        df_movies.to_csv(caminho_movies_csv, index=False, encoding='utf-8')
        print(f'\nArquivo "movies.csv" exportado com sucesso em "{caminho_movies_csv}"!')
    except Exception as excecao:
        print('\nAviso: Ocorreu um erro ao exportar o arquivo "movies.csv":')
        print(excecao)

    # Exportando series.csv
    try:
        df_series.to_csv(caminho_series_csv, index=False, encoding='utf-8')
        print(f'Arquivo "series.csv" exportado com sucesso em "{caminho_series_csv}"!')
    except Exception as excecao:
        print('Aviso: Ocorreu um erro ao exportar o arquivo "series.csv":')
        print(excecao)

    # Exportando movies.json
    try:
        df_movies.to_json(caminho_movies_json, orient='records',
                          indent=4, force_ascii=False)
        print(f'Arquivo "movies.json" exportado com sucesso em "{caminho_movies_json}"!')
    except Exception as excecao:
        print('Aviso: Ocorreu um erro ao exportar o arquivo "movies.json":')
        print(excecao)

    # Exportando series.json
    try:
        df_series.to_json(caminho_series_json, orient='records',
                          indent=4, force_ascii=False)
        print(f'Arquivo "series.json" exportado com sucesso em "{caminho_series_json}"!')
    except Exception as excecao:
        print('Aviso: Ocorreu um erro ao exportar o arquivo "series.json":')
        print(excecao)


def obter_categoria_textual(nota_float):
    """
    Classifica uma nota numérica em uma categoria textual.

    Regras:
        - nota >= 9.0               -> "Obra-prima"
        - 8.0 <= nota < 9.0         -> "Excelente"
        - 7.0 <= nota < 8.0         -> "Bom"
        - nota < 7.0                -> "Mediano"

    Parâmetros:
        nota_float (float): Nota do filme (rating).

    Retorno:
        str: Categoria textual correspondente à nota.
    """
    if nota_float >= 9.0:
        return 'Obra-prima'
    elif 9.0 > nota_float >= 8.0:
        return 'Excelente'
    elif 8.0 > nota_float >= 7.0:
        return 'Bom'
    else:
        return 'Mediano'


def adicionar_categoria(df_movies):
    """
    Adiciona ao DataFrame de filmes uma coluna 'categoria'
    baseada na coluna 'rating'.

    Parâmetros:
        df_movies (pandas.DataFrame): DataFrame contendo, entre outras,
            a coluna 'rating'.

    Retorno:
        pandas.DataFrame: Mesmo DataFrame de entrada, agora com a
        coluna adicional 'categoria'.
    """
    df_movies['categoria'] = df_movies['rating'].apply(obter_categoria_textual)
    return df_movies


def resumo_categoria_ano(df_movies):
    """
    Cria um resumo em formato de tabela com a quantidade de filmes
    por categoria e ano de lançamento.

    Linhas:
        - categoria (ex.: "Obra-prima", "Excelente", ...)

    Colunas:
        - year (ano de lançamento)

    Células:
        - quantidade de filmes naquela combinação (categoria, ano).

    Parâmetros:
        df_movies (pandas.DataFrame): DataFrame de filmes contendo as
            colunas 'categoria' e 'year'.

    Retorno:
        pandas.DataFrame: Tabela resumo com categorias nas linhas e
        anos nas colunas.
    """
    resumo = (
        df_movies
        .groupby(['categoria', 'year'])
        .size() # conta quantos filmes há em cada (categoria, year)
        .unstack(fill_value=0) # transforma "year" em colunas, preenchendo vazios com 0
        .sort_index() # ordena por categoria (apenas para organizar melhor)
    )
    return resumo

