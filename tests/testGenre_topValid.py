import requests
from bs4 import BeautifulSoup


def getMovieDetails(movieName):
    url = "https://www.imdb.com/"                                       # URL du site web choisi = IMDB
    query = "/search/title?title="                                      # Requête pour trouver le titre du film/série
    movieNameQuery = query + "+".join(movieName.strip().split(" "))     # Requête(query) formé

    # Page Web obtenue et analysée
    html = requests.get(url+movieNameQuery+"&title_type=feature")
    bS = BeautifulSoup(html.text, "html.parser")

    # Obtient le premier film qui apparait dans la section "titre"
    result = bS.find("h3", {"class": "lister-item-header"})

    if result is None:
        return None

    movieLink = url + result.a.attrs["href"]

    # Obtient la page du film avec les détails du film
    html = requests.get(movieLink)
    movie = BeautifulSoup(html.text, "html.parser")

    return movie


def getGenres(movie):
    '''details = movie.find("li", {"data-testid": "title-details-releasedate"})
    if not details:
        print("Details section not found.")'''

    genres = [i.text for i in movie.findAll("a", {"class": "sc-16ede01-3"})]

    return genres


if __name__ == "__main__":
    movieDetails = {}

    movieName = "Dune"
    movieDetails = getMovieDetails(movieName)
    if movieDetails is None:
        print("The film you requested was not found")
        quit()

    movie = getMovieDetails(movieName)

    movieDetails["genres"] = getGenres(movie)
    print(", ".join([str(i) for i in movieDetails["genres"]]))