"""Chargement des repères historiques et tirage des questions."""

from pathlib import Path

import numpy as np
import pandas as pd


CHEMIN_REPERES = (Path(__file__).resolve().parents[2]/ "data" / "reperes_histoire.csv")

# random.random() et random.randint() sont obsolètes, on utilise numpy.random.default_rng() pour un tirage plus sûr
rng = np.random.default_rng()


def charger_reperes(chemin=CHEMIN_REPERES):
    """
    Charge les repères historiques et renvoie un DataFrame trié par année
    avec les colonnes nom, annee, date_texte, type et source.
    """
    if not Path(chemin).exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")

    df = pd.read_csv(chemin)
    df = df.rename(columns={"evenement": "nom", "annee_debut": "annee"})
    df = df.dropna(subset=["nom", "annee"])
    df = df[["nom", "annee", "date_texte", "type", "source"]]
    return df.sort_values("annee").reset_index(drop=True)


def tirer_duel(df, difficulte):
    """
    Tire deux repères avec des années différentes.
    En facile, les années sont éloignées. En difficile, elles sont proches.
    """
    premier = df.iloc[rng.integers(len(df))]

    candidats = df[df["annee"] != premier["annee"]].copy()
    candidats["ecart"] = (candidats["annee"] - premier["annee"]).abs()
    candidats = candidats.sort_values("ecart")

    moitie = max(1, len(candidats) // 2)
    if difficulte == "difficile":
        candidats = candidats.head(moitie)
    else:
        candidats = candidats.tail(moitie)

    second = candidats.iloc[rng.integers(len(candidats))]
    second = second.drop("ecart")

    duel = [premier.to_dict(), second.to_dict()]
    rng.shuffle(duel)
    return duel[0], duel[1]


def tirer_qcm(df, nb_choix, difficulte):
    """
    Tire un repère (la bonne réponse) et des repères pièges,
    tous avec des années différentes.

    Renvoie (bonne_reponse, propositions, position_bonne_reponse).
    En difficile, les pièges sont pris parmi les années voisines.
    """
    df = df.drop_duplicates(subset="annee").reset_index(drop=True)
    position = int(rng.integers(len(df)))
    bonne = df.iloc[position]

    autres = df.drop(index=position)
    if difficulte == "difficile":
        ecart_rang = (autres.index.to_series() - position).abs()
        autres = autres.loc[ecart_rang.sort_values().index[:nb_choix * 2]]

    pieges = autres.sample(nb_choix - 1, random_state=int(rng.integers(1_000_000)))

    propositions = [bonne.to_dict()] + pieges.to_dict("records")
    rng.shuffle(propositions)
    position_bonne = next(i for i, p in enumerate(propositions) if p["annee"] == bonne["annee"])
    return bonne.to_dict(), propositions, position_bonne


def formater_annee(annee):
    """Affiche une année lisible : 52 av. J.-C. au lieu de -52."""
    annee = int(annee)
    if annee < 0:
        return f"{-annee} av. J.-C."
    return str(annee)