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

    # Obtient la page du casting du film
    htmlCast = requests.get(movieLink + "fullcredits")
    casting = BeautifulSoup(htmlCast.text, "html.parser")

    return movie, casting


def getName(movie):
    name = movie.find("h1", {"data-testid": "hero-title-block__title"}).text

    return name


def getYear(movie):
    try:
        year = movie.find("li", {"class": "ipc-inline-list__item"}).a.text    # Trouve année
    except AttributeError:
        year = "No year indicated"

    return year


def getRuntime(movie):
    tech = movie.find("li", {"data-testid": "title-techspec_runtime"})
    if not tech:
        print("Tech section not found.")

    try:
        runtime = tech.find("div", {"class": "ipc-metadata-list-item__content-container"}).text  # Trouve la durée
    except AttributeError as ae:
        print(ae)
        runtime = "No indication of the duration of the film"

    return runtime


def getRating(movie):
    score = movie.find("div", {"data-testid": "hero-rating-bar__aggregate-rating__score"})
    if not score:
        print("Score section not found.")

    try:
        rating = score.find("span", {"class": "sc-7ab21ed2-1 jGRxWM"}).text  # Trouve la durée
    except AttributeError as ae:
        print(ae)
        rating = "No rating"

    return rating


def getReleaseDate(movie):
    details = movie.find("li", {"data-testid": "title-details-releasedate"})
    if not details:
        print("Details section not found.")

    try:
        release_date = details.find("a", {"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text  # Trouve la durée
    except AttributeError as ae:
        print(ae)
        release_date = "No exact release date"

    return release_date


def getGenres(movie):
    hist = movie.find("li", {"data-testid": "storyline-genres"})
    if not hist:
        print("Hist section not found.")

    genres = [i.text for i in hist.find_all("a", {"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})]

    return genres


def getPlot(movie):
    plot = movie.find("p", {"data-testid": "plot"}).span.text

    return plot


def getDirector(casting):
    director = casting.find("td", {"class": "name"}).a.text.strip()

    return director


def getStory(movie):
    hist = movie.find("section", {"data-testid": "Storyline"})
    if not hist:
        print("Hist section not found.")

    story = hist.find("div", {"data-testid": "storyline-plot-summary"}).text

    return story


def getWriters(casting):
    cred = casting.find("table", {"class": "simpleTable simpleCreditsTable"})
    cred_suiv = cred.find_next_sibling("table")
    if not cred_suiv:
        print("Credits section not found.")

    writers = [i.text for i in cred_suiv.find_all("td", {"class": "name"})]

    return writers


def getCasting(casting):
    table_cast = casting.find("table", {"class": "cast_list"})

    cast = table_cast.find_all("img", {"class": "loadlate"}, alt=True)
    '''for i in cast:
        print(i["alt"])'''

    return cast


if __name__ == "__main__":
    movieDetails = {}

    #movieName = input("Enter the name of the movie whose information you want to know \n")
    movieName = "Dune"

    movie, casting = getMovieDetails(movieName)
    if movie is None:
        print("The film you requested was not found")
        quit()

    movieDetails["name"] = getName(movie)
    movieDetails["year"] = getYear(movie)
    print("\n {movie} ({year})".format(movie=movieDetails["name"], year=movieDetails["year"]))

    movieDetails["runtime"] = getRuntime(movie)
    print("Runtime:", movieDetails["runtime"])

    movieDetails["rating"] = getRating(movie)
    print("Rating:", movieDetails["rating"] + "/10")

    movieDetails["releaseDate"] = getReleaseDate(movie)
    print("Release Date:", movieDetails["releaseDate"])

    movieDetails["genres"] = getGenres(movie)
    print("Genres:", ", ".join([str(i) for i in movieDetails["genres"]]))

    movieDetails["plot"] = getPlot(movie)
    print("Plot summary: \n", movieDetails["plot"])

    movieDetails["director"] = getDirector(casting)
    print("Director:", movieDetails["director"])

    movieDetails["story"] = getStory(movie)
    print("Story: \n", pformat(movieDetails["story"]))

    movieDetails["writers"] = getWriters(casting)
    list_writers = []
    for i in movieDetails["writers"]:
        list_writers.append(i.strip())
    print("Writers:", ", ".join([str(i) for i in list_writers]))

    cast = getCasting(casting)
    list_cast = []
    for i in cast:
        list_cast.append(i["alt"])
    print("Casting: \n", pformat(", ".join([str(i) for i in list_cast])))