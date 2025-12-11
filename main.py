from initialisation_jeu import creation_jeu
import ecran_accueil
import ecran_fin

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

    score = partie.logique_score_ratelier.nb_points

    fin = ecran_fin.Game_over()

    while statue_partie == "fin de partie" :

        if accueil.mode == "multi" :

            fin.affichage_multi(partie.liste_joueurs)

        else:

            fin.affichage_solo(score)

        break

picktok()


