import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    """
    Baixa o HTML de uma URL e devolve um objeto BeautifulSoup.

    Parâmetros:
        url (str): Endereço da página que será acessada.

    Retorno:
        BeautifulSoup: Objeto contendo a estrutura HTML da página,
        pronto para ser navegada e ter elementos extraídos.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.36'
        )
    }
    requisicao = urllib.request.Request(url, headers=headers)
    resposta = urllib.request.urlopen(requisicao)
    html = resposta.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def obter_filmes_top(url, n_filmes = 250):
    """
    Acessa a página do IMDb Top 250 e extrai dados dos filmes.

    Para cada filme encontrado, extrai:
        - título
        - ano de lançamento
        - nota (rating) no IMDb

    Parâmetros:
        url (str): URL da página do IMDb Top 250 (ou equivalente).
        n_filmes (int, opcional): Quantidade máxima de filmes a serem
            coletados a partir do topo do ranking. Padrão: 250.

    Retorno:
        list[dict]: Lista de dicionários, em que cada dicionário
        representa um filme com as chaves:
            - 'titulo' (str)
            - 'ano_lancamento' (int)
            - 'nota' (float)
    """
    soup = get_soup(url)

    ul_filmes = soup.find('ul', class_='ipc-metadata-list')

    # Cada filme é representado por uma tag 'li' de classe 'ipc-metadata-list-summary-item'
    tags_li_filmes = ul_filmes.find_all('li', class_='ipc-metadata-list-summary-item')

    lista_filmes = []

    for tag_li_filme in tags_li_filmes[:n_filmes]:
        # Cada título de filme é armazenado dentro de uma tag 'h3'
        tag_h3_titulo = tag_li_filme.find('h3', class_='ipc-title__text')
        # O título do filme é o texto contido pela tag
        texto_titulo = tag_h3_titulo.get_text(strip=True)

        # Extraindo o ano de lançamento do filme
        # É armazenado dentro da PRIMEIRA tag 'span' de classe 'cli-title-metadata-item' (usar método 'find')
        tag_span_ano_lancamento = tag_li_filme.find('span', class_='cli-title-metadata-item')
        texto_ano_lancamento = tag_span_ano_lancamento.get_text(strip=True)
        int_ano_lancamento = int(texto_ano_lancamento)

        # Extraindo a nota do filme
        tag_span_nota = tag_li_filme.find('span', class_='ipc-rating-star--rating')
        texto_nota = tag_span_nota.get_text(strip=True)
        float_nota = float(texto_nota.replace(',', '.'))

        # Montando um dicionário contendo título, ano de lançamento e nota no IMDb de cada filme
        filme = {
            'titulo': texto_titulo,
            'ano_lancamento': int_ano_lancamento,
            'nota': float_nota
        }

        # Armazenando na lista os dicionários dos filmes
        lista_filmes.append(filme)

    return lista_filmes

