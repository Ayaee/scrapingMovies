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

    # Casting
    htmlCast = requests.get(movieLink + "fullcredits")
    casting = BeautifulSoup(htmlCast.text, "html.parser")

    return movie, casting


def getPlot(movie):
    plot = movie.find("p", {"data-testid": "plot"}).span.text

    return plot
    

def getWriters(casting):
    cred = casting.find("table", {"class": "simpleTable simpleCreditsTable"})
    cred_suiv = cred.find_next_sibling("table")
    if not cred_suiv:
        print("Credits section not found.")

    writers = [i.text for i in cred_suiv.find_all("td", {"class": "name"})]

    return writers
    


if __name__ == "__main__":
    movieDetails = {}
    movieName = "Dune"

    movie, casting = getMovieDetails(movieName)
    if movie is None:
        print("The film you requested was not found")
        quit()

    movieDetails["plot"] = getPlot(movie)
    print("Plot summary: \n", movieDetails["plot"])

    movieDetails["writers"] = getWriters(casting)
    list_writers = []
    for i in movieDetails["writers"]:
        list_writers.append(i.strip())
    print("Writers:", ", ".join([str(i) for i in list_writers]))