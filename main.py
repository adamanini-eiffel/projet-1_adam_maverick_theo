from initialisation_jeu import creation_jeu
import ecran_accueil
import ecran_fin
from logique import enregistrer

def picktok():

    statue_partie = "aucune partie en en cours"

    accueil = ecran_accueil.Accueil()

    while statue_partie ==  "aucune partie en en cours" :

        accueil.affichage()

        if not accueil.statue :

            statue_partie = "partie en cours"

    partie = creation_jeu()

    while statue_partie == "partie en cours":

        if accueil.mode == "multi" :

            partie.multijoueur()

        partie.deroulement_partie()

        statue_partie = "fin de partie"
        enregistrer("test1.scores", partie.plateau, partie.logique_score_ratelier.ratelier, False, None)

    score = partie.logique_score_ratelier.nb_points

    fin = ecran_fin.Game_over()

    while statue_partie == "fin de partie" :

        if accueil.mode == "multi" :

            fin.affichage_multi(partie.liste_joueurs)

        else:

            fin.affichage_solo(score)

        break

picktok()


