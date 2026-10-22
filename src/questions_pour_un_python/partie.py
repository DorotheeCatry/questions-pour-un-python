"""Déroulement d'une partie : boucle de jeu, questions et règles."""

import random

from .donnees import formater_annee, tirer_duel, tirer_qcm

POINTS = {
    "duel": 10,
    "avant_apres": 10,
    "qcm": 15,
}

NB_CHOIX_QCM = 4

# En dessous de ce nombre de repères pas encore vus, on remet tout en jeu.
MINIMUM_DISPONIBLES = 10


def demander_choix(message, choix_valides):
    """Redemande tant que la saisie ne fait pas partie des choix valides."""
    reponse = input(message).strip()
    while reponse not in choix_valides:
        print(f"Réponse invalide, choisis parmi : {', '.join(choix_valides)}")
        reponse = input(message).strip()
    return reponse


def afficher_reponse(repere):
    """Affiche la vraie date d'un repère, telle qu'elle est dans la source."""
    print(f"  ➜ {repere['nom']} : {repere['date_texte']}")


class Partie:
    """Une partie de Questions pour un Python."""

    def __init__(self, joueur, df_reperes, difficulte):
        self.joueur = joueur
        self.df_reperes = df_reperes
        self.difficulte = difficulte
        self.numero_tour = 0
        self.deja_vus = set()

    def reperes_disponibles(self):
        """Renvoie les repères qui n'ont pas encore été montrés."""
        disponibles = self.df_reperes[
            ~self.df_reperes["nom"].isin(self.deja_vus)]

        if len(disponibles) < MINIMUM_DISPONIBLES:
            self.deja_vus.clear()
            return self.df_reperes
        return disponibles

    def marquer_vus(self, *reperes):
        """Retient les repères montrés pour ne pas les reposer."""
        for repere in reperes:
            self.deja_vus.add(repere["nom"])

    def choisir_type_question(self):
        """Tire au hasard le type de la prochaine question."""
        return random.choice(list(POINTS))

    def poser_duel(self):
        """Lequel des deux repères est le plus ancien ?"""
        repere_1, repere_2 = tirer_duel(self.reperes_disponibles(),
                                        self.difficulte)
        self.marquer_vus(repere_1, repere_2)

        print("⌛ Lequel s'est passé en premier ?")
        print(f"  1. {repere_1['nom']}")
        print(f"  2. {repere_2['nom']}")

        bonne_reponse = "1" if repere_1["annee"] < repere_2["annee"] else "2"
        reponse = demander_choix("Ta réponse (1 ou 2) : ", ["1", "2"])

        afficher_reponse(repere_1)
        afficher_reponse(repere_2)
        return reponse == bonne_reponse

    def poser_avant_apres(self):
        """On donne la date d'un repère, l'autre est-il avant ou après ?"""
        reference, mystere = tirer_duel(self.reperes_disponibles(),
                                        self.difficulte)
        self.marquer_vus(reference, mystere)

        print(f"⇄ {reference['nom']} : {reference['date_texte']}.")
        print(f"  Et « {mystere['nom']} », c'était avant ou après ?")
        print("  1. Avant")
        print("  2. Après")

        bonne_reponse = "1" if mystere["annee"] < reference["annee"] else "2"
        reponse = demander_choix("Ta réponse (1 ou 2) : ", ["1", "2"])

        afficher_reponse(mystere)
        return reponse == bonne_reponse

    def poser_qcm(self):
        """En quelle année ? Quatre propositions, une seule juste."""
        bonne, propositions, position_bonne = tirer_qcm(
            self.reperes_disponibles(), NB_CHOIX_QCM, self.difficulte)
        self.marquer_vus(bonne)

        if bonne["type"] == "periode":
            print(f"✎ En quelle année a commencé : {bonne['nom']} ?")
        else:
            print(f"✎ En quelle année : {bonne['nom']} ?")

        for numero, proposition in enumerate(propositions, start=1):
            print(f"  {numero}. {formater_annee(proposition['annee'])}")

        choix_valides = [str(i) for i in range(1, len(propositions) + 1)]
        reponse = demander_choix(
            f"Ta réponse (1 à {len(propositions)}) : ", choix_valides)

        afficher_reponse(bonne)
        return int(reponse) - 1 == position_bonne

    def jouer_tour(self):
        """Choisit un type de question, la pose et met à jour le joueur."""
        self.numero_tour += 1
        print(f"\n═══════ ? Question {self.numero_tour} ? ═══════")

        type_question = self.choisir_type_question()
        questions = {
            "duel": self.poser_duel,
            "avant_apres": self.poser_avant_apres,
            "qcm": self.poser_qcm,
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