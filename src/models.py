class TV:
    """
    Classe base para representar qualquer mídia de TV/cinema.

    Atributos:
        title (str): Título da obra.
        year (int): Ano de lançamento.
    """
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f'"{self.title}" ({self.year})'


class Movie(TV):
    """
    Classe que representa um filme, especializada a partir de TV.

    Atributos:
        title (str): Título do filme.
        year (int): Ano de lançamento.
        rating (float): Nota do filme no IMDb.
    """
    def __init__(self, title, year, rating):
        # Herdando os atributos title e year da classe pai 'TV'
        super().__init__(title, year)
        # Adicionando o atributo rating
        self.rating = rating

    # Sobrescrevendo o método __str__
    def __str__(self):
        return f'"{self.title}" ({self.year}) - Nota: {self.rating}'


class Series(TV):
    """
    Classe que representa uma série, especializada a partir de TV.

    Atributos:
        title (str): Título da série.
        year (int): Ano de lançamento.
        seasons (int): Quantidade de temporadas.
        episodes (int): Quantidade total de episódios.
    """
    def __init__(self, title, year, seasons, episodes):
        # Herdando os atributos title e year da classe pai 'TV'
        super().__init__(title, year)
        # Adicionando os atributos seasons e episodes
        self.seasons = seasons
        self.episodes = episodes

    # Sobrescrevendo o método __str__
    def __str__(self):
        return f'"{self.title}" ({self.year}) - Temporadas: {self.seasons}, Episódios: {self.episodes}'


def criar_catalogo(lista_filmes_scraping):
    """
    Cria uma lista de objetos (catalog) a partir dos dados do scraping.

    A partir da lista de dicionários retornada pelo scraping do IMDb:
        - cria um objeto Movie para cada filme;
        - adiciona manualmente duas séries fictícias (Breaking Bad e Better Call Saul).

    Parâmetros:
        lista_filmes_scraping (list[dict]): Lista de filmes obtida do scraping,
            em que cada dicionário possui as chaves:
            'titulo', 'ano_lancamento', 'nota'.

    Retorno:
        list[TV]: Lista contendo objetos Movie e Series.
    """
    catalog = []

    # Utilizando os dados do exercício 2 (lista de dicionários representando os filmes)
    for filme in lista_filmes_scraping:
        titulo = filme['titulo']
        ano = filme['ano_lancamento']
        nota = filme['nota']

        # Criando objeto da classe Movie a partir dos dados no dicionário
        objeto_movie = Movie(title=titulo, year=ano, rating=nota)

        # Armazenando na lista catalog
        catalog.append(objeto_movie)

    # Criando manualmente dois objetos Series e inserindo na lista catalog
    series1 = Series(title='Breaking Bad', year=2008, seasons=5, episodes=62)
    catalog.append(series1)
    series2 = Series(title='Better Call Saul', year=2015, seasons=6, episodes=63)
    catalog.append(series2)

    return catalog

