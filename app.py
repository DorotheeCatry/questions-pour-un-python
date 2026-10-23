"""Version web (Streamlit) de Questions pour un Python.

Lancement : uv run streamlit run app.py
"""

from html import escape
from pathlib import Path

import streamlit as st

from questions_pour_un_python.donnees import (charger_reperes, formater_annee,
                                                tirer_duel, tirer_qcm)
from questions_pour_un_python.joueur import VIES_DE_DEPART, Joueur
from questions_pour_un_python.partie import NB_CHOIX_QCM, POINTS, Partie
from questions_pour_un_python.scores import charger_scores, enregistrer_score

DOSSIER_ASSETS = Path(__file__).parent / "assets"
LOGO = DOSSIER_ASSETS / "logo.png"
STYLE = DOSSIER_ASSETS / "style.css"

# Icône et nom affichés pour chaque type de question
TYPES = {
    "duel": ("⚔", "Duel"),
    "avant_apres": ("⇄", "Avant ou après"),
    "qcm": ("✎", "QCM"),
}

MEDAILLES = ["🥇", "🥈", "🥉", "4", "5"]

st.set_page_config(page_title="Questions pour un Python",
                    page_icon=str(LOGO))


def html(contenu):
    """Affiche du HTML (on l'utilise pour les éléments stylés en CSS)."""
    st.markdown(contenu, unsafe_allow_html=True)


html(f"<style>{STYLE.read_text(encoding='utf-8')}</style>")


@st.cache_data
def reperes():
    """Charge le CSV une seule fois, puis le garde en mémoire."""
    return charger_reperes()


# --- Préparation des questions ---

def nouvelle_question(partie):
    """Prépare une question au hasard sous forme de dictionnaire."""
    type_question = partie.choisir_type_question()
    df = partie.reperes_disponibles()

    if type_question == "qcm":
        bonne, propositions, position = tirer_qcm(
            df, NB_CHOIX_QCM, partie.difficulte)
        partie.marquer_vus(bonne)
        debut = "En quelle année"
        if bonne["type"] == "periode":
            debut = "En quelle année a commencé"
        return {
            "type": type_question,
            "titre": f"{debut} : <strong>{escape(bonne['nom'])}</strong> ?",
            "options": [formater_annee(p["annee"]) for p in propositions],
            "bonne": position,
            "a_reveler": [bonne],
        }

    repere_1, repere_2 = tirer_duel(df, partie.difficulte)
    partie.marquer_vus(repere_1, repere_2)

    if type_question == "duel":
        return {
            "type": type_question,
            "titre": "Lequel s'est passé en premier ?",
            "options": [repere_1["nom"], repere_2["nom"]],
            "details": [repere_1["date_texte"], repere_2["date_texte"]],
            "bonne": 0 if repere_1["annee"] < repere_2["annee"] else 1,
            "a_reveler": [],
        }

    return {
        "type": type_question,
        "titre": (f"{escape(repere_1['nom'])} : "
                    f"<strong>{escape(repere_1['date_texte'])}</strong>.<br>"
                    f"Et « {escape(repere_2['nom'])} », "
                    "c'était avant ou après ?"),
        "options": ["Avant", "Après"],
        "bonne": 0 if repere_2["annee"] < repere_1["annee"] else 1,
        "a_reveler": [repere_2],
    }


# --- Actions déclenchées par les boutons ---

def demarrer():
    """Crée le joueur et la partie à partir du formulaire d'accueil."""
    try:
        joueur = Joueur(st.session_state.pseudo)
    except ValueError as erreur:
        st.session_state.erreur = str(erreur)
        return

    partie = Partie(joueur, reperes(), st.session_state.difficulte)
    partie.numero_tour = 1
    st.session_state.partie = partie
    st.session_state.question = nouvelle_question(partie)
    st.session_state.reponse = None
    st.session_state.score_enregistre = False
    st.session_state.record = False
    st.session_state.erreur = None


def repondre(choix):
    """Vérifie la réponse et met à jour le joueur."""
    joueur = st.session_state.partie.joueur
    question = st.session_state.question

    a_bon = choix == question["bonne"]
    bonus = 0
    if a_bon:
        bonus = joueur.bonne_reponse(POINTS[question["type"]])
    else:
        joueur.mauvaise_reponse()

    st.session_state.reponse = {"choix": choix, "a_bon": a_bon,
                                "bonus": bonus}


def question_suivante():
    partie = st.session_state.partie
    partie.numero_tour += 1
    st.session_state.question = nouvelle_question(partie)
    st.session_state.reponse = None


def retour_accueil():
    del st.session_state.partie


# --- Affichage : éléments communs ---

def afficher_logo(taille):
    """Logo centré, plus grand quand la colonne du milieu est plus large."""
    _, milieu, _ = st.columns([1, taille, 1])
    milieu.image(str(LOGO))


def afficher_classement():
    scores = charger_scores()
    if scores.empty:
        return

    top = scores.sort_values("score", ascending=False).head(5)
    lignes = []
    for rang, ligne in enumerate(top.itertuples()):
        lignes.append(
            '<div class="ligne-score">'
            f'<span class="rang">{MEDAILLES[rang]}</span>'
            f'<span class="pseudo">{escape(str(ligne.pseudo))}</span>'
            f'<span class="points">{ligne.score} pts</span>'
            "</div>"
        )
    html('<div class="classement"><h3>🏆 Meilleurs scores</h3>'
            + "".join(lignes) + "</div>")


# --- Écran d'accueil ---

def afficher_accueil():
    afficher_logo(taille=2)
    html('<p class="accroche">Teste tes connaissances sur les grandes '
            "dates de l'histoire de France et du monde !</p>")

    regles = [
        ("⚔", "Duel", "Lequel s'est passé en premier ?"),
        ("⇄", "Avant ou après", "On te donne une date, situe l'autre."),
        ("✎", "QCM", "Quatre années, une seule est la bonne."),
    ]
    for colonne, (icone, titre, texte) in zip(st.columns(3), regles):
        with colonne:
            html(f'<div class="regle"><div class="icone">{icone}</div>'
                f"<b>{titre}</b><p>{texte}</p></div>")

    st.write("")
    with st.container(key="carte_depart"):
        st.text_input("Ton pseudo", key="pseudo",
                    placeholder="Ex : Vercingétorix")
        st.radio("Difficulté", ["facile", "difficile"], key="difficulte",
                    horizontal=True,
                    captions=["Dates éloignées", "Dates proches"])
        st.button("▶ Commencer la partie", on_click=demarrer,
                    type="primary", width="stretch")
        if st.session_state.get("erreur"):
            st.error(st.session_state.erreur)

    html('<p class="infos-regles">💚💚💚 Trois vies · ⚡ Bonus à partir de '
            "3 bonnes réponses d'affilée</p>")
    afficher_classement()


# --- Écran de jeu ---

def afficher_statut(joueur):
    coeurs = "💚" * joueur.vies + "🤍" * (VIES_DE_DEPART - joueur.vies)
    pastilles = [
        ("Score", f"{joueur.score} pts"),
        ("Vies", coeurs),
        ("Série", f"⚡ {joueur.serie}"),
    ]
    contenu = "".join(
        f'<div class="pastille"><span>{nom}</span><b>{valeur}</b></div>'
        for nom, valeur in pastilles
    )
    html(f'<div class="statut">{contenu}</div>')


def classe_option(i, question, reponse):
    """Couleur d'un choix une fois la réponse donnée."""
    if i == question["bonne"]:
        return "juste"
    if i == reponse["choix"]:
        return "faux"
    return "neutre"


def afficher_options(question, reponse):
    """Boutons avant la réponse, choix colorés après."""
    options = question["options"]

    if question["type"] == "duel":
        colonnes = st.columns([5, 1, 5], vertical_alignment="center")
        with colonnes[1]:
            html('<div class="vs">VS</div>')
        cases = [colonnes[0], colonnes[2]]
    else:
        grille = st.columns(2)
        cases = [grille[i % 2] for i in range(len(options))]

    for i, (case, option) in enumerate(zip(cases, options)):
        with case:
            if reponse is None:
                st.button(option, key=f"option_{i}", on_click=repondre,
                            args=(i,), width="stretch")
                continue

            detail = ""
            if "details" in question:
                detail = (f'<span class="detail">'
                        f'{escape(question["details"][i])}</span>')
            classe = classe_option(i, question, reponse)
            html(f'<div class="option {classe}">{escape(option)}'
                f"{detail}</div>")


def afficher_retour(question, reponse):
    """Message bonne ou mauvaise réponse, puis les vraies dates."""
    if reponse["a_bon"]:
        message = "✔ Bonne réponse !"
        if reponse["bonus"]:
            message += f" ⚡ Bonus de série : +{reponse['bonus']} points"
        html(f'<div class="retour juste">{message}</div>')
    else:
        html('<div class="retour faux">✘ Raté... tu perds une vie</div>')

    for repere in question["a_reveler"]:
        html(f'<p class="revelation">➜ <b>{escape(repere["nom"])}</b> : '
            f'{escape(repere["date_texte"])}</p>')


def afficher_partie():
    partie = st.session_state.partie
    joueur = partie.joueur
    question = st.session_state.question
    reponse = st.session_state.reponse

    afficher_logo(taille=1)
    afficher_statut(joueur)

    with st.container(key="carte_question"):
        icone, nom_type = TYPES[question["type"]]
        html('<div class="entete">'
            f'<span class="badge">{icone} {nom_type}</span>'
            f'<span class="numero">Question {partie.numero_tour}</span>'
            "</div>")
        html(f'<p class="question">{question["titre"]}</p>')

        afficher_options(question, reponse)

        if reponse is not None:
            afficher_retour(question, reponse)
            if joueur.est_vivant():
                st.write("")
                st.button("Question suivante ➜", on_click=question_suivante,
                            type="primary", width="stretch")

    if reponse is not None and not joueur.est_vivant():
        afficher_fin(joueur)


# --- Fin de partie ---

def afficher_fin(joueur):
    # On enregistre une seule fois, même si la page se recharge.
    if not st.session_state.score_enregistre:
        anciens_scores = charger_scores()
        st.session_state.record = (anciens_scores.empty or joueur.score
                                    > anciens_scores["score"].max())
        enregistrer_score(joueur)
        st.session_state.score_enregistre = True
        if st.session_state.record and joueur.score > 0:
            st.balloons()

    st.write("")
    with st.container(key="carte_fin"):
        html('<h2 class="fin-titre">☠ Partie terminée !</h2>')
        html(f'<div class="score-final">{joueur.score} pts</div>')
        html(f'<p class="sous-score">⚡ Meilleure série : '
            f"{joueur.meilleure_serie}</p>")
        if st.session_state.record and joueur.score > 0:
            html('<p class="record">🎉 Nouveau record !</p>')
        st.button("↺ Rejouer", on_click=retour_accueil, type="primary",
                    width="stretch")

    afficher_classement()


if "partie" in st.session_state:
    afficher_partie()
else:
    afficher_accueil()