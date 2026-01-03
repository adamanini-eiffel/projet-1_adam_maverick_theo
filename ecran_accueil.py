import fltk
import math

class Accueil:

    def __init__(self):

        # Permet de savoir si l'utilisateur est encore sur l'écran d'accueil du jeu
        self.statue = True

        self.mode = None

        self.charger_partie = False

    def affichage(self):

        fltk.cree_fenetre(1000, 1000)

        self.creation()

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == "ClicGauche":

                if self.clic_dans_cercle(fltk.abscisse(ev), fltk.ordonnee(ev), (1000 * 1/ 3,600), 70):

                    self.statue = False

                    self.mode = "solo"

                    break

                if self.clic_dans_cercle(fltk.abscisse(ev), fltk.ordonnee(ev), (1000 * 2 / 3, 600), 70):

                    self.statue = False

                    self.mode = "multi"

                    break

                if self.clic_dans_cercle(fltk.abscisse(ev), fltk.ordonnee(ev), (1000 / 2, 775), 70) :

                    self.charger_partie = True

                    self.statue = False

                    break


            fltk.mise_a_jour()

        if not self.statue:

            fltk.ferme_fenetre()

    def creation(self):

        fltk.texte(500, 300, "Bienvenue sur PickTok !", couleur="red", ancrage='center', police = "monsterrat")


        fltk.texte(1000 * 1/ 3, 600, "Play solo",taille = 20, ancrage='center', police = "monsterrat")
        fltk.cercle(1000 * 1/ 3,600, 70, epaisseur = 5)


        fltk.texte(1000 * 2/ 3, 600, "Play multi",taille = 20, ancrage='center', police = "monsterrat")
        fltk.cercle(1000 * 2 / 3, 600, 70, epaisseur = 5)



        fltk.texte(1000 / 2, 760, "Charger", taille=20, ancrage='center', police="monsterrat")
        fltk.texte(1000 / 2, 785, "Partie", taille=20, ancrage='center', police="monsterrat")
        fltk.cercle(1000 / 2, 775, 70, epaisseur = 5)

    def clic_dans_cercle(self,x_clic, y_clic, centre, rayon):

        x_centre, y_centre = centre

        distance = math.sqrt((x_clic - x_centre) ** 2 + (y_clic - y_centre) ** 2)

        return distance <= rayon
