#!/bin/env python3
from random import sample

class Carte:
    VALEURS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "V", "D", "R")
    COULEURS = list("♠♣♥♦")

    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def __str__(self):
        return f"{self.VALEURS[self.valeur - 1]}{self.COULEURS[self.couleur]}"

    def score(self):
        """ Renvoie la valeur de la carte. """
        return min(self.valeur, 10)


class Joueur:
    def __init__(self, nom, score = 0):
        self.nom = nom
        self.cartes = []
        self.score_initial = score

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += f" {carte}"
        return f"{self.nom} :{main} => {self.score()}"

    def pioche_carte(self, nb_cartes = 1):
        """ Permet au joueur de piocher une ou plusieurs cartes. """
        for _ in range(nb_cartes):
            self.cartes.append(pioche.pop(0))

    def score(self):
        """ Calcule le score de la main du joueur. """
        scores_possibles = [ self.score_initial ]

        def incremente(tab, val):
            for i in range(len(tab)):
                tab[i] += val

        for carte in self.cartes:
            if carte.score() != 1:
                incremente(scores_possibles, carte.score())
            else:  # la carte est un as, deux possibilités de score: 1 ou 11
                temp_score = scores_possibles.copy()
                incremente(scores_possibles, 1)
                incremente(temp_score, 11)
                scores_possibles.extend(temp_score)

        for score in sorted(scores_possibles, reverse=True):
            if score <= 21:
                return score
        return sorted(scores_possibles)[-1]  # valeur arbitraire en cas de défaite

    def tour_joueur(self):
        print("-------------")
        print(f"Tour de {self.nom} \n{self}")
        if self.score() == 21:
            print("Vous avez gagné!!")

        reponse = ""
        while reponse != "stop":
            reponse = input("Voulez-vous piocher une carte (pioche) ou arrêter de jouer (stop)? : ")

            if reponse == "pioche":
                self.pioche_carte()
                # print(f"Vous avez pioché un {self.cartes[-1]}, votre score est maintenant {self.score()}")
                print(self)
                if self.score() == 21:
                    print("Vous avez gagné!!")
                    return
                if self.score() > 21:
                    print("Vous avez perdu!!")
                    return


def paquet():
    """ Créé un paquet standard de 52 cartes sous la forme d'une liste de tuples. """
    cartes = []
    for couleur in range(4):
        for valeur in range(1, 14):
            cartes.append(Carte(valeur, couleur))
    return cartes


def init_pioche(nb_paquets):
    """ Initialise la pioche en mélangeant les paquets de cartes. """
    rv_pioche = []
    for _ in range(nb_paquets):
        rv_pioche.extend(sample(paquet(), k=52))
    return rv_pioche


def init_joueurs(nombre, score = 0):
    """ Créé les différentes instances des joueurs. """
    rv_liste_joueurs = []
    for i in range(nombre):
        nom = str(input(f"Entrez le nom du joueur #{i+1} : "))
        rv_liste_joueurs.append(Joueur(nom, score))
    return rv_liste_joueurs


def premier_tour():
    """ Effectue le premier tour et fait piocher les deux premières cartes
    à chaque joueur. Potentiellement une fonction temporaire. """

    for joueur in liste_joueurs:
        joueur.pioche_carte(2)
        print(joueur)


def gagnant():
    meilleur_score = 0
    for contender in liste_joueurs:
        if contender.score() > meilleur_score:
            meilleur_score = contender.score()
            meilleur_joueur = contender.nom
    print(f"Le gagnant est {meilleur_joueur} avec un score de {meilleur_score}")


pioche = init_pioche(2)
nb_joueurs = int(input("Entrez le nombre de joueurs : "))
liste_joueurs = init_joueurs(nb_joueurs)
premier_tour()

for joueur in liste_joueurs:
    joueur.tour_joueur()

gagnant()

# test algo
# j = Joueur("test")
# j.cartes = [ Carte(1, 1), Carte(5, 2), Carte(1, 3) ]
# assert j.score() == 17
# print(j)
