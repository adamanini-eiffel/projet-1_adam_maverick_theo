class Joueur :

    def __init__(self, pseudo):

        self.score = 0

        self.pseudo = pseudo

    def ajouter_points(self,points):

        self.score += points
