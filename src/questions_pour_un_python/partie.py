"""Déroulement d'une partie : boucle de jeu, questions et règles."""

import random

from .donnees import tirer_duel

# Types de questions disponibles. On ajoutera "reference" et "qcm" ensuite.
TYPES_QUESTIONS = ["duel"]

POINTS = {
    "duel": 10,
}


def demander_choix(message, choix_valides):
    """Redemande tant que la saisie ne fait pas partie des choix valides."""
    reponse = input(message).strip()
    while reponse not in choix_valides:
        print(f"Réponse invalide, choisis parmi : {', '.join(choix_valides)}")
        reponse = input(message).strip()
    return reponse


class Partie:
    """Une partie de Questions pour un Python."""

    def __init__(self, joueur, df_theme, difficulte, sens="plus_grand"):
        """
        sens vaut "plus_grand" (ex : la ville la plus peuplée)
        ou "plus_petit" (ex : l'événement le plus ancien en histoire).
        """
        self.joueur = joueur
        self.df_theme = df_theme
        self.difficulte = difficulte
        self.sens = sens
        self.numero_tour = 0

    def choisir_type_question(self):
        """Tire au hasard le type de la prochaine question."""
        return random.choice(TYPES_QUESTIONS)

    def poser_duel(self):
        """Pose une question duel. Renvoie True si le joueur a bon."""
        element_1, element_2 = tirer_duel(self.df_theme, self.difficulte)

        if self.sens == "plus_petit":
            print("⌛ Lequel est arrivé en premier ?")
            premier_gagne = element_1["valeur"] < element_2["valeur"]
        else:
            print("⚖ Lequel a la plus grande valeur ?")
            premier_gagne = element_1["valeur"] > element_2["valeur"]

        print(f"  1. {element_1['nom']}")
        print(f"  2. {element_2['nom']}")

        bonne_reponse = "1" if premier_gagne else "2"
        reponse = demander_choix("Ta réponse (1 ou 2) : ", ["1", "2"])

        for element in (element_1, element_2):
            valeur = f"{element['valeur']} {element['unite']}".strip()
            print(f"  ➜ {element['nom']} : {valeur}")

        return reponse == bonne_reponse

    def jouer_tour(self):
        """Choisit un type de question, la pose et met à jour le joueur."""
        self.numero_tour += 1
        print(f"\n═══════ ? Question {self.numero_tour} ? ═══════")

        type_question = self.choisir_type_question()
        questions = {
            "duel": self.poser_duel,
        }
        a_bon = questions[type_question]()

        if a_bon:
            bonus = self.joueur.bonne_reponse(POINTS[type_question])
            print("✔ Bonne réponse !")
            if bonus:
                print(f"⚡ Bonus de série : +{bonus} points !")
        else:
            self.joueur.mauvaise_reponse()
            print("✘ Raté... tu perds une vie")

        print(self.joueur)

    def lancer(self):
        """Enchaîne les tours tant que le joueur a des vies."""
        print(f"► C'est parti {self.joueur.pseudo} !")
        print(self.joueur)

        while self.joueur.est_vivant():
            self.jouer_tour()

        print("\n☠ Plus de vies, la partie est terminée !")
        print(f"★ Score final : {self.joueur.score} points")
        print(f"⚡ Meilleure série : {self.joueur.meilleure_serie}")