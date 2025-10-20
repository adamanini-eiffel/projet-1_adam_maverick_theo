from random import random, choice
from math import sqrt
from typing import Tuple, Optional, List, Set

Couleurs: tuple = ("Rouge", "Jaune", "Bleu", "Orange", "Vert", "Gris", "Marron")


class Jeton:
    def __init__(self, couleur: str, x: int, y: int) -> None:
        self.couleur = couleur
        self.x = x
        self.y = y
        self.est_cache = True
        self.est_capture = False

    def retourner(self) -> None:
        self.est_cache = False

    def capturer(self) -> None:
        """Ne devrait être appelé que si self.est_cache est True"""
        self.est_capture = True

    def __str__(self):
        return self.couleur


def distance(a: Jeton, b: Jeton) -> float:
    """
    Renvoie la distance entre deux jetons
    """
    if a is None or b is None:
        return -1
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


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
        Renvoie True si une triplette est formée et la retire des jetons du râtelier, False sinon
        """
        for i, jeton in enumerate(self.jetons):
            count = 0
            for jeton2 in self.jetons[i:]:
                if jeton.couleur == jeton2.couleur:
                    count += 1

            if count == 3:
                # Remove the triplette
                to_remove = []
                for j in self.jetons[:]:
                    if j.couleur == jeton.couleur and len(to_remove) < 3:
                        to_remove.append(j)

                for j in to_remove:
                    self.jetons.remove(j)
                return True
        return False

    def ajouter_jeton(self, jeton: Jeton) -> None:
        if not self.est_complet():
            self.jetons.append(jeton)


class Grille:
    def __init__(self, largeur: int, hauteur: int, taux_neutralise: float = 0.1) -> None:
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille: List[Optional[Jeton]] = self.generer_grille(taux_neutralise)

    def generer_grille(self, taux_neutralise: float) -> List[Optional[Jeton]]:
        attempts = 0
        while attempts < 100:
            grille = [None] * (self.largeur * self.hauteur)

            for cellule in range(len(grille)):
                if random() <= taux_neutralise:
                    continue
                grille[cellule] = Jeton(
                    couleur=choice(Couleurs),
                    x=(cellule % self.largeur),
                    y=(cellule // self.largeur)
                )

            grille = self.corrige_enclaves_simples(grille)

            # on arrête là et on relance
            if not self.trouver_enclave_large(grille):
                return grille
            attempts += 1

        print("Impossible de générer une grille sans enclave large après 100 tentatives")
        return grille

    def trouver_enclave_simple(self, grille: List[Optional[Jeton]]) -> Tuple[Tuple[int, int], ...]:
        """
        Renvoie les coordonnées des enclaves simples si elles existent, Tuple vide sinon.
        Une enclave simple est un jeton isolé de tout autre jeton par quatre cases neutralisées
        """
        enclaves = []

        for jeton in grille:
            if jeton is None:
                continue
            voisins = self.get_voisins(grille, jeton)
            if voisins == [None] * 4:
                enclaves.append((jeton.x, jeton.y))

        return tuple(enclaves)

    def corrige_enclaves_simples(self, grille: List[Optional[Jeton]]) -> List[Optional[Jeton]]:
        enclaves: Tuple[Tuple[int, int], ...] = self.trouver_enclave_simple(grille)
        if not enclaves:
            return grille

        print(f"correction d'enclaves simples: {enclaves}")
        for jeton_x, jeton_y in enclaves:
            index = jeton_x + self.largeur * jeton_y
            jeton = grille[index]
            if jeton is None:
                continue

            voisins_coords = self.get_voisins_coords(jeton)
            if voisins_coords:
                remplace_x, remplace_y = choice(voisins_coords)
                grille[remplace_x + self.largeur * remplace_y] = Jeton(
                    choice(Couleurs), remplace_x, remplace_y
                )

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

    def get_voisins(self, grille: List[Optional[Jeton]], jeton: Jeton) -> List[Optional[Jeton]]:
        """Retourne les jetons voisins"""
        voisins_coords = self.get_voisins_coords(jeton)
        voisins = []

        for x, y in voisins_coords:
            index = x + self.largeur * y
            voisins.append(grille[index])

        return voisins

    def trouver_enclave_large(self, grille: List[Optional[Jeton]]) -> bool:
        """
        Renvoie True si une enclave large a été trouvée, False sinon.
        """
        # Trouver tous les jetons non neutralisés
        jetons = [j for j in grille if j is not None]

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

            voisins = self.get_voisins(grille, current)
            for voisin in voisins:
                if voisin is not None and voisin not in visited:
                    stack.append(voisin)

        # Si nous n'avons pas visité tous les jetons, il y a une enclave
        return len(visited) != len(jetons)

    def __str__(self) -> str:
        graduation = '\t'
        for i in range(self.largeur):
            graduation += f'{i + 1}\t\t\t'

        res = f'{graduation}\n'
        for i in range(self.hauteur):
            res += f'{i + 1}|'
            for j in range(self.largeur):
                res += f'\t{self.grille[self.largeur * i + j]}\t|'

            res += '\n'

        return res



if __name__ == "__main__":
    g = Grille(8, 10, 0.28)
    print(g)