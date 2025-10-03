class Jeton:
    def __init__(self, color: str, x: int, y: int) -> None:
        self.color = color
        self.x = x
        self.y = y
        
        self.cachee = False
        self.capture = False        

    def retourner(self) -> None:
        self.cachee = True

    def capturer(self) -> None:
        """ Ne devrait être appeller que si self.cachee est True """
        self.capture = True


class Ratelier:
    def __init__(self, taille_max: int = 5) -> None:
        self.taille_max = taille_max
        self.jetons: list = []

    def est_complet(self) -> bool:
        return len(self.jetons) == self.taille_max

    def triplette(self) -> str:
        """
        Si une triplette est formée, renvoie sa couleur,
        None sinon.
        """
        ...

    def est_vide(): ...
    
    def ajouter_jeton(self, jeton: Jeton): ...