import requests
from bs4 import BeautifulSoup
from pprint import pformat


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
    

def getCasting(casting):
    table_cast = casting.find("table", {"class": "cast_list"})

    cast = table_cast.find_all("img", {"class": "loadlate"}, alt=True)
    '''for i in cast:
        print(i["alt"])'''

    return cast
    


if __name__ == "__main__":
    movieDetails = {}
    movieName = "Dune"

    movie, casting = getMovieDetails(movieName)
    if movie is None:
        print("The film you requested was not found")
        quit()

    movieDetails["plot"] = getPlot(movie)
    print("Plot summary: \n", movieDetails["plot"])

    cast = getCasting(casting)
    list_cast = []
    for i in cast:
        list_cast.append(i["alt"])
    print("Casting:", pformat(", ".join([str(i) for i in list_cast])))