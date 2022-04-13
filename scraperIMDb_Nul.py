import requests
from bs4 import BeautifulSoup


# Fonction pour obtenir les Détails du Film/Série
def getMovieDetails(movieName):
    url = "https://www.imdb.com/"                                       # URL du site web choisi = IMDB
    query = "/search/title?title="                                      # Requête pour trouver le titre du film/série
    movieDetails = {}                                                   # Dictionnaire vide pour stocker les détails
    movieNameQuery = query + "+".join(movieName.strip().split(" "))     # Requête(query) formé

    # Page Web obtenue et analysée
    html = requests.get(url+movieNameQuery+"&title_type=feature")
    bS = BeautifulSoup(html.text, "html.parser")

    # Obtient le premier film qui apparait dans la section "titre"
    result = bS.find("h3", {"class": "lister-item-header"})

    if result is None:
        return None

    movieLink = url + result.a.attrs["href"]
    movieDetails["name"] = result.a.text

    # Obtient la page du film avec les détails du film
    html = requests.get(movieLink)
    bS = BeautifulSoup(html.text, "html.parser")

    # Obtient les différentes sections de la page
    details = bS.find("section", {"data-testid": "Details"})
    genres = bS.find("section", {"data-testid": "storyline-genres"})
    tech = bS.find("li", {"data-testid": "title-techspec_runtime"})
    hist = bS.find("section", {"data-testid": "Storyline"})

    if not tech :
        print("Tech section not found.")
        #raise Exception("Tech section not found.")


    try:
        movieDetails["year"] = bS.find("li", {"class": "ipc-inline-list__item"}).a.text    # Trouve année
    except AttributeError:
        movieDetails["year"] = "No year indicated"                                                  # Si pas d'année

    # Notes, Genres, Durée, Date de sortie (essayer de fusionner ça avec année en haut)
    try:
        movieDetails["runtime"] = tech.find("div", {"class": "ipc-metadata-list-item__content-container"}).text  # Trouve la durée
        movieDetails["rating"] = bS.find("span", {"class": "sc-7ab21ed2-1"}).span.text   # Trouve la note
        movieDetails["releaseDate"] = details.find("li", {"class": "ipc-inline-list__item"})                          # Trouve la durée 
    except AttributeError as ae:
        print(ae)
        movieDetails["runtime"] = "No indication of the duration of the film"                                       # Si pas de durée
        movieDetails["rating"] = "No rating"                                        # Si pas de note
        movieDetails["releaseDate"] = "No exact release date"

    movieDetails["genres"] = [i.text for i in bS.findAll("a", {"class": "sc-16ede01-3"})]      # Trouve le genre
    #movieDetails["genres"] = [i.text for i in hist.find_all("li", {"data-testid": "storyline-genres"})]

    # Intrigue
    movieDetails["plot"] = bS.find("p", {"data-testid": "plot"}).span.text

    #Casting
    html = requests.get(movieLink + "fullcredits")
    bS = BeautifulSoup(html.text, "html.parser")

    # Réalisateurs, Scénaristes, Acteurs 
    movieDetails["directors"] = bS.find("td", {"class": "name"}).a.text.strip()                         # Trouve réalisateurs
    #movieDetails["writers"] = [i.text for i in bS[1].findAll("a") if "name" in i.attrs["href"]]     # Trouve scénaristes
    #movieDetails["writters"] = bS.findAll("col", {"class": "column1"})
    try:
        #movieDetails["cast"] = [i.text for i in bS[2].findAll("a") if "name" in i.attrs["href"]]    # Trouve acteurs
        movieDetails["cast"] = bS.findAll("tr", {"class": "odd, even"})
    except IndexError:
        movieDetails["cast"] = movieDetails ["writers"]                                                        # Si pas d'acteurs
        movieDetails["writers"] = "No information"  

    # Histoire   
    movieDetails["history"] = hist.find("div", {"data-testid": "storyline-plot-summary"}).text                                                                # Si pas de scénaristes

    # Retourne le dictionnaire avec les détails du film
    return movieDetails


if __name__ == "__main__":
    #movieName = input("Enter the name of the movie whose information you want to know \n")
    movieName = "Star Wars"
    movieDetails = getMovieDetails(movieName)
    if movieDetails is None:
        print("The film you requested was not found")
        quit()
    print("\n {movie} ({year})".format(movie = movieDetails["name"], year = movieDetails["year"]))  #DONE
    print("Runtime:", movieDetails["runtime"])                                                      #
    print("Rating:", movieDetails["rating"])                                                        #
    print("Release date:", movieDetails["releaseDate"])                                             #JE L'AVAIS
    print("Genres:", ", ".join(movieDetails["genres"]))                                             #DONE (MAIS VOIR AUTRE)
    #print("Genres:", movieDetails["genres"])                                                        #
    print("Plot summary: \n", movieDetails["plot"])                                                 #DONE (MAIS VOIR AUTRE)
    #print("Director(s):", ", ".join(movieDetails["directors"]))
    print("Director(s):", movieDetails["directors"])                                                #DONE
    '''reponse = input("Want to know a little more about the story? Write 'Yes'\n")
    if reponse == "Yes":
        print("Histoire: \n", movieDetails["history"])
    else:
        print("A bientot !")'''
    print("Histoire: \n", movieDetails["history"])
    print("Writer(s):", ", ".join(movieDetails["writers"]))                                         #
    print("Cast: \n", ", ".join(movieDetails["cast"]))                                              #
        

'''if __name__ == "__main__":
    movieName = input("Enter the name of the movie whose information you want to know \n")
    movieDetails = getMovieDetails(movieName)
    if movieDetails is None:
        print("The film you requested was not found")
        quit()    
    print("\n {movie} ({year})".format(movie = movieDetails["name"], year = movieDetails["year"]))  #DONE

    while True:
        choix = input("Voulez vous plus d'informations ? Sur la 'Duree' du film, son 'Score', son 'Genre', son 'Casting' ?")
        if choix == "Duree":
            print("Runtime:", movieDetails["runtime"])
        elif choix == "Score":
            print("Rating:", movieDetails["rating"])                                                        #
        elif choix == "Genre":
            print("Genres:", ", ".join(movieDetails["genres"]))
        elif choix == "Casting":
            print("Director(s):", movieDetails["directors"])
    print("Release date:", movieDetails["releaseDate"])                                             #JE L'AVAIS
    #print("Genres:", movieDetails["genres"])                       s                                 #
    print("Plot summary: \n", movieDetails["plot"])                                                 #DONE (MAIS VOIR AUTRE)
    #print("Director(s):", ", ".join(movieDetails["directors"]))                                                #DONE
    reponse = input("Want to know a little more about the story? Write 'Yes'\n")
    if reponse == "Yes":
        print("Histoire: \n", movieDetails["history"])
    else:
        quit()
    print("Writer(s):", ", ".join(movieDetails["writers"]))                                         #
    print("Cast: \n", ", ".join(movieDetails["cast"]))                                              #'''
