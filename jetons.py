from random import random, choice
from math import sqrt
from typing import Tuple, Optional, Dict, List, Set

Couleurs: tuple = ("red", "yellow", "blue", "orange", "green", "gray", "brown")


# utilitaires

def distance(a,b) -> float:
    """
    Renvoie la distance entre deux jetons
    """
    if a is None or b is None:
        return -1
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def _1Dto2DCoords(coord: int, largeur: int = 8, hauteur: int = 10) -> Tuple[int, int]:
    """
    Renvoie un couple (x, y) correspondant aux coordonées d'un point dans une grille de l * h.
    coord correspond à la coordonée sur une table d'une dimension (utilisé dans la classe Grille).
    Le tuple (-1, -1) est renvoyé si la coordonée n'appartient pas à la table (coord > l*h).
    Fonction réciproque de _2Dto1DCoords.
    """
    if (coord < 0 or coord >= largeur * hauteur):
        return (-1, -1)

    x = coord % largeur
    y = coord // largeur
    return (x, y)


def _2Dto1DCoords(x: int, y: int, largeur: int = 8, hauteur: int = 10) -> int:
    """
    Renvoie la coordonée (une dimention) correspondant au point de coordonée (x, y) dans une table l * h.
    la coordonée -1 est renvoyé si la coordonée n'appartient pas à la table.
    Fonction réciproque de _1Dto2DCoords.
    """
    if (x < 0 or y < 0 or x >= largeur or y >= hauteur):
        return -1

    return y * largeur + x


def _2Dto1DCoordsTuple(coords: tuple[int, int], largeur: int = 8, hauteur: int = 10) -> int:
    """
    Pareil que _2Dto1DCoords, coords est un tuple de deux entiers qui représente une coordonée sur la table.
    """
    return _2Dto1DCoords(coords[0], coords[1], largeur, hauteur)


# classes

class Jeton:
    def __init__(self, couleur: str, x: int, y: int) -> None:
        self.couleur = couleur
        self.x = x
        self.y = y
        self.est_cache = True
        self.est_capture = False

    def get_couleur(self) -> str:
        return self.couleur

    def retourner(self) -> None:
        self.est_cache = False

    def capturer(self) -> None:
        """Ne devrait être appelé que si self.est_cache est True"""
        self.est_capture = True

    def __str__(self) -> str:
        return self.couleur


class JetonNul:
    """
    Représente un espace vide (capturé) dans la grille, pas un espace neutralisé (cases None / noires).
    Pas besoin de stoker des variables autres que la couleure. Une seule instance peut être dupliqué
    au besoin (celle juste en dessous)
    """

    def __init__(self) -> None:
        self.couleur = "BLANC"

    def __str__(self) -> str:
        return self.couleur


# jeton constant à dupliquer
JETON_NUL = JetonNul()


class Ratelier:
    def __init__(self, taille_max: int = 5) -> None:
        self.taille_max = taille_max
        self.jetons: List[Jeton] = []

    def est_complet(self) -> bool:
        return len(self.jetons) == self.taille_max

    def est_vide(self) -> bool:
        return len(self.jetons) == 0

    def triplette(self) -> bool:
        """
        Renvoie True si une triplette est formée et la retire des jetons du râtelier, False sinon.
        Devrait être appellé à chaque mise à jour du râtelier.
        """
        occurences_couleurs: dict = {}
        for jeton in self.jetons:
            if (not jeton.couleur in occurences_couleurs):
                occurences_couleurs[jeton.couleur] = 0

            occurences_couleurs[jeton.couleur] += 1

        for couleur, occurences in occurences_couleurs.items():
            if occurences < 3:
                continue

            enlevee = 0
            for j in self.jetons[:]:  # copie pour éviter d'itérer sur une liste modifiée
                if j.couleur == couleur and enlevee < 3:
                    self.jetons.remove(j)
                    enlevee += 1

            return True
        return False

    def ajouter_jeton(self, jeton: Jeton) -> None:
        if not self.est_complet():
            self.jetons.append(jeton)

# temporaire: valeurs de teux_neutralisé qui permettent d'éviter les approximations des floatants:
# 0.125 -> 3
# 0.714999973773956298828125 ( ~ 0.715)  -> 2



class Grille:
    def __init__(self, largeur: int, hauteur: int, taux_neutralise: float = 0.125) -> None:
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille: List[Optional[Jeton]] = self.generer_grille(taux_neutralise, essais_max=100)

    """def generer_grille(self, taux_neutralise: float, essais_max: int = 100) -> List[Optional[Jeton]]:
        attempts = 0
        grille = []
        while attempts < essais_max:
            grille = [None] * (self.largeur * self.hauteur)

            for cellule in range(len(grille)):
                if random() <= taux_neutralise:
                    continue

                x, y = _1Dto2DCoords(cellule, self.largeur, self.hauteur)
                grille[cellule] = Jeton(couleur=choice(Couleurs), x=x, y=y)

            grille = self.corrige_enclaves_simples(grille)

            # on arrête là et on relance
            if not self.trouver_enclave_large(grille):
                return grille
            attempts += 1

        print(f"Impossible de générer une grille sans enclave large après {essais_max} tentatives")
        return grille"""

    def generer_grille(self, taux_neutralise: float, essais_max: int = 100) -> List[Optional[Jeton]]:
        grille: List[Optional[Jeton]] = []
        max_neutralise = int(self.largeur * self.hauteur * taux_neutralise)
        occurences_couleurs: int = (self.largeur * self.hauteur - max_neutralise) / 3 * len(Couleurs)
        couleurs: Dict[str: int] = {couleur : occurences_couleurs for couleur in Couleurs}
        
        essais = 0
        while essais < essais_max:
            grille = [None] * (self.largeur * self.hauteur)

            for cellule in range(len(grille)):
                if random() <= taux_neutralise:
                    continue

                x, y = _1Dto2DCoords(cellule, self.largeur, self.hauteur)
                couleur_jeton = ''
                while (couleur_jeton not in Couleurs or couleurs[couleur_jeton] == 0):
                    couleur_jeton = choice(Couleurs)

                couleurs[couleur_jeton] -= 1
                grille[cellule] = Jeton(couleur_jeton, x, y)


            grille = self.corrige_enclaves_simples(grille)

            # on arrête là et on relance
            if not self.trouver_enclave_large(grille):
                return grille
            essais += 1

        print(f"Impossible de générer une grille sans enclave large après {essais_max} tentatives")
        return grille



    def trouver_enclave_simple(self, grille: List[Optional[Jeton]]) -> Tuple[Tuple[int, int], ...]:
        """
        Renvoie les coordonnées des enclaves simples si elles existent, Tuple vide sinon.
        Une enclave simple est un jeton isolé de tout autre jeton par quatre cases neutralisées
        """
        enclaves = []

        for jeton in grille:
            if not isinstance(jeton, Jeton):
                continue
            voisins = self.get_voisins(jeton, grille)
            if voisins == [None] * 4:
                enclaves.append((jeton.x, jeton.y))

        return tuple(enclaves)

    def corrige_enclaves_simples(self, grille: List[Optional[Jeton]]) -> List[Optional[Jeton]]:
        enclaves: Tuple[Tuple[int, int], ...] = self.trouver_enclave_simple(grille)
        if not enclaves:
            return grille

        print(f"correction d'enclaves simples: {enclaves}")
        for jetons_coords in enclaves:
            index = _2Dto1DCoordsTuple(jetons_coords, self.largeur, self.hauteur)
            jeton = grille[index]

            if not isinstance(jeton, Jeton):
                continue

            voisins_coords = self.get_voisins_coords(jeton)
            if voisins_coords:
                remplace_x, remplace_y = choice(voisins_coords)
                index_remplace = _2Dto1DCoords(remplace_x, remplace_y, self.hauteur, self.largeur)
                grille[index_remplace] = Jeton(choice(Couleurs), remplace_x, remplace_y)

        return grille

    def get_voisins_coords(self, jeton: Jeton) -> List[Tuple[int, int]]:
        """Retourne les coordonnées des voisins d'un jeton"""
        x, y = jeton.x, jeton.y
        voisins = []

        if x > 0:
            voisins.append((x - 1, y))
        if x < self.largeur - 1:
            voisins.append((x + 1, y))
        if y > 0:
            voisins.append((x, y - 1))
        if y < self.hauteur - 1:
            voisins.append((x, y + 1))

        return voisins

    def trouver_enclave_large(self, grille: List[Optional[Jeton]]) -> bool:
        """
        Renvoie True si une enclave large a été trouvée, False sinon.
        """
        # Trouver tous les jetons non neutralisés
        jetons = [j for j in grille if isinstance(j, Jeton)]

        if not jetons:
            return False

        # Vérifier la connectivité entre tous les jetons
        visited: Set[Jeton] = set()
        stack = [jetons[0]]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            voisins = self.get_voisins(current, grille)
            for voisin in voisins:
                if isinstance(voisin, Jeton) and voisin not in visited:
                    stack.append(voisin)

        # Si nous n'avons pas visité tous les jetons, il y a une enclave
        return len(visited) != len(jetons)

    def get_voisins(self, jeton: Jeton, grille: List[Optional[Jeton]] = None) -> List[Optional[Jeton]]:
        """Retourne les jetons voisins (jeton ou none)"""
        if (grille is None):
            grille = self.grille

        voisins_coords = self.get_voisins_coords(jeton)
        voisins = []

        for x, y in voisins_coords:
            index = _2Dto1DCoords(x, y, self.largeur, self.hauteur)
            voisins.append(grille[index])

        return voisins

    def capturer_jeton(self, jeton: Jeton, ratelier: Ratelier) -> None:
        """
        Enleve un jeton et retourne tout les voisins jetons non-retournés
        """
        voisins = self.get_voisins(jeton)
        for voisin in voisins:
            if isinstance(voisin, Jeton):
                voisin.retourner()

        ratelier.ajouter_jeton(jeton)
        self.grille[_2Dto1DCoords(jeton.x, jeton.y, self.largeur, self.hauteur)] = JETON_NUL

    def __str__(self) -> str:
        # affiche la grille en un tableau
        # nb: les cases neutralisés sont notés None.
        graduation = '\t'
        for i in range(self.largeur):
            graduation += f'{i + 1}\t\t\t'

        res = f'{graduation}\n'
        for i in range(self.hauteur):
            res += f'{i + 1}|'
            for j in range(self.largeur):
                res += f'\t{self.grille[_2Dto1DCoords(i, j, self.largeur, self.hauteur)]}\t|'

            res += '\n'

        return res



if __name__ == "__main__":
    from random import choice

    r = Ratelier()
    g = Grille(10, 10, 0.40)

    choix = choice(g.grille)
    while not isinstance(choix, Jeton):
        choix = choice(g.grille)

    print(f"capture du jeton {choix.x + 1, choix.y + 1}")
    g.capturer_jeton(choix, r)
    
    ligne = ''
    for i, j in enumerate(g.grille):
        if i % g.largeur == 0:
            print(ligne)
            ligne = ''

        ligne += f'{j}\t'

    print(g.trouver_enclave_simple(g.grille))