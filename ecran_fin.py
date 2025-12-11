import fltk


class Game_over():

    def __init__(self):

        self.relancer_partie = False

    def affichage_solo(self,score):

        fltk.cree_fenetre(1000, 1000)

        fltk.texte(500, 300, "Voici le récap de votre partie !", ancrage='center', police = "monsterrat")

        fltk.texte(500, 350, "Score : " + str(score), ancrage='center', police="monsterrat")

        fltk.texte(500, 900, "Revenir à l'écran d'accueil", ancrage='center', police="monsterrat")

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == 'Quitte':
                break

            else:
                pass

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

    def affichage_multi(self,liste_score):

        fltk.cree_fenetre(1000, 1000)

        fltk.texte(500, 300, "Voici le récap de votre partie !", ancrage='center', police="monsterrat")

        if liste_score[0].score >= liste_score[1].score:

            fltk.texte(500, 350, "Le score du joueur " + str(liste_score[0].pseudo) + " est de : " +  str(liste_score[0].score), ancrage='center', police="monsterrat")

            fltk.texte(500, 400, "Le score du joueur " + str(liste_score[1].pseudo) + " est de : " + str(liste_score[1].score), ancrage='center', police="monsterrat")

        else :

            fltk.texte(500, 350, "Le score du joueur " + str(liste_score[1].pseudo) + " est de : " + str(liste_score[1].score),ancrage='center', police="monsterrat")

            fltk.texte(500, 400, "Le score du joueur " + str(liste_score[0].pseudo) + " est de : " + str(liste_score[0].score), ancrage='center', police="monsterrat")

        fltk.texte(500, 800, "Revenir à l'écran d'accueil", ancrage='center', police="monsterrat")

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == 'Quitte':
                break

            else:
                pass

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

