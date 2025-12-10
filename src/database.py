from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

from .models import Movie, Series  # import relativo


# Criando a base para o ORM
Base = declarative_base()


class MovieDB(Base):
    """
    Classe de mapeamento ORM para a tabela 'movies' no banco de dados.

    Campos:
        id (int): Chave primária, autoincremento.
        title (str): Título do filme (único, não nulo).
        year (int): Ano de lançamento.
        rating (float): Nota do filme no IMDb.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    year = Column(Integer)
    rating = Column(Float)

    def __repr__(self):
        return f'"{self.title}" ({self.year}) - Nota: {self.rating}'


class SeriesDB(Base):
    """
    Classe de mapeamento ORM para a tabela 'series' no banco de dados.

    Campos:
        id (int): Chave primária, autoincremento.
        title (str): Título da série (único, não nulo).
        year (int): Ano de lançamento.
        seasons (int): Quantidade de temporadas.
        episodes (int): Quantidade de episódios.
    """
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    year = Column(Integer)
    seasons = Column(Integer)
    episodes = Column(Integer)

    def __repr__(self):
        return f'"{self.title}" ({self.year}) - Temporadas: {self.seasons}, Episódios: {self.episodes}'


def criar_engine(db_url = "sqlite:///data/imdb.db"):
    """
    Cria e devolve um objeto engine do SQLAlchemy para o banco de dados.

    Parâmetros:
        db_url (str, opcional): URL de conexão com o banco.
            Padrão: 'sqlite:///data/imdb.db'.

    Retorno:
        sqlalchemy.Engine: Engine configurado para a URL informada.
    """
    return create_engine(db_url)


def criar_tabelas(engine):
    """
    Cria as tabelas 'movies' e 'series' no banco de dados, caso ainda não existam.

    Parâmetros:
        engine (sqlalchemy.Engine): Engine conectada ao banco onde
            as tabelas serão criadas.
    """
    Base.metadata.create_all(engine)


def salvar_catalogo_no_banco(catalog, engine):
    """
    Percorre a lista catalog (Movie e Series) e salva no banco de dados.

    Para cada item:
        - se for Movie, cria um registro em 'movies';
        - se for Series, cria um registro em 'series';
        - se o título já existir (violação de UNIQUE), o registro é ignorado
          e uma mensagem é exibida.

    Parâmetros:
        catalog (list[TV]): Lista contendo objetos Movie e Series.
        engine (sqlalchemy.Engine): Engine conectada ao banco onde
            os dados serão inseridos.
    """
    Session = sessionmaker(bind=engine) # Criando uma fábrica de sessões

    session = Session() # Criando uma sessão

    # Inserindo na base de dados os objetos Movie e Series armazenados na lista catalog (ex. 5)
    for item in catalog:
        if isinstance(item, Movie): # instância de Movie -> tabela movies
            # Instanciando um objeto MovieDB com os atributos do objeto Movie
            novo_registro = MovieDB(
                title=item.title,
                year=item.year,
                rating=item.rating
            )
        elif isinstance(item, Series): # instância de Series -> tabela series
            # Instanciando um objeto SeriesDB com os atributos do objeto Series
            novo_registro = SeriesDB(
                title=item.title,
                year=item.year,
                seasons=item.seasons,
                episodes=item.episodes
            )
        else:
            print('Item desconhecido, ignorando...')
            continue

        # Adicionando à sessão
        session.add(novo_registro)

        # Usando try-except para tratar tentativas de inserção de título duplicado
        try:
            # Tentando gravar a inserção
            session.commit()
        except IntegrityError: # Se violar a restrição de título único, dá erro de Integridade
            # Desfazendo a transação que falhou
            session.rollback()
            # Exibindo mensagem de erro
            print(f'Aviso: título duplicado ignorado: "{novo_registro.title}".')

    # Encerrando a sessão
    session.close()

