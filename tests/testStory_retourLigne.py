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


def getStory(movie):
    hist = movie.find("section", {"data-testid": "Storyline"})
    if not hist:
        print("Hist section not found.")

    story = hist.find("div", {"data-testid": "storyline-plot-summary"}).text

    return story


if __name__ == "__main__":
    movieDetails = {}

    movieName = "Dune"
    movieDetails = getMovieDetails(movieName)
    if movieDetails is None:
        print("The film you requested was not found")
        quit()

    movie = getMovieDetails(movieName)

    movieDetails["story"] = getStory(movie)
    print("Story: \n", movieDetails["story"])