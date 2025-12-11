from affichage import Plateau
import jetons


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

plateau_case = initialisation_plateau(8, 10, longueur_case)

g = jetons.Grille(8, 10, 0.3)

def liste_vers_tableau(liste, lignes, colonnes):
    return [liste[i*colonnes:(i+1)*colonnes] for i in range(lignes)]

plateau_jetons = liste_vers_tableau(g.grille, 10, 8)

def fusion(plateau_case, plateau_jetons):

    for i in range (len(plateau_jetons)):

        for j in range (len(plateau_jetons[i])):

            plateau_case[i][j].jeton = plateau_jetons[i][j]

    return plateau_case

plateau_case = fusion(plateau_case, plateau_jetons)

def initialisation_jetons(plateau):

    for case in plateau[0]:

        if case.jeton is not None:

            case.jeton.est_cache = False

    return plateau

plateau_case = initialisation_jetons(plateau_case)

def creation_jeu() :

    return Plateau(longueur_case, 1000, 600, plateau_case)
