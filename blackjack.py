from random import sample


def paquet():
    """La fonction créé un paquet standard de 52 cartes
    sous la forme d'une liste de tuples"""

    cartes = []
    for couleur_carte in range(4):
        for valeur_carte in range(13):
            cartes.append((valeur_carte, couleur_carte))
    return cartes


def valeur_cartes(carte):
    """Cette fonction renvoie la valeur d'une carte"""

    if carte[0] == 1:  # L'as vaut 1 ou 11, au choix
        reponse = 0
        while reponse != 1 or reponse != 11:
            reponse = int(input("Vous venez de piocher un as, voulez-vous qu'il valle 1 ou 11? "))
        return reponse

    if carte[0] >= 11:  # Valet, Dame et Roi vallent tous 10
        return 10

    return carte[0]  # On renvoit la valeur de la carte.


def init_pioche(n):
    """Initialise la pioche en mélangeant les paquet de cartes"""

    pioche = []
    for i in range(n):
        pioche.extend(sample(paquet(), k=52))
    return pioche


def pioche_carte(pioche, *args):
    """Fonction qui permet de piocher une carte, il y a
    un argument optionel au cas où on veuille plusieurs
    cartes en même temps"""

    if len(args) > 0:
        n = args[0]
    else:
        n = 1

    cartes_pioches = []
    for i in range(n):
        cartes_pioches.append(pioche[0])
        pioche.pop(0)
