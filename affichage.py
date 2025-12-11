import fltk
from logique import Regles
import playeur


class Plateau:

    def __init__(self, longueur_case, largeur_plateau, hauteur_plateau, plateau):

        self.largeur_plateau = largeur_plateau
        self.hauteur_plateau = hauteur_plateau

        self.longueur_case = longueur_case

        self.plateau = plateau
        self.logique_score_ratelier = Regles()

        self.liste_joueurs = []
        self.tour = 1


    def affichage_case(self):

        for ligne in self.plateau:

            for case in ligne:
                remplissage = None if case.jeton is not None else "black"

                fltk.rectangle(
                    case.x,
                    case.y,
                    case.x + self.longueur_case,
                    case.y + self.longueur_case,
                    remplissage=remplissage
                )

    def affichage_jeton(self):

        for col in self.plateau:

            for case in col:

                jeton = case.jeton

                if jeton is None:
                    continue

                cx = (case.x * 2 + self.longueur_case) // 2
                cy = (case.y * 2 + self.longueur_case) // 2

                if not jeton.est_capture and jeton.est_cache:

                    remplissage1 = "white"
                    remplissage2 = str(jeton)

                    fltk.cercle(cx, cy, 20, remplissage=remplissage1)
                    fltk.cercle(cx, cy, 10, remplissage=remplissage2)

                elif not jeton.est_capture and not jeton.est_cache:

                    remplissage = str(jeton)
                    fltk.cercle(cx, cy, 20, remplissage=remplissage)

                elif jeton.est_capture and not jeton.est_cache:

                    remplissage = "white"
                    fltk.cercle(cx, cy, 20, remplissage=remplissage)

    def deroulement_partie(self):

        fltk.cree_fenetre(self.largeur_plateau, self.hauteur_plateau)

        self.affichage_case()
        self.affichage_jeton()

        while True:

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == "ClicGauche":

                ligne_case, colonne_case = self.action_joueur(fltk.abscisse(ev), fltk.ordonnee(ev))

                case_selectionner = self.plateau[colonne_case][ligne_case]

                print(case_selectionner.jeton.est_cache)

                if case_selectionner.jeton is not None and not case_selectionner.jeton.est_cache and not case_selectionner.jeton.est_capture:

                    case_selectionner.jeton.capturer()

                    case_selectionner.jeton.retourner()

                    self.get_voisins(colonne_case, ligne_case)

                    for i in range(len(self.logique_score_ratelier.ratelier.jetons)):

                        fltk.efface("jeton_" + str(i))

                    if len(self.liste_joueurs) == 0:

                        self.logique_score_ratelier.modifier_ratelier(case_selectionner.jeton)

                    else :

                        tour = self.tour_joueur()

                        self.logique_score_ratelier.modifier_ratelier(case_selectionner.jeton)

                        self.liste_joueurs[tour].ajouter_points(self.logique_score_ratelier.nb_points)

                        self.logique_score_ratelier.nb_points = 0

                    self.affichage_ratelier()

                    fltk.efface("score")

                    fltk.efface("joueur")

                    self.affichage_score()

                self.affichage_jeton()

            elif tev == 'Quitte' or self.logique_score_ratelier.fin_de_partie:  # on sort de la boucle
                break

            else:  # dans les autres cas, on ne fait rien
                pass

            fltk.mise_a_jour()

        fltk.ferme_fenetre()

    def get_voisins(self, colonne_case, ligne_case):

        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ]

        for dc, dl in directions:
            c = colonne_case + dc
            l = ligne_case + dl

            if 0 <= c < len(self.plateau) and 0 <= l < len(self.plateau[0]):
                jeton = self.plateau[c][l].jeton

                if jeton is not None and jeton.est_cache:
                    jeton.est_cache = False

    def action_joueur(self, click_x, click_y):

        # index de la case
        case_x = click_x // self.longueur_case
        case_y = click_y // self.longueur_case

        if click_x > self.plateau[9][7].x + self.longueur_case or click_y > self.plateau[9][7].y + self.longueur_case:

            return 0

        else:

            return case_x, case_y

    def affichage_ratelier(self):

        x = self.largeur_plateau * 2 / 3
        y = 0

        for i in range(self.logique_score_ratelier.ratelier.taille_max):
            fltk.rectangle(
                x,
                y,
                x + self.longueur_case,
                y + self.longueur_case,
            )

            y += self.longueur_case

        y = 0

        liste_jeton_graphique = []


        for i in range(len(self.logique_score_ratelier.ratelier.jetons)):
            cx = (x * 2 + self.longueur_case) // 2
            cy = (y * 2 + self.longueur_case) // 2

            remplissage = str(self.logique_score_ratelier.ratelier.jetons[i])

            jeton = fltk.cercle(
                cx,
                cy,
                20,
                remplissage=remplissage,
                tag = "jeton_" + str(i)
            )

            liste_jeton_graphique.append(jeton)

            y += self.longueur_case

    def affichage_score(self):

        score = self.logique_score_ratelier.nb_points

        cx = self.largeur_plateau * 2 / 3
        cy = self.hauteur_plateau * 2 / 3

        fltk.rectangle(
            cx,
            cy,
            cx + self.largeur_plateau * 1 / 3,
            cy + self.hauteur_plateau * 1 / 3,
        )

        if len(self.liste_joueurs) == 0 :

            fltk.texte(
                cx + 15,
                cy + 75,
                "Votre score est de : " + str(score),
                taille = 20,
                tag = "score"
        )

        else :

            fltk.texte(
                cx + 15,
                cy + 45,
                "C'est le tour du : " + self.liste_joueurs[self.tour].pseudo,
                taille = 20,
                tag = "joueur"
            )

            fltk.texte(
                cx + 15,
                cy + 75,
                "Votre score est de : " + str(self.liste_joueurs[self.tour].score),
                taille = 20,
                tag = "score"
            )

    def multijoueur(self):

        for i in range(2):

            self.liste_joueurs.append(playeur.Joueur("joueur_" + str(i + 1)))

    def tour_joueur(self):

        if self.tour == 1:

            self.tour = 0

            return self.tour

        else :

            self.tour = 1

            return self.tour

