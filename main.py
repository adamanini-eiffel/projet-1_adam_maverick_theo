import fltk
import random

import initialisation_jeu
import ecran_accueil

partie = "aucune partien en cours"

accueil = ecran_accueil.Accueil()

while partie ==  "aucune partien en cours" :

    accueil.affichage()

    if not accueil.statue :

        partie = "partie en cours"

initialisation_jeu.creation_jeu()


