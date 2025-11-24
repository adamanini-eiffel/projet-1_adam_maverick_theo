from jetons import  Ratelier, Grille



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

        else:
            self.grille.capturer_jeton(jeton,self.ratelier)

            if self.ratelier.est_complet():
                if self.ratelier.triplette() :
                    self.nbpoints += 2
                    print(self.nbpoints)

                else:
                    print(self.nbpoints)
                    self.nbpoints=0
                    print(self.nbpoints)
                    self.ratelier = Ratelier()

            if self.ratelier.triplette() and not self.ratelier.est_complet():
                self.nbpoints+=1
                print(self.nbpoints)

    def enregistrer(self):
        pass



    def load(self):
        pass









