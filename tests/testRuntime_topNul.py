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


def getRuntime(movie):
    tech = movie.find("ul", {"data-testid": "hero-title-block__metadata"})
    if not tech:
        print("Tech section not found.")

    try:
        runtime = tech.find("li", {"class": "ipc-inline-list__item"}).text  # Trouve la durée
    except AttributeError as ae:
        print(ae)
        runtime = "No indication of the duration of the film"

    return runtime

if __name__ == "__main__":
    movieDetails = {}

    movieName = "Dune"
    movieDetails = getMovieDetails(movieName)
    if movieDetails is None:
        print("The film you requested was not found")
        quit()

    movie = getMovieDetails(movieName)

    movieDetails["runtime"] = getRuntime(movie)
    print("Runtime:", movieDetails["runtime"])