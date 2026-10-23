"""Gestion du joueur : pseudo, score, vies et série de bonnes réponses."""

VIES_DE_DEPART = 3
SERIE_POUR_BONUS = 3
POINTS_BONUS = 5


class Joueur:
    """Un joueur de Questions pour un Python."""

    def __init__(self, pseudo):
        pseudo = pseudo.strip()
        if not pseudo:
            raise ValueError("Le pseudo ne peut pas être vide.")

        self.pseudo = pseudo
        self.score = 0
        self.vies = VIES_DE_DEPART
        self.serie = 0
        self.meilleure_serie = 0

    def bonne_reponse(self, points):
        """Ajoute les points de la question et renvoie le bonus gagné."""
        self.serie += 1
        self.meilleure_serie = max(self.meilleure_serie, self.serie)

        bonus = 0
        if self.serie >= SERIE_POUR_BONUS:
            bonus = POINTS_BONUS

        self.score += points + bonus
        return bonus

    def mauvaise_reponse(self):
        """Retire une vie et remet la série à zéro."""
        self.vies -= 1
        self.serie = 0

    def est_vivant(self):
        """Renvoie True tant qu'il reste au moins une vie au joueur."""
        return self.vies > 0

    def __str__(self):
        coeurs_pleins = ["♥"] * self.vies
        coeurs_vides = ["♡"] * (VIES_DE_DEPART - self.vies)
        coeurs = " ".join(coeurs_pleins + coeurs_vides)
        return f"☺ {self.pseudo} | ★ {self.score} pts | {coeurs}"