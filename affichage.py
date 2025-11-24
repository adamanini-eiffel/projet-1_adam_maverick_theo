import fltk
from fltk import remplissage
from logique import Regles
from jetons import Ratelier

class Plateau:

    def __init__(self, longueur_case, largeur_plateau, hauteur_plateau, plateau, ratelier: Ratelier):

        self.largeur_plateau = largeur_plateau
        self.hauteur_plateau = hauteur_plateau

        self.longueur_case = longueur_case

        self.plateau = plateau
        self.ratelier = ratelier
        self.regles=Regles()

    def affichage_case(self):

        for i in range(len(self.plateau)):

            for j in range(len(self.plateau[i])):

                if self.plateau[i][j].jeton is not None:

                    fltk.rectangle(
                        self.plateau[i][j].x,
                        self.plateau[i][j].y,
                        self.plateau[i][j].x + self.longueur_case,
                        self.plateau[i][j].y + self.longueur_case
                    )

                else:

                    fltk.rectangle(
                        self.plateau[i][j].x,
                        self.plateau[i][j].y,
                        self.plateau[i][j].x + self.longueur_case,
                        self.plateau[i][j].y + self.longueur_case,
                        remplissage="black",
                    )



    def affichage_jeton(self):

        for i in range(len(self.plateau)):

            for j in range(len(self.plateau[i])):

                if self.plateau[i][j].jeton is not None and not self.plateau[i][j].jeton.est_capture and \
                        self.plateau[i][j].jeton.est_cache:

                    fltk.cercle(
                        (self.plateau[i][j].x * 2 + self.longueur_case) // 2,
                        (self.plateau[i][j].y * 2 + self.longueur_case) // 2,
                        20,
                        remplissage="white"
                    )

                    fltk.cercle(
                        (self.plateau[i][j].x * 2 + self.longueur_case) // 2,
                        (self.plateau[i][j].y * 2 + self.longueur_case) // 2,
                        10,
                        remplissage=str(self.plateau[i][j].jeton)
                    )

                elif self.plateau[i][j].jeton is not None and not self.plateau[i][j].jeton.est_capture and \
                        not self.plateau[i][j].jeton.est_cache:

                    fltk.cercle(
                        (self.plateau[i][j].x * 2 + self.longueur_case) // 2,
                        (self.plateau[i][j].y * 2 + self.longueur_case) // 2,
                        20,
                        remplissage=str(self.plateau[i][j].jeton)
                    )

                elif self.plateau[i][j].jeton is not None and self.plateau[i][j].jeton.est_capture and \
                        not self.plateau[i][j].jeton.est_cache:

                    fltk.cercle(
                        (self.plateau[i][j].x * 2 + self.longueur_case) // 2,
                        (self.plateau[i][j].y * 2 + self.longueur_case) // 2,
                        20,
                        remplissage="white"
                    )

    def partie(self):

        fltk.cree_fenetre(self.largeur_plateau, self.hauteur_plateau)


        self.affichage_case()

        while True:

            self.affichage_jeton()

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == "ClicGauche":

                if self.action_joueur(fltk.abscisse(ev), fltk.ordonnee(ev)) != 0:

                    ligne_case, colonne_case = self.action_joueur(fltk.abscisse(ev), fltk.ordonnee(ev))

                    if self.plateau[colonne_case][ligne_case].jeton is not None and not self.plateau[colonne_case][
                        ligne_case].jeton.est_cache:
                        self.plateau[colonne_case][ligne_case].jeton.est_capture = True
                        self.regles.modifier_ratelier(self.plateau[colonne_case][ligne_case].jeton)

                        self.get_voisins(self.plateau[colonne_case][ligne_case], colonne_case, ligne_case)



            elif tev == 'Quitte':  # on sort de la boucle
                break

            else:  # dans les autres cas, on ne fait rien
                pass

            fltk.mise_a_jour()

        fltk.ferme_fenetre()



    def ajouter_ratelier(self, jeton):

        pass

    def get_voisins(self, case, colonne_case, ligne_case):


        if ligne_case - 1 >= 0 and self.plateau[colonne_case][ligne_case - 1].jeton is not None and \
                self.plateau[colonne_case][ligne_case - 1].jeton.est_cache:
            self.plateau[colonne_case][ligne_case - 1].jeton.est_cache = False


        if ligne_case + 1 <= 7 and self.plateau[colonne_case][ligne_case + 1].jeton is not None and \
                self.plateau[colonne_case][ligne_case + 1].jeton.est_cache:
            self.plateau[colonne_case][ligne_case + 1].jeton.est_cache = False


        if colonne_case - 1 >= 0 and self.plateau[colonne_case - 1][ligne_case].jeton is not None and \
                self.plateau[colonne_case - 1][ligne_case].jeton.est_cache:
            self.plateau[colonne_case - 1][ligne_case].jeton.est_cache = False


        if colonne_case + 1 <= 7 and self.plateau[colonne_case + 1][ligne_case].jeton is not None and \
                self.plateau[colonne_case + 1][ligne_case].jeton.est_cache:
            self.plateau[colonne_case + 1][ligne_case].jeton.est_cache = False

            print("e")

    def action_joueur(self, click_x, click_y):

        # index de la case
        case_x = click_x // self.longueur_case
        case_y = click_y // self.longueur_case

        if click_x > self.plateau[9][7].x + self.longueur_case or click_y > self.plateau[9][7].y + self.longueur_case:

            return 0

        else:

            return case_x, case_y
