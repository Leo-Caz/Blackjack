#!/bin/env python3
from random import sample, randint
from copy import deepcopy

MISE_MIN = 10
MISE_MAX = 1000
ARGENT_JOUEUR_DEPART = 2000
ARGENT_CROUPIER_DEPART = 100000


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
        self.assurance = False
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

    def possede_as(self):
        rv_possede_as = False
        score_sans_as = 0
        for carte in self.cartes:
            if carte.score() == 1:
                rv_possede_as = True
            else:
                score_sans_as += carte.score()
        if score_sans_as >= 11:
            rv_possede_as = False
        return rv_possede_as

    def possede_paire(self):
        """ Regarde si un joueur possede une paire de cartes """
        cartes_valeurs = []
        for carte in self.cartes:
            cartes_valeurs.append(carte.score())

        cartes_valeurs.sort()
        for i in range(len(cartes_valeurs) - 1):
            if cartes_valeurs[i] == cartes_valeurs[i + 1]:
                return True
        return False

    def score(self, carte_bonus = []):
        """ Calcule le score de la main du joueur. """
        scores_possibles = [0]

        def incremente(liste, val):
            """ Ajoute la valeur de la carte à tous les scores possibles """
            for i in range(len(liste)):
                liste[i] += val

        for carte in self.cartes + carte_bonus:
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


class Bot(Joueur):
    """ Décris le fonctionnement des bots """
    def __init__(self, nom, argent, niveau, opti_mise):
        super().__init__(nom, argent)
        self.mise = 100
        self.memoire_cartes = []
        self.niveau = niveau
        self.opti_mise = opti_mise  # FIXME: virer ce nom de merde
        self.argent_precedent = self.argent

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
        """ Permet au bot de piocher de façon intelligente """

        def valeur_carte(carte):
            """ renvoie la valeur d'une carte """
            return min(carte, 10)

        def calcule_proba(score, recurence = False, carte_piochee = -1):
            total_cartes = 52 * NB_PAQUETS
            cartes_possibles = [4 * NB_PAQUETS for _ in range(13)]

            for cartes_tour in self.memoire_cartes:
                for carte in cartes_tour:
                    cartes_possibles[carte.valeur - 1] -= 1
                    total_cartes -= 1

            if carte_piochee != -1:
                cartes_possibles[carte_piochee] -= 1
                total_cartes -= 1

            proba_depasse = 0
            for carte, nombre in enumerate(cartes_possibles):
                score_carte = valeur_carte(carte + 1)
                # Score > 21
                if self.score() + score_carte > 21:
                    # Score > 21 pour la première fois et on a au moins un as qui vaut 11
                    if self.possede_as() and recurence is False:
                        prochain_score = score + score_carte - 10
                        proba_depasse += calcule_proba(prochain_score, True, carte) / total_cartes

                    # Score > 21 et on peut rien y faire
                    else:
                        proba_depasse += nombre / total_cartes

            return proba_depasse

        def raisonnement_proba():
            while True:
                if (self.score() == 0 and len(self.cartes) > 0) or self.score() == 21:
                    return

                if calcule_proba(self.score()) < 0.5:
                    self.pioche_carte()
                else:
                    return

        def double_retable():
            """ Determine si faire un double est rentable ou non """
            if self.possede_as():
                if self.score() == 13 and 5 <= croupier.score() <= 6:
                    return True
                if 14 <= self.score() <= 16 and 4 <= croupier.score() <= 6:
                    return True
                if self.score() == 17 and 3 <= croupier.score() <= 6:
                    return True
                if self.score() == 18 and 2 <= croupier.score() <= 6:
                    return True
                if self.score() == 19 and croupier.score() == 6:
                    return True

            if self.score() == 9 and 2 <= croupier.score() <= 6:
                return True
            if self.score() == 10 and 2 <= croupier.score() <= 9:
                return True
            if self.score() == 11:
                return True

        if self.niveau == 0:
            while self.score() <= 17:
                self.pioche_carte()
            if self.score() in [17, 18] and randint(0, 2) == 0:
                self.pioche_carte()
            return

        if self.niveau > 0:
            if double_retable():
                self.double()
                return
            raisonnement_proba()

        if self.niveau < 0:
            if 19 <= self.score([pioche[0]]) <= 21:
                self.double()
                return

            carte_future = []
            score_max = self.score()
            i_max = 0
            i = 0
            while 0 < self.score(carte_future) <= 21:
                carte_future.append(pioche[i])
                if score_max <= self.score(carte_future):
                    score_max = self.score(carte_future)
                    i_max = i + 1
                i += 1
            self.pioche_carte(i_max)
            return


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
                if j.score() == 21 and len(j.cartes) == 2:
                    rv_gains -= round(j.mise * 1.5)

                elif j.score() > score_croupier:
                    rv_gains -= j.mise

                elif j.score () < score_croupier:
                    rv_gains += j.mise

            return rv_gains

        def valeur_carte(carte):
            """ renvoie la valeur d'une carte """
            return min(carte, 10)

        def esperence_gains(score, recurence = False, carte_piochee = -1):
            """ calcule les gains moyens possibles de gagner en piochant une carte """
            total_cartes = 52 * NB_PAQUETS
            cartes_possibles = [4 * NB_PAQUETS for _ in range(13)]

            for tour, cartes_tour in enumerate(self.memoire_cartes):
                for carte in cartes_tour:
                    cartes_possibles[carte.valeur - 1] -= 1
                    total_cartes -= 1

            if carte_piochee != -1:
                cartes_possibles[carte_piochee] -= 1
                total_cartes -= 1

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
                elif self.possede_as() and recurence is False:
                    prochain_score = score + score_carte - 10
                    gains = esperence_gains(prochain_score, True, carte)

                # Score > 21 et on peut rien y faire
                else:
                    gains = 0
                rv_esperence_gains += gains * (nombre / total_cartes)
            return rv_esperence_gains

        def raisonnement_esperence():
            while True:
                if (self.score() == 0 and len(self.cartes) > 0) or self.score() == 21:
                    return

                if esperence_gains(self.score()) >= calcule_gains(self.score()):
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
            carte_future = []
            score_max = self.score()
            i_max = 0
            i = 0
            while 0 < self.score(carte_future) <= 21:
                carte_future.append(pioche[i])
                if score_max <= self.score(carte_future):
                    score_max = self.score(carte_future)
                    i_max = i + 1
                i += 1
            self.pioche_carte(i_max)
            return


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


def init_joueurs(nombre_joueurs, nombre_bots):
    """ Créé les différentes instances des joueurs. """
    rv_liste_joueurs = []
    for i in range(nombre_joueurs):
        nom = str(input(f"Entrez le nom du joueur #{i+1} : "))
        rv_liste_joueurs.append(Joueur(nom, ARGENT_JOUEUR_DEPART))

    for i in range(nombre_bots):
        nom = str(input(f"Entrez le nom du bot #{i+1} : "))
        nom = f"Bot_{nom}"
        niveau = int(input(f"Entrez le niveau de {nom} (un entier) : "))
        while True:
            reponse = input(f"optimiser la mise de {nom}? (oui/non) : ")
            if reponse == "oui":
                opti_mise = True
                break

            if reponse == "non":
                opti_mise = False
                break
        rv_liste_joueurs.append(Bot(nom, ARGENT_JOUEUR_DEPART, niveau, opti_mise))
    return rv_liste_joueurs


def premier_tour():
    """ Demande la mise et fait piocher les deux premières cartes à chaque joueur. """

    def logique_split(id_joueur, j, recurence = False):
        """ créé les objest joueurs temporaires en cas de splits """

        def creer_split(id_joueur, j, recurence = False):
            # Créer le joueur temporaire:
            j_split = deepcopy(j)
            j_split.clone = j
            liste_joueurs.insert(id_joueur + 1, j_split)
            if j.split:
                j_split.nom = f"{j.nom}2"
            else:
                j_split.nom = f"{j.nom}_split"
            j_split.split = True

            # Remplacer une des carte de la paire par une autre carte
            j.cartes.pop(1)
            j.pioche_carte()
            print(j)

            j_split.cartes.pop(0)
            j_split.pioche_carte()
            print(j_split)

            # Reproposer un split dans le cas où l'original repioche une paire
            if j.possede_paire() and not recurence and not j.possede_as():
                recurence = True
                logique_split(id_joueur, j, recurence)

            # Reproposer un split dans le cas où le split repioche une paire
            if j_split.possede_paire() and not recurence and not j_split.possede_as():
                recurence = True
                logique_split(id_joueur + 1, j_split, recurence)

        class TS:
            """ Enum pour la table de décision """
            S = 1
            P = 2
            R = 3

        table_decision = [  # table_decision[ligne][colonne]
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.P, TS.P, TS.P, TS.P],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.P, TS.P, TS.P, TS.P],
                [TS.P, TS.P, TS.P, TS.S, TS.S, TS.P, TS.P, TS.P, TS.P, TS.P],
                [TS.P, TS.P, TS.P, TS.P, TS.P, TS.P, TS.P, TS.P, TS.P, TS.P],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.P, TS.P, TS.P, TS.P, TS.P],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.P, TS.P, TS.P, TS.P],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S, TS.S],
                [TS.S, TS.S, TS.S, TS.S, TS.S, TS.R, TS.S, TS.S, TS.R, TS.R],
                [TS.R, TS.R, TS.R, TS.R, TS.R, TS.R, TS.R, TS.R, TS.R, TS.R]]

        if isinstance(j, Bot):
            if j.opti_mise:
                ligne = j.cartes[0].score() - 1
                colonne = croupier.cartes[0].score() - 1
                if table_decision[ligne][colonne] == TS.S:
                    creer_split(id_joueur, j, recurence)
                    return

                if table_decision[ligne][colonne] == TS.P:
                    j.pioche_carte()
                    return

            else:
                creer_split(id_joueur, j, recurence)
                return

        else:
            while True:
                reponse = input("Vous avez une paire, voulez-vous faire un split? (oui/non) ")
                if reponse == "oui":
                    creer_split(id_joueur, j, recurence)
                    return

                if reponse == "non":
                    return

    def demande_mise(j):
        """ demande joueurs la mise et leur propose de quitter la table """
        def clamp_mise(val):
            return max(min(val, MISE_MAX), MISE_MIN)

        if isinstance(j, Bot):
            j.mise = clamp_mise(round(j.argent * 0.05))
            return

        while True:
            print(f"{j.nom}: misez de l'argent (entre {MISE_MIN}€ et {MISE_MAX}€)")
            mise = int(input(f"vous avez {j.argent}€ (misez 0 pour quitter la table) : "))
            if MISE_MIN <= mise <= MISE_MAX:
                j.mise = mise
                return

            if mise == 0:
                print(f"{j.nom} a quitté la table.")
                ordre_66.append(j)
                return

    def demande_assurance(j):
        """ Demande aux joueurs si il veulent une assurance """
        if isinstance(j, Bot):
            if j.opti_mise:
                j.assurance = False
                return
            j.assurance = True
            return

        # Pour les joueurs humains:
        while True:
            reponse = input("Le croupier à un as, miser une assurance? (oui/non) ")
            if reponse == "oui":
                j.assurance = True
                return
            if reponse == "non":
                j.assurance = False
                return

    # On demande la mise et propose au joueur de quitter la table:
    for id_joueur, j in enumerate(liste_joueurs):
        if j.split is False:
            demande_mise(j)

            j.pioche_carte(2)
            print(j)

            # Le joueur a un blackjack:
            if j.score() == 21 and len(j.cartes) == 2:
                print("Blackjack!!")


            # Le croupier a un as et on propose une assurance au joueur:
            if croupier.cartes[0].valeur == 1:
                demande_assurance(j)

            # Le croupier a une paire et on propose un split:
            if j.possede_paire():
                logique_split(id_joueur, j)
            print(" ")

    # On retire les joueurs qui ont dessidé de partir
    for j in ordre_66:
        liste_joueurs.remove(j)


def tour_joueur(j):
    """ Effectue le tour de chaque joueur """
    print("-------------")
    print(f"Tour de {j.nom} :\n{j}")
    print(" • Liste des actions:")
    print(" • pioche: pioche une carte")
    print(" • rester: passe au joueur suivant")
    print(" • double: pioche une carte, double la mise et passe au joueur suivant")
    print(" -> (seulement le premier tour)")

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

        elif reponse == "double" and len(j.cartes) == 2:
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

    def payer(j_argent, j_mise):
        if j_mise.assurance is True:
            if croupier.score() == 21 and len(croupier.cartes) == 2:
                j_argent.argent += j_mise.mise
            else:
                j_argent.argent -= j_mise.mise / 2

        if j_mise.score() == 21 and len(j_mise.cartes) == 2:
            j_argent.argent += round(j_mise.mise * 1.5)
            croupier.argent -= round(j_mise.mise * 1.5)
            print(f"{j_mise.nom} a gagné {j_mise.mise}€ et a maintenant {j_argent.argent}€")

        elif j_mise.score() > croupier.score():
            j_argent.argent += j_mise.mise
            croupier.argent -= j_mise.mise
            print(f"{j_mise.nom} a gagné {j_mise.mise}€ et a maintenant {j_argent.argent}€")

        elif j_mise.score() < croupier.score():
            j_argent.argent -= j_mise.mise
            croupier.argent += j_mise.mise
            print(f"{j_mise.nom} a perdu {j_mise.mise}€ et a maintenant {j_argent.argent}€")

        else:  # en cas d'égalité
            print(f"Égalité entre {j_mise.nom} et le croupier")

    print("-------------")
    for j in liste_joueurs:
        if j.split is False:
            payer(j, j)

        else:
            payer(j.clone, j)
            ordre_66.append(j)


def remplir_pioche():
    """ Récupère les cartes sur la table, les mélangent et les ajoute à la fin de la pioche """
    cartes_recuperees = []
    for j in liste_joueurs:
        cartes_recuperees.extend(j.cartes)
        j.cartes.clear()
    cartes_recuperees.extend(croupier.cartes)
    croupier.cartes.clear()
    pioche.extend(sample(cartes_recuperees, k=len(cartes_recuperees)))


if __name__ == "__main__":
    # Initialisation:
    nb_joueurs = int(input("Entrez le nombre de joueurs humains : "))
    nb_bots = int(input("Entrez le nombre de bots : "))
    liste_joueurs = init_joueurs(nb_joueurs, nb_bots)
    NB_PAQUETS = 4 * ((len(liste_joueurs) // 4) + 1)
    pioche = init_pioche()
    croupier = Croupier(ARGENT_CROUPIER_DEPART, 1)
    croupier.niveau = int(input("entrez le niveau du croupier (un entier) : "))
    ordre_66 = []
    joueurs_partis = []
    tour = 0

    # Boucle principale:
    while len(liste_joueurs) > 0 and croupier.argent > MISE_MIN:
        tour += 1
        print("___________________________")
        croupier.pioche_carte()
        print(croupier)
        premier_tour()
        for joueur in liste_joueurs:
            if joueur.score() != 21:
                if isinstance(joueur, Bot):  # si le joueur est un bot
                    joueur.pioche_intelligente()
                else:  # si le joueur est un humain
                    tour_joueur(joueur)
                print(joueur)

        croupier.pioche_carte()

        croupier.regarde_cartes()
        croupier.pioche_intelligente()
        print(croupier)

        regler_mises()
        remplir_pioche()

        for joueur in liste_joueurs:
            joueur.cartes.clear()
            if joueur.argent < MISE_MIN:
                ordre_66.append(joueur)

        for joueur in ordre_66:
            liste_joueurs.remove(joueur)
            if not joueur.split:
                if joueur.argent > 0:
                    joueurs_partis.append( (joueur, tour, "quitté la table") )
                else:
                    joueurs_partis.append( (joueur, tour, "perdu") )

        ordre_66.clear()

    print("___________________________")
    for joueur, tour_perdu, motif in joueurs_partis:
        print(f"{joueur.nom} a {motif} au tour {tour_perdu} avec {joueur.argent}€")
    print("___________________________")
    for joueur in liste_joueurs:
        print(f"{joueur.nom} a battu le croupier après {tour} tours et a {joueur.argent}€")
