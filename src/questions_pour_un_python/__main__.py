"""Menu principal de 'Questions pour un Python'."""

from .donnees import charger_reperes
from .joueur import Joueur
from .partie import Partie, demander_choix
from .scores import afficher_stats, charger_scores, enregistrer_score

TITRE = r"""
╔══════════════════════════════════════════╗
║        ? QUESTIONS POUR UN PYTHON ?      ║
║      Le quiz d'histoire en console       ║
╚══════════════════════════════════════════╝
"""


def demander_pseudo():
    """Redemande le pseudo tant qu'il est vide."""
    while True:
        try:
            return Joueur(input("Ton pseudo : "))
        except ValueError as erreur:
            print(f"⚠ {erreur}")


def demander_difficulte():
    """Renvoie "facile" ou "difficile"."""
    print("\nChoisis la difficulté :")
    print("  1. Facile (dates éloignées)")
    print("  2. Difficile (dates proches)")
    choix = demander_choix("Ton choix : ", ["1", "2"])
    return "facile" if choix == "1" else "difficile"


def jouer(df_reperes):
    """Lance une partie complète puis enregistre le score."""
    joueur = demander_pseudo()
    difficulte = demander_difficulte()

    Partie(joueur, df_reperes, difficulte).lancer()

    enregistrer_score(joueur)
    afficher_stats(charger_scores())


def main():
    print(TITRE)

    try:
        df_reperes = charger_reperes()
    except FileNotFoundError as erreur:
        print(f"⚠ Impossible de lancer le jeu : {erreur}")
        return

    while True:
        print("\n☰ Menu")
        print("  1. Jouer")
        print("  2. Voir les meilleurs scores")
        print("  3. Quitter")
        choix = demander_choix("Ton choix : ", ["1", "2", "3"])

        if choix == "1":
            jouer(df_reperes)
        elif choix == "2":
            afficher_stats(charger_scores())
        else:
            print("À bientôt pour de nouvelles questions !")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPartie interrompue. À bientôt !")