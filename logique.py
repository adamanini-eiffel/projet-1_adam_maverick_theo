from jetons import Ratelier, Grille
from os import mkdir

class Regles:

    def __init__(self, nb_points=0):
        self.nb_points = nb_points
        self.ratelier = Ratelier()
        self.grille = Grille(8, 10)
        self.fin_de_partie = False

    def points(self):

        if self.ratelier.triplette():
            self.nb_points += 1

            if self.ratelier.est_complet():
                self.nb_points += 1

        elif self.ratelier.est_complet():
            self.ratelier = Ratelier()
            self.nb_points = 0

    def modifier_ratelier(self, jeton):

        self.grille.capturer_jeton(jeton, self.ratelier)

        if self.ratelier.est_complet():
            if self.ratelier.triplette():
                self.nb_points += 2

            else:

                self.fin_de_partie = True
                self.nb_points = 0
                self.ratelier = Ratelier()

        elif self.ratelier.triplette() :
            self.nb_points += 1

def enregistrer(fichier: str, grille, ratelier: Ratelier, multijoueur: bool, score: dict[str, int], tour = 0, joueur_1 = 0, joueur_2 = 0):
    if not "sauvegardes/" in fichier:
        try:
            mkdir("./sauvegardes")
            print(f"Directory 'sauvegardes' created successfully.")
        except FileExistsError:
            print(f"Directory 'sauvegardes' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create 'sauvegardes'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        fichier = f"sauvegardes/{fichier}"

    with open(fichier, "w") as file:
        file.write("===== Grille =====\n")
        grille_str = '{'
        etat_cache_grille = ""
        etat_capture_grille = ""
        for ligne in grille:
            for case in ligne:
                grille_str += f"({case.x};{case.y}):{case.jeton}, "
                if not case.jeton is None:
                    etat_cache_grille += f"{case.jeton.est_cache},"
                    etat_capture_grille += f"{case.jeton.est_capture},"
                else :
                    etat_cache_grille += f"{None},"
                    etat_capture_grille += f"{None},"

        file.write(f"{grille_str}{'}'}\n")
        file.write(f"{etat_capture_grille}\n")
        file.write(f"{etat_cache_grille}\n")

        file.write("===== Ratelier =====\n")
        ratelier_str = ''
        for jeton in ratelier.jetons:
            ratelier_str += f"{jeton} "
        file.write(f"{ratelier_str if ratelier_str else None}\n")

        file.write("===== Scores =====\n")
        file.write(f"{multijoueur = }\n")
        file.write(f"{score}\n")

        if multijoueur:

            file.write("===== Multijoueur =====\n")
            file.write(f"{tour = }\n")
            file.write(f"{joueur_1 = }\n")
            file.write(f"{joueur_2 = }\n")
