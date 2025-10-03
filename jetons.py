Couleurs: tuple = (
    "Rouge",
    "Jaune",
    "Bleu",
    "Orange",
    "Vert",
    "Gris",
    "Marron"
)

class Jeton:
    def __init__(self, couleur: str, x: int, y: int) -> None:
        self.couleur = couleur
        self.x = x
        self.y = y
        
        self.est_cache = False
        self.est_capture = False        

    def retourner(self) -> None:
        self.est_cache = True

    def capturer(self) -> None:
        """ Ne devrait être appeller que si self.est_cachee est True """
        self.est_capture = True


class Ratelier:
    def __init__(self, taille_max: int = 5) -> None:
        self.taille_max = taille_max
        self.jetons: list = []

    def est_complet(self) -> bool:
        return len(self.jetons) == self.taille_max

    def est_vide(self) -> bool:
        return len(self.jetons) == 0

    def triplette(self) -> bool:
        """
        Renvoie True si une triplette est formée et la retire des jetons du ratelier, False sinon
        """
        ...

    def ajouter_jeton(self, jeton: Jeton):
        if self.est_complet():
            ...
        
        self.jetons.append(jeton.couleur)


class Grille:
    def __init__(self) -> None:
        pass

    def get_voisins(self, jeton: Jeton) -> list:
        """
        Renvoie la liste des voisins d'un jeton si celui si est présent. Liste vide sinon. 
        """
        ...
        