"""
bugs (par ordre de priorité).

Il y a une probabilité que les jetons initiaux disparaissent tous, à éviter.

Pour une probabilité trop grosse, le programme finira par trouver une solution qui contourne la fonction de
détection d'enclave (tous les jetons sont collés dans un endroit). Ne devrait normalement
pas arriver sauf si la proba est vraiment forte.


"""

from random import random, choice
from math import sqrt
from typing import Tuple, Optional, List, Set

Couleurs: tuple = ("red", "yellow", "blue", "orange", "green", "gray", "brown")


# ------------------------- utilitaires -------------------------

def distance(a,b) -> float:
    """
    Renvoie la distance entre deux jetons
    """
    if a is None or b is None:
        return -1
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def _1Dto2DCoords(coord: int, largeur: int = 8, hauteur: int = 10) -> Tuple[int, int]:
    """
    Renvoie un couple (x, y) correspondant aux coordonnées d'un point dans une grille de l * h.
    coord correspond à la coordonnée sur une table d'une dimension (utilisé dans la classe Grille).
    Le tuple (-1, -1) est renvoyé si la coordonnée n'appartient pas à la table (coord > l*h).
    Fonction réciproque de _2Dto1DCoords.
    """
    if coord < 0 or coord >= largeur * hauteur:
        return -1, -1

    x = coord % largeur
    y = coord // largeur
    return x, y


def _2Dto1DCoords(x: int, y: int, largeur: int = 8, hauteur: int = 10) -> int:
    """
    Renvoie la coordonnée (une dimension) correspondant au point de coordonnée (x, y) dans une table l * h.
    la coordonnée -1 est renvoyé si la coordonnée n'appartient pas à la table.
    Fonction réciproque de _1Dto2DCoords.
    """
    if x < 0 or y < 0 or x >= largeur or y >= hauteur:
        return -1

    return y * largeur + x


def _2Dto1DCoordsTuple(coords: tuple[int, int], largeur: int = 8, hauteur: int = 10) -> int:
    """
    Pareil que _2Dto1DCoords, coords est un tuple de deux entiers qui représente une coordonnée sur la table.
    """
    return _2Dto1DCoords(coords[0], coords[1], largeur, hauteur)


def optimise_probabilite(p: float, cases: int, max_deviation: float = -1):
    """
    Prends une probabilité initiale p correspondant au nombre de cases neutralisées, cases le nombre de cases totales
    (neutralisées ou non) et une déviation maximale de la probabilité initiale. Si la déviation initiale n'est pas donnée,
    on s'assure juste que la probabilité reste entre 0 et 1.
    Renvoie la probabilité la plus proche de p qui permet d'obtenir un nombre d'apparitions par couleur
    qui soit un multiple de 3. -1 si rien n'est trouvé ou si la probabilité sort de la déviation maximale.
    """
    if max_deviation == -1:
        max_deviation = min(1 - p, p)

    c = len(Couleurs)
    k_ideal = ((1 - p) * cases) / (3 * c)         # nombre de cases idéal pour que la prédiction soit égale à p (pas un int)
    k_optimal = round(k_ideal)
    new_p = 1 - ((3 * k_optimal * c) / cases)     # on en déduit la nouvelle probabilité

    return new_p if abs(new_p - p) < max_deviation else -1


# ------------------------- classes -------------------------

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
    Pas besoin de stoker des variables autres que la couleur. Une seule instance peut être dupliquée
    au besoin (celle juste en dessous).
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
        occurrences_couleurs: dict = {}
        for jeton in self.jetons:
            if not jeton.couleur in occurrences_couleurs:
                occurrences_couleurs[jeton.couleur] = 0

            occurrences_couleurs[jeton.couleur] += 1

        for couleur, occurrences in occurrences_couleurs.items():
            if occurrences < 3:
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


class Grille:
    def __init__(self, largeur: int, hauteur: int, taux_neutralise: float = 0.28, essais_max=1000) -> None:
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille: List[Optional[Jeton]] = self.generer_grille(taux_neutralise, essais_max)


    def generer_grille(self, taux_neutralise: float, essais_max: int = 100) -> List[Optional[Jeton]]:
        grille: List[Optional[Jeton]] = [None] * (self.largeur * self.hauteur)
        attempts = 0

        # Optimiser le taux
        taux_optimise = optimise_probabilite(taux_neutralise, self.largeur * self.hauteur)
        if taux_optimise == -1:
            taux_optimise = taux_neutralise
            print("impossible d'optimiser la probabilité")

        taux_optimise = round(taux_optimise, 5)
        cases_valides = int(self.largeur * self.hauteur * (1 - taux_optimise))
        occurrences_par_couleur = {couleur: cases_valides // len(Couleurs) for couleur in Couleurs}

        # Ajuster pour que le total soit correct
        total_jetons = sum(occurrences_par_couleur.values())
        difference = cases_valides - total_jetons
        if difference > 0:
            # Distribuer les jetons restants
            couleurs = list(Couleurs)
            for i in range(difference):
                occurrences_par_couleur[couleurs[i % len(couleurs)]] += 1

        print(f"taux trouvé: {taux_optimise} (diff: {round(abs(taux_neutralise - taux_optimise), 5)})")
        print(f"{occurrences_par_couleur = }")
        print(f"{cases_valides = }, cases_totales = {self.largeur * self.hauteur}, diff = {self.largeur * self.hauteur - cases_valides}")

        if cases_valides == 0:
            print("la probabilité qu'une case soit neutralisée est probablement beaucoup trop haute")
            return grille

        while attempts < essais_max:
            occurrences_restantes = occurrences_par_couleur.copy()

            for cellule in range(len(grille)):
                if random() <= taux_optimise:
                    continue

                x, y = _1Dto2DCoords(cellule, self.largeur, self.hauteur)

                # Choisir une couleur avec des occurrences restantes
                couleurs_disponibles = [c for c, count in occurrences_restantes.items() if count > 0]
                if not couleurs_disponibles:
                    break

                couleur = choice(couleurs_disponibles)
                occurrences_restantes[couleur] -= 1
                grille[cellule] = Jeton(couleur, x, y)

            grille = self.corrige_enclaves_simples(grille)

            if not self.trouver_enclave_large(grille):
                return grille

            attempts += 1

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
                index_remplace = _2Dto1DCoords(remplace_x, remplace_y, self.largeur, self.hauteur)
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
        if grille is None:
            grille = self.grille

        voisins_coords = self.get_voisins_coords(jeton)
        voisins = []

        for x, y in voisins_coords:
            index = _2Dto1DCoords(x, y, self.largeur, self.hauteur)
            voisins.append(grille[index])

        return voisins

    def capturer_jeton(self, jeton: Jeton, ratelier: Ratelier) -> None:
        """
        Enlève un jeton et retourne tous les voisins jetons non-retournés
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
            graduation += f'{i + 1}\t\t'

        res = f'{graduation}\n'
        for i in range(self.hauteur):
            res += f'{i + 1}|'
            for j in range(self.largeur):
                res += f'\t{self.grille[_2Dto1DCoords(j, i, self.largeur, self.hauteur)]}\t\t|'

            res += '\n'

        return res


if __name__ == "__main__":

    r = Ratelier()
    g = Grille(8, 10, 0.5, 1000)

    choix = choice(g.grille)
    while not isinstance(choix, Jeton):
        choix = choice(g.grille)

    print(f"capture du jeton {choix.x + 1, choix.y + 1}")
    g.capturer_jeton(choix, r)
    print(g)
