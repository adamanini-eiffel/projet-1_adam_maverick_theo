from jetons import Jeton, Ratelier, Grille



class Regles:
    def __init__(self, nbpoints = 0) -> None:
        self.nbpoints = nbpoints
        self.ratelier = Ratelier()
        self.grille = Grille(8, 10)


    def points(self)-> None:
        if self.ratelier.triplette() :
            self.nbpoints += 1
            if self.ratelier.est_complet():
                self.nbpoints += 1

        elif self.ratelier.est_complet():
            self.ratelier=Ratelier()
            self.nbpoints=0



    def modifier_ratelier(self,jeton):
        if jeton is None:
            return

        if jeton.est_cache:
            self.grille.capturer_jeton(jeton,self.ratelier)


            if self.ratelier.triplette() :
                self.nbpoints += 1
                if self.ratelier.est_complet():
                    self.nbpoints += 1
            print(self.nbpoints)

            if self.ratelier.est_complet():
                print(self.nbpoints)
                self.nbpoints=0
                self.ratelier = Ratelier()








