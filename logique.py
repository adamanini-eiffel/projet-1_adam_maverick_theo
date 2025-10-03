import fltk
from jetons import Jeton,Ratelier,Grille


class regle:
    def __init__(self,nbpoints=0) -> None:
        self.nbpoints=nbpoints
        self.ratelier=Ratelier()


    def points(self)-> None:
        if triplette():
            nbpoints+=1
            if self.ratelier.est_complet():
                nbpoints+=1
        else:
            if self.ratelier.est_complet():
                nbpoints=0

    def modifier_ratelier(self):
        if ... :
            voisins=self.grille.get_voisins(jeton)
            for voisin in voisins:
                voisin.Jeton.retourner()
            self.ratelier.ajouter_jeton()
        if self.ratelier.est_complet():
            self.ratelier=Ratelier()



    def change_ratelier(self) ->None:
        pass






