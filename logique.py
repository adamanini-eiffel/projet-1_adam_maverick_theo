from jetons import  Ratelier, Grille



class Regles:
    def __init__(self, nb_points = 0) -> None:
        self.nb_points = nb_points
        self.ratelier = Ratelier()
        self.grille = Grille(8, 10)


    def points(self)-> None:
        if self.ratelier.triplette() :
            self.nb_points += 1
            if self.ratelier.est_complet():
                self.nb_points += 1

        elif self.ratelier.est_complet():
            self.ratelier=Ratelier()
            self.nb_points=0



    def modifier_ratelier(self,jeton):
        if jeton is None:
            return

        else:
            self.grille.capturer_jeton(jeton,self.ratelier)

            if self.ratelier.est_complet():
                if self.ratelier.triplette() :
                    self.nb_points += 2
                    print(self.nb_points)

                else:
                    print(self.nb_points)
                    self.nb_points=0
                    print(self.nb_points)
                    self.ratelier = Ratelier()

            if self.ratelier.triplette() and not self.ratelier.est_complet():
                self.nb_points+=1
                print(self.nb_points)

def enregistrer(fichier: str, grille, ratelier: Ratelier, multijoueur: bool, score: dict[str, int]):
    if not "sauvegardes/" in fichier:
        fichier = f"sauvegardes/{fichier}"

    with open(fichier, "w") as file:
        file.write("===== Grille =====\n")
        grille_str = '{'
        for ligne in grille:
            for case in ligne:
                grille_str += f"({case.x}, {case.y}): {case.jeton}, "
        file.write(f"{grille_str}{'}'}\n")

        file.write("===== Ratelier =====\n")
        ratelier_str = ''
        for jeton in ratelier.jetons:
            ratelier_str += f"{jeton} "
        file.write(f"{ratelier_str if ratelier_str else None }\n")

        file.write("===== Scores =====\n")
        file.write(f"{multijoueur = }\n")
        file.write(f"{score}\n")







