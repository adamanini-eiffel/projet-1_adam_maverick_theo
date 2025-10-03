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
        for i, jeton in enumerate(self.jetons):
            count = 0

            for jeton2 in self.jetons[i:]:
                if jeton.couleur == jeton2.couleur:
                    count += 1

            if count == 3:
                return True

        return False
                

    def ajouter_jeton(self, jeton: Jeton) -> None:
        if self.est_complet():
            ...
        
        self.jetons.append(jeton)


class Grille:
    def __init__(self) -> None:
        pass

    def get_voisins(self, jeton: Jeton) -> list:
        """
        Renvoie la liste des voisins d'un jeton si celui si est présent. Liste vide sinon. 
        """
        ...
        
"""
Tests (peut être suppr)


ratelier = Ratelier()
for _ in range(5): ratelier.ajouter_jeton(Jeton("Jaune", 0, 0))
assert ratelier.triplette()

ratelier = Ratelier()
for _ in range(2): ratelier.ajouter_jeton(Jeton("Jaune", 0, 0))
for _ in range(3): ratelier.ajouter_jeton(Jeton("Rouge", 0, 0))
assert ratelier.triplette()

ratelier = Ratelier()
for _ in range(2): ratelier.ajouter_jeton(Jeton("Jaune", 0, 0))
for _ in range(2): ratelier.ajouter_jeton(Jeton("Rouge", 0, 0))
ratelier.ajouter_jeton(Jeton("Vert", 0, 0))
assert ratelier.triplette() == False

ratelier = Ratelier()
for i in Couleurs:
    if not ratelier.est_complet:
        ratelier.ajouter_jeton(Jeton(i), 0, 0)
assert ratelier.triplette() == False

"""