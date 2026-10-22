"""Sauvegarde des scores et statistiques."""

from datetime import date
from pathlib import Path

import pandas as pd


# scores.csv est à la racine du projet.
CHEMIN_SCORES = Path(__file__).resolve().parents[2] / "scores.csv"
COLONNES = ["date", "pseudo", "score", "meilleure_serie"]


def charger_scores(chemin=CHEMIN_SCORES):
    """Renvoie le tableau des scores, vide si le fichier n'existe pas."""
    if not Path(chemin).exists():
        return pd.DataFrame(columns=COLONNES)

    try:
        return pd.read_csv(chemin)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        print("⚠ Le fichier des scores est illisible, on repart de zéro.")
        return pd.DataFrame(columns=COLONNES)


def enregistrer_score(joueur, chemin=CHEMIN_SCORES):
    """Ajoute le score du joueur à la fin du fichier."""
    nouvelle_ligne = pd.DataFrame([{
        "date": date.today().isoformat(),
        "pseudo": joueur.pseudo,
        "score": joueur.score,
        "meilleure_serie": joueur.meilleure_serie,
    }])
    fichier_existe = Path(chemin).exists()
    nouvelle_ligne.to_csv(chemin, mode="a", header=not fichier_existe, index=False)


def afficher_stats(df_scores):
    """Affiche le classement et quelques statistiques."""
    if df_scores.empty:
        print("Aucune partie enregistrée pour l'instant.")
        return

    print("\n★ ★ ★  Meilleurs scores  ★ ★ ★")
    top = df_scores.sort_values("score", ascending=False).head(5)
    for rang, ligne in enumerate(top.itertuples(), start=1):
        print(f"  {rang}. {ligne.pseudo} : {ligne.score} pts "
            f"(série de {ligne.meilleure_serie}, le {ligne.date})")

    print(f"\nParties jouées : {len(df_scores)}")
    print(f"Score moyen : {df_scores['score'].mean():.0f} pts")
    print(f"Plus longue série : {df_scores['meilleure_serie'].max()}")