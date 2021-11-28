#!/bin/env python3
from random import sample

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


class Joueur:
    valeurs = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "V", "D", "R")
    couleurs = list("♠♣♥♦")

    def __init__(self, nom, score):
        self.nom = nom
        self.score = score
        self.cartes = []

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += " " + self.valeurs[carte[0] - 1] + self.couleurs[carte[1]]
        return f"{self.nom} :{main} => {self.score}"

    def pioche_carte(self, nb_cartes = 1):
        """ Permet au joueur de piocher une ou plusieurs cartes. """
        for _ in range(nb_cartes):
            self.cartes.append(pioche[0])
            self.score += valeur_carte(self.cartes[-1])
            pioche.pop(0)


def paquet():
    """ Créé un paquet standard de 52 cartes sous la forme d'une liste de tuples. """
    cartes = []
    for couleur in range(4):
        for valeur in range(13):
            cartes.append((valeur, couleur))
    return cartes


def valeur_carte(carte):
    """ Renvoie la valeur d'une carte. """
    if carte[0] == 1:  # L'as vaut 1 ou 11, au choix
        reponse = 0
        while reponse != 1 or reponse != 11:
            reponse = int(input("Vous venez de piocher un as, voulez-vous qu'il vaille 1 ou 11? "))
        return reponse

    if carte[0] >= 11:  # Valet, Dame et Roi valent tous 10
        return 10

    return carte[0]  # renvoie la valeur de la carte


def premier_tour():
    """ Effectue le premier tour et fait piocher les deux premières cartes
    à chaque joueur. Potentiellement une fonction temporaire. """

    for joueur in liste_joueurs:
        joueur.pioche_carte(2)
        print(joueur)


pioche = init_pioche(2)
nb_joueurs = int(input("Entrez le nombre de joueurs : "))
liste_joueurs = init_joueurs(nb_joueurs)

premier_tour()
