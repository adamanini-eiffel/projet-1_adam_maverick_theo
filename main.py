import initialisation_jeu
import ecran_fin
from ecran_accueil import Accueil

premiere_partie = initialisation_jeu.creation_jeu()

def picktok(partie = None):

    statue_partie = "aucune partie en en cours"

    accueil = Accueil()

    relance = False

    while statue_partie ==  "aucune partie en en cours" : 

        accueil.affichage()

        if not accueil.statue :

            statue_partie = "partie en cours"

    if accueil.charger_partie:

        partie = initialisation_jeu.charger_la_partie()

    elif partie == None :

        partie = initialisation_jeu.creation_jeu()

    if accueil.mode == "multi" and not accueil.charger_partie :

        partie.multijoueur()

    accueil.charger_partie = not accueil.charger_partie

    while statue_partie == "partie en cours":

        partie.deroulement_partie()

        statue_partie = "fin de partie"

    score = partie.logique_score_ratelier.nb_points

    fin = ecran_fin.Game_over()

    while statue_partie == "fin de partie" :

        if accueil.mode == "multi" :

            fin.affichage_multi(partie.liste_joueurs)

            relance = not fin.relancer_partie

            break

        else:

            fin.affichage_solo(score)

            relance = not fin.relancer_partie

            break

    if fin.relancer_partie :

        return picktok()

picktok(premiere_partie)
