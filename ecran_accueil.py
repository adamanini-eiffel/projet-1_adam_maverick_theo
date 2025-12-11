import fltk

class Accueil:

    def __init__(self):

        # Permet de savoir si l'utilisateur est encore sur l'écran d'accueil du jeu
        self.statue = True

        self.mode = "solo"

    def affichage(self):

        fltk.cree_fenetre(1000, 1000)

        self.creation()

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == "ClicGauche":

                if fltk.abscisse(ev) >= 1000 * 1/ 3 - 70 and fltk.abscisse(ev) <= 1000 * 1/ 3 + 70 and fltk.ordonnee(ev) >= 530 and fltk.ordonnee(ev) <= 670:

                    self.statue = False

                    break

                if fltk.abscisse(ev) >= 1000 * 2/ 3 - 70 and fltk.abscisse(ev) <= 1000 * 2/ 3 + 70 and fltk.ordonnee(ev) >= 530 and fltk.ordonnee(ev) <= 670:

                    self.statue = False

                    self.mode = "multi"

                    break
            else:
                pass

            fltk.mise_a_jour()

        if not self.statue:
            fltk.ferme_fenetre()

    def creation(self):

        fltk.texte(500, 300, "Bienvenue sur PickTok !", couleur="red", ancrage='center', police = "monsterrat")


        fltk.texte(1000 * 1/ 3, 600, "Play solo",taille = 20, ancrage='center', police = "monsterrat")
        fltk.cercle(1000 * 1/ 3,600, 70, epaisseur = 5)


        fltk.texte(1000 * 2/ 3, 600, "Play multi",taille = 20, ancrage='center', police = "monsterrat")
        fltk.cercle(1000 * 2 / 3, 600, 70, epaisseur = 5)


        fltk.texte(1000 * 1/ 3, 760, "Score",taille = 20, ancrage='center', police = "monsterrat")

        fltk.texte(1000 * 1 / 3, 785, "All Time", taille=20, ancrage='center', police="monsterrat")

        fltk.cercle(1000 * 1 / 3, 775, 70, epaisseur = 5)
