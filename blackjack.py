#!/bin/env python3
from random import sample

class Carte:
    """ Définie le fonctionnement des cartes """
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
    """ Définie les méthodes et propriétés des joueurs """
    def __init__(self, nom, argent, score = 0):
        self.nom = nom
        self.cartes = []
        self.score_initial = score
        self.argent = argent
        self.mise = 0
        self.blackjack = False

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += f" {carte}"
        return f"{self.nom} :{main} => {self.score()} | argent : {self.argent} | mise : {self.mise}"

    def pioche_carte(self, nb_cartes = 1):
        """ Permet au joueur de piocher une ou plusieurs cartes. """
        for _ in range(nb_cartes):
            self.cartes.append(pioche.pop(0))

    def score(self):
        """ Calcule le score de la main du joueur. """
        scores_possibles = [ self.score_initial ]

        def incremente(tab, val):
            """ Ajoute la valeur de la carte à tous les scores possibles """
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
        return 0 # valeur arbitraire en cas de défaite


class Croupier(Joueur):
    """ Définie le comportement du croupier """
    def __init__(self, argent):
        super().__init__("Croupier", argent)
        self.mise = [0 for _ in range(nb_joueurs)]

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += f" {carte}"
        return f"{self.nom} :{main} => {self.score()} | argent : {self.argent}"



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


def init_joueurs(nombre, argent, score = 0):
    """ Créé les différentes instances des joueurs. """
    rv_liste_joueurs = []
    for i in range(nombre):
        nom = str(input(f"Entrez le nom du joueur #{i+1} : "))
        rv_liste_joueurs.append(Joueur(nom, argent, score))
    return rv_liste_joueurs


def premier_tour():
    """ Demande la mise et fait piocher les deux premières cartes à chaque joueur. """
    joueurs_partis = []
    for id_joueur, j in enumerate(liste_joueurs):
        mise_valide = False
        while not mise_valide:
            print(f"{j.nom}: misez de l'argent (entre 10€ et 1000€)")
            mise = int(input("vous avez {j.argent}€ (misez 0 pour quitter la table) : "))
            if MISE_MIN <= mise <= MISE_MAX:
                mise_valide = True

            elif mise == 0:
                print(f"{j.nom} a quitté la table.")
                joueurs_partis.append(j)
                mise_valide = True

        j.mise = mise
        croupier.mise[id_joueur] = mise
        j.pioche_carte(2)
        print(j)
        print(" ")

        if j.score() == 21:
            print("Vous avez gagné!!")
            j.blackjack = True

    for j in joueurs_partis:
        liste_joueurs.remove(j)


def tour_joueur(j):
    """ Effectue le tour de chaque joueur """
    print("-------------")
    print(f"Tour de {j.nom} :\n{j}")

    reponse = ""
    while reponse != "stop":
        reponse = input("Voulez-vous piocher une carte (pioche) ou arrêter de jouer (stop)? : ")

        if reponse == "pioche":
            j.pioche_carte()
            print(j)
            if j.score() == 21:
                print("Vous avez gagné!!")
                return
            if j.score() == 0:
                print("Vous avez perdu!!")
                return


def regler_mises():
    """ Règle les comptes en fin de partie """
    print("-------------")
    for id_joueur, j in enumerate(liste_joueurs):
        if j.blackjack is True:
            j.argent += round(j.mise * 1.5)
            croupier.argent -= croupier.mise

        elif j.score() > croupier.score():
            j.argent += j.mise
            croupier.argent -= croupier.mise[id_joueur]
            print(f"{j.nom} a gagné {j.mise}€ et a maintenant {j.argent}€")

        elif j.score() < croupier.score():
            j.argent -= j.mise
            croupier.argent += croupier.mise[id_joueur]
            print(f"{j.nom} a perdu {j.mise}€ et a maintenant {j.argent}€")

        else:  # en cas d'égalité
            print(f"Égalité entre {j.nom} et le croupier")


# Initialisation:
MISE_MIN = 10
MISE_MAX = 1000
pioche = init_pioche(2)
nb_joueurs = int(input("Entrez le nombre de joueurs : "))
liste_joueurs = init_joueurs(nb_joueurs, 1000)
croupier = Croupier(10000)

# Boucle principale:
while len(liste_joueurs) > 0 or croupier.argent < MISE_MIN:
    print("___________________________")
    croupier.pioche_carte()
    print(croupier)
    premier_tour()
    for joueur in liste_joueurs:
        if joueur.score() != 21:
            tour_joueur(joueur)

    croupier.pioche_carte()
    print(croupier)
    regler_mises()

    joueurs_perdu = []
    for joueur in liste_joueurs:
        joueur.cartes.clear()
        if joueur.argent < MISE_MIN:
            joueurs_perdu.append(joueur)

    for joueur in joueurs_perdu:
        liste_joueurs.remove(joueur)
    croupier.cartes.clear()

# test algo
# j_test = Joueur("test", 500)
# print(j_test)
# j_test.mise.append(50)
# j_test.deduit_mise()
# j.cartes = [ Carte(1, 1), Carte(5, 2), Carte(1, 3) ]
# assert j.score() == 17
# print(j_test)
