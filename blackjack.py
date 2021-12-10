#!/bin/env python3
from random import sample, randint
from copy import deepcopy

MISE_MIN = 10
MISE_MAX = 1000
NB_PAQUETS = 2


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
    def __init__(self, nom, argent):
        self.nom = nom
        self.cartes = []
        self.argent = argent
        self.mise = 0
        self.blackjack = False
        self.assurance = False
        self.nb_splits = 0
        self.split = False
        self.clone = None

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += f" {carte}"
        return f"{self.nom} :{main} => {self.score()} | argent : {self.argent} | mise : {self.mise}"

    def pioche_carte(self, nb_cartes = 1):
        """ Permet au joueur de piocher une ou plusieurs cartes. """
        for _ in range(nb_cartes):
            self.cartes.append(pioche.pop(0))
            verifie_memoire(self.cartes[-1])

    def double(self):
        """ pioche une carte et double la mise du joueur """
        self.pioche_carte()
        self.mise *= 2

    def possede_paire(self):
        """ Regarde si un joueur possede une paire de cartes """
        cartes_valeurs = []
        for carte in self.cartes:
            cartes_valeurs.append(carte.valeur)

        cartes_valeurs.sort()
        for i in range(len(cartes_valeurs) - 1):
            if cartes_valeurs[i] == cartes_valeurs[i + 1]:
                return True
        return False

    def score(self):
        """ Calcule le score de la main du joueur. """
        scores_possibles = [0]

        def incremente(liste, val):
            """ Ajoute la valeur de la carte à tous les scores possibles """
            for i in range(len(liste)):
                liste[i] += val

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
    def __init__(self, argent, niveau):
        super().__init__("Croupier", argent)
        self.memoire_cartes = []
        self.niveau = niveau

    def __str__(self):
        main = ""
        for carte in self.cartes:
            main += f" {carte}"
        return f"{self.nom} :{main} => {self.score()} | argent : {self.argent}"

    def regarde_cartes(self):
        """ Garde en mémoire les dernières cartes jouées """
        carte_table = []
        for j in liste_joueurs:
            carte_table.extend(j.cartes)
        carte_table.extend(self.cartes)

        self.memoire_cartes.append(carte_table)
        if len(self.memoire_cartes) > self.niveau:
            self.memoire_cartes.pop(0)

    def pioche_intelligente(self):
        """ Détermine si le Croupier doit piocher une carte ou non """

        def calcule_gains(score_croupier):
            """ Calcule les gains du Croupier suivant un score donné """
            rv_gains = 0
            for j in liste_joueurs:
                if j.blackjack is True:
                    rv_gains -= round(j.mise * 1.5)

                elif j.score() > score_croupier:
                    rv_gains -= j.mise

                elif j.score () < score_croupier:
                    rv_gains += j.mise

            return rv_gains

        def valeur_carte(carte):
            """ renvoie la valeur d'une carte """
            return min(carte, 10)

        def esperence_gains(score, possede_as, recurence = False, carte_piochee = -1):
            """ calcule les gains moyens possibles de gagner en piochant une carte """
            total_cartes = 52 * NB_PAQUETS
            cartes_possibles = [4 * NB_PAQUETS for i in range(13)]

            for tour, cartes_tour in enumerate(self.memoire_cartes):
                for carte in cartes_tour:
                    cartes_possibles[carte.valeur - 1] -= 1

            if carte_piochee != -1:
                cartes_possibles[carte_piochee] -= 1

            rv_esperence_gains = 0
            for carte, nombre in enumerate(cartes_possibles):
                score_carte = valeur_carte(carte + 1)
                # On pioche un as qui vaut 11 et score + as <= 21
                if score_carte == 1 and score + 11 <= 21:
                    gains = calcule_gains(score + 11)

                # Le score avec la nouvelle carte ne dépasse pas 21 (as = 1)
                elif score + score_carte < 21:
                    gains = calcule_gains(score + score_carte)

                # Score > 21 pour la première fois et on a au moins un as qui vaut 11
                elif possede_as and recurence is False:
                    prochain_score = score + score_carte - 10
                    gains = esperence_gains(prochain_score, False, True, carte)

                # Score > 21 et on peut rien y faire
                else:
                    gains = 0
                rv_esperence_gains += gains * (nombre / total_cartes)
            return rv_esperence_gains

        def raisonnement_esperence():
            while True:
                if (self.score() == 0 and len(self.cartes) > 0) or self.score() == 21:
                    return

                possede_as = False
                score_sans_as = 0
                for carte in self.cartes:
                    if carte.score() == 1:
                        possede_as = True
                    else:
                        score_sans_as += carte.score()
                if score_sans_as > 11:
                    possede_as = False

                if esperence_gains(self.score(), possede_as) >= calcule_gains(self.score()):
                    self.pioche_carte()
                else:
                    return

        if self.niveau == 0:
            while self.score() < 17:
                self.pioche_carte()
            if self.score() in [17, 18] and randint(0, 2) == 0:
                self.pioche_carte()

        elif self.niveau >= 1:
            raisonnement_esperence()

        else:  # Niveau négatif = mode triche, parce que pourquoi pas
            while self.score() + pioche[0].valeur <= 21:
                self.pioche_carte()


def init_pioche():
    """ Initialise la pioche en mélangeant les paquets de cartes. """

    def paquet():
        """ Créé un paquet standard de 52 cartes sous la forme d'une liste de tuples. """
        cartes = []
        for couleur in range(4):
            for valeur in range(1, 14):
                cartes.append(Carte(valeur, couleur))
        return cartes

    rv_pioche = []
    for _ in range(NB_PAQUETS):
        rv_pioche.extend(sample(paquet(), k=52))
    return rv_pioche


def init_joueurs(nombre, argent):
    """ Créé les différentes instances des joueurs. """
    rv_liste_joueurs = []
    for i in range(nombre):
        nom = str(input(f"Entrez le nom du joueur #{i+1} : "))
        rv_liste_joueurs.append(Joueur(nom, argent))
    return rv_liste_joueurs


def premier_tour():
    """ Demande la mise et fait piocher les deux premières cartes à chaque joueur. """

    def creer_split(id_joueur, j):  # FIXME: Rendre la gestion des joueurs temporaires propre
        """ créé les objest joueurs temporaires en cas de splits """
        while True:
            reponse = input("Vous avez une paire, voulez-vous faire un split? (oui/non) ")
            if reponse == "oui":
                # Créer le joueur temporaire:
                # print("uuu")
                if j.split is True:
                    j.clone.nb_splits += 1
                else:
                    j.nb_splits += 1

                j_split = deepcopy(j)
                j_split.clone = j
                liste_joueurs.insert(id_joueur + 1, j_split)
                j_split.nom = f"{j.nom}_split{j_split.clone.nb_splits}"
                j_split.split = True

                # Remplacer une des carte de la paire par une autre carte
                j.cartes.pop(1)
                j.pioche_carte()
                print(j)
                # Reproposer un split dans le cas où on repioche une paire
                if j.split is True:
                    if j.clone.nb_splits <= 1 and j.possede_paire():
                        # print("prout 1")
                        creer_split(id_joueur, j)

                else:
                    if j.nb_splits <= 1 and j.possede_paire():
                        # print("prout 2")
                        creer_split(id_joueur, j)

                # Remplacer une des carte de la paire par une autre carte
                j_split.cartes.pop(0)
                j_split.pioche_carte()
                print(j_split)
                # Reproposer un split dans le cas où on repioche une paire
                if j_split.possede_paire() and j_split.clone.nb_splits <= 1:
                    # print("prout 3")
                    creer_split(id_joueur + 1, j_split)
                return

            if reponse == "non":
                return

    def demande_mise(j, rv_joueurs_partis):
        """ demande joueurs la mise et leur propose de quitter la table """
        rv_joueurs_partis = []
        while True:
            print(f"{j.nom}: misez de l'argent (entre {MISE_MIN}€ et {MISE_MAX}€)")
            mise = int(input(f"vous avez {j.argent}€ (misez 0 pour quitter la table) : "))
            if MISE_MIN <= mise <= MISE_MAX:
                j.mise = mise
                return rv_joueurs_partis

            if mise == 0:
                print(f"{j.nom} a quitté la table.")
                joueurs_partis.append(j)
                return rv_joueurs_partis


    def demande_assurance(j):
        """ Demande aux joueurs si il veulent une assurance """
        while True:
            reponse = input("Le croupier à un as, miser une assurance? (oui/non) ")
            if reponse == "oui":
                j.assurance = True
                return
            if reponse == "non":
                j.assurance = False
                return

    # On demande la mise et propose au joueur de quitter la table:
    joueurs_partis = []
    for id_joueur, j in enumerate(liste_joueurs):
        if j.split is False:
            demande_mise(j, joueurs_partis)

            j.pioche_carte(2)
            print(j)

            # Le joueur a un blackjack:
            if j.score() == 21:
                print("Vous avez gagné!!")
                j.blackjack = True

            # Le croupier a un blackjack et on propose une assurance au joueur:
            if croupier.cartes[0].valeur == 1:
                demande_assurance(j)

            # Le croupier a une paire et on propose un split:
            if j.possede_paire():
                creer_split(id_joueur, j)
            print(" ")

    # On retire les joueurs qui ont dessidé de partir
    for j in joueurs_partis:
        liste_joueurs.remove(j)


def tour_joueur(j):
    """ Effectue le tour de chaque joueur """
    print("-------------")
    print(f"Tour de {j.nom} :\n{j}")
    print(" • Liste des actions:")
    print(" • pioche: pioche une carte")
    print(" • rester: passe au joueur suivant")
    print(" • double: pioche une carte, double la mise et passe au joueur suivant")
    print(" -> (seulement si le score du joueur est 9, 10 ou 11)")

    while True:
        reponse = input("Quelle est votre action? ")

        if reponse == "rester":
            return

        if reponse == "pioche":
            j.pioche_carte()
            print(j)
            if j.score() == 21:
                print("Vous avez gagné!!")
                return
            if j.score() == 0:
                print("Vous avez perdu!!")
                return

        elif reponse == "double" and 9 <= j.score() <= 11:
            j.double()
            print(j)
            return


def verifie_memoire(carte_verifier):
    """ retire les cartes en mémoire des bots si elle vient d'être pioché """
    # TODO: Faire la manipe pour les bots une fois qu'il existent
    tours_supprimer = []
    for tour, cartes_tour in enumerate(croupier.memoire_cartes):
        if carte_verifier in cartes_tour:
            tours_supprimer.append(tour)

    for tour in tours_supprimer:
        croupier.memoire_cartes.pop(tour)


def regler_mises():
    """ Règle les comptes en fin de partie """

    def payer(j):
        if j.assurance is True:
            if croupier.blackjack is True:
                j.argent += j.mise
            else:
                j.argent -= j.mise / 2

        if j.blackjack is True:
            j.mise = round(j.mise * 1.5)
            j.argent += j.mise
            croupier.argent -= j.mise
            print(f"{j.nom} a gagné {j.mise}€ et a maintenant {j.argent}€")

        elif j.score() > croupier.score():
            j.argent += j.mise
            croupier.argent -= j.mise
            print(f"{j.nom} a gagné {j.mise}€ et a maintenant {j.argent}€")

        elif j.score() < croupier.score():
            j.argent -= j.mise
            croupier.argent += j.mise
            print(f"{j.nom} a perdu {j.mise}€ et a maintenant {j.argent}€")

        else:  # en cas d'égalité
            print(f"Égalité entre {j.nom} et le croupier")

    print("-------------")
    ordre_66 = []
    for j in liste_joueurs:
        if j.split is False:
            payer(j)

        else:
            payer(j.clone)
            ordre_66.append(j)

    for j in ordre_66:
        liste_joueurs.remove(j)


def remplir_pioche():
    """ Récupère les cartes sur la table, les mélangent et les ajoute à la fin de la pioche """
    cartes_recuperees = []
    for j in liste_joueurs:
        cartes_recuperees.extend(j.cartes)
    cartes_recuperees.extend(croupier.cartes)
    pioche.extend(sample(cartes_recuperees, k=len(cartes_recuperees)))


if __name__ == "__main__":
    # Initialisation:
    pioche = init_pioche()
    ## debut test:
    for _ in range(2):
        pioche.insert(1, Carte(4, 0))
    ## fin test
    nb_joueurs = int(input("Entrez le nombre de joueurs : "))
    liste_joueurs = init_joueurs(nb_joueurs, 1000)
    croupier = Croupier(10000, 1)
    croupier.niveau = int(input("entrez le niveau du croupier (un entier) : "))

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
        if croupier.score() == 21:
            croupier.blackjack = True

        croupier.regarde_cartes()
        croupier.pioche_intelligente()
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

        remplir_pioche()
