import fltk

class Accueil:

    def __init__(self):

        # Permet de savoir si l'utilisateur est encore sur l'écran d'accueil du jeu
        self.statue = True

    def affichage(self):

        fltk.cree_fenetre(1000, 1000)

        self.creation()

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == "ClicGauche":

                print(True, fltk.abscisse(ev), fltk.ordonnee(ev))

                if fltk.abscisse(ev) >= 450 and fltk.abscisse(ev) <= 550 and fltk.ordonnee(ev) >= 550 and fltk.ordonnee(ev) <= 650:


                    self.statue = False

                    break

            else:
                pass

            fltk.mise_a_jour()

        if not self.statue:
            fltk.ferme_fenetre()

    def creation(self):

        fltk.texte(500, 300, "Bienvenue sur PickTok !", couleur="red", ancrage='center', police = "monsterrat")

        fltk.texte(500, 600, "Play", ancrage='center', police = "mmonsterrat")

        fltk.cercle(500,600, 50, epaisseur = 6)

