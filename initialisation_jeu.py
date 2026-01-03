from affichage import Plateau
import jetons
import joueur


class Case:

    def __init__(self, x, y):

        self.jeton = 0

        self.x = x
        self.y = y

    def __str__(self):
        return f"Case de {self.jeton} jeton(s) x:{self.x} y:{self.y}"


def initialisation_plateau(nb_case_largeur, nb_case_hauteur, longueur_case):

    plateau = []

    coord_case_y = 0

    for indexCaseColonne in range(1,nb_case_hauteur + 1):

        ligne = []
        coord_case_x = 0

        for indexCaseLigne in range(1,nb_case_largeur + 1):

            newCase = Case(coord_case_x, coord_case_y)
            ligne.append(newCase)

            coord_case_x = indexCaseLigne * longueur_case

        plateau.append(ligne)
        coord_case_y = indexCaseColonne  * longueur_case

    return plateau

def creation_plateau(plateau_case, plateau_jetons):

    for i in range(len(plateau_jetons)):

        for j in range(len(plateau_jetons[i])):

            plateau_case[i][j].jeton = plateau_jetons[i][j]

    return plateau_case

longueur_case = 50


def liste_vers_tableau(liste, lignes, colonnes):
    return [liste[i*colonnes:(i+1)*colonnes] for i in range(lignes)]


def fusion(plateau_case, plateau_jetons):

    for i in range (len(plateau_jetons)):

        for j in range (len(plateau_jetons[i])):

            plateau_case[i][j].jeton = plateau_jetons[i][j]

    return plateau_case

def initialisation_jetons(plateau):

    for case in plateau[0]:

        if case.jeton is not None:

            case.jeton.est_cache = False

    return plateau


def creation_jeu() :

    return Plateau(longueur_case, 1000, 600, initialisation_jetons(fusion(initialisation_plateau(8, 10, longueur_case), liste_vers_tableau(jetons.Grille(8, 10, 0.3).grille, 10, 8))))

def charger_la_partie():

    with open("sauvegardes/test1.scores", "r") as file:

        f = file.readlines()

    sauvegarde_plateau = dict_to_plateau(str_dict_to_dict(f[1]))

    etat_jeton_capture =  str_to_list_etat(f[2])

    etat_jeton_cache = str_to_list_etat(f[3])

    sauvegarde_plateau = mise_a_jour_etat_jeton(sauvegarde_plateau, etat_jeton_capture, etat_jeton_cache)

    plateau = Plateau(longueur_case, 1000, 600, sauvegarde_plateau)

    plateau.logique_score_ratelier.nb_points = int(f[8])

    plateau.logique_score_ratelier.ratelier.jetons = charger_ratelier(f[5])

    if len(f[7])== len("multijoueur = True "):

        partie = sauvegarde_multi(plateau, f[10][-2], f[11][-2], f[12][-2])

    return plateau

def sauvegarde_multi(plateau, tour, j1, j2):

    plateau.tour = int(tour)

    plateau.liste_joueurs.append(joueur.Joueur("joueur_1"))
    plateau.liste_joueurs.append(joueur.Joueur("joueur_2"))

    plateau.liste_joueurs[0].score = int(j1)
    plateau.liste_joueurs[1].score = int(j2)

    return plateau

def charger_ratelier(ratelier):

    if ratelier == 'None':

        return []

    else :

        ratelier = ratelier.strip().split(" ")

        ratelier_1 = [jetons.Jeton(i, 0, 0) for i in ratelier]

    return ratelier_1


def str_dict_to_dict(s: str) -> dict:

    d = {}

    s = s[1:-2]

    s = s.split(",")

    for item in s:

        if not item.strip():
            continue

        key, value = item.strip().split(":")
        x, y = key[1:-1].split(";")

        d[(int(x), int(y))] = None if value == "None" else value

    return d

def str_to_list_etat(liste):

    return liste.strip().split(",")

def dict_to_plateau(dico):

    liste_jetons = []

    tableau_coord = initialisation_plateau(8, 10, longueur_case)

    for value in dico.values():


        if value == None:

            liste_jetons.append(None)

        else:

            liste_jetons.append(jetons.Jeton(value, 0, 0))

    tableau_jetons = liste_vers_tableau(liste_jetons, 10, 8)

    return fusion(tableau_coord, tableau_jetons)

def mise_a_jour_etat_jeton (plateau, liste_etat_capture, liste_etat_cache):

    liste_etat_capture = liste_vers_tableau(liste_etat_capture, 10, 8)

    liste_etat_cache = liste_vers_tableau(liste_etat_cache, 10, 8)

    for i in range(len(plateau)):

        for j in range(len(plateau[i])):

            if plateau[i][j].jeton != None:


                if liste_etat_capture[i][j] == "True":

                    plateau[i][j].jeton.est_capture = True

                else:

                    plateau[i][j].jeton.est_capture = False


                if liste_etat_cache[i][j] == "True":

                    plateau[i][j].jeton.est_cache = True

                else:

                    plateau[i][j].jeton.est_cache = False

    return plateau
