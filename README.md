# Questions pour un Python

**Un quiz d'histoire en console**

Petit jeu fait en Python pendant la game jam de la formation.

Le principe : à chaque tour, le jeu tire au hasard un type de question parmi trois, sur des grandes dates de l'histoire de France et du monde.

* **Le duel** : deux événements, il faut trouver lequel s'est passé en premier
  * "Qu'est-ce qui s'est passé en premier : le Code noir ou la guerre de Sept Ans ?"
* **Avant ou après** : le jeu donne la date d'un événement, il faut dire si le deuxième était avant ou après
  * "La Bastille a été prise le 14 juillet 1789. Le couronnement de Charlemagne, c'était avant ou après ?"
* **Le QCM** : une question, quatre années proposées, une seule est juste
  * "En quelle année : chute du mur de Berlin ?"

Comme on ne sait jamais quelle question va tomber, ça évite que le jeu devienne répétitif.

On gagne des points à chaque bonne réponse (un peu plus pour le QCM), avec un bonus si on enchaîne. Au bout de 3 erreurs, la partie est fini.

> Projet réalisé en binôme : Sami Kabdani & Dorothée Catry

## Lancer le jeu

Il faut Python 3.10 ou plus.

```bash
pip install -r requirements.txt
python main.py
```

## Comment on joue

1. On entre son pseudo
2. On choisit la difficulté
   * facile : les dates à comparer sont très éloignées
   * difficile : les dates sont proches, il faut vraiment savoir
3. Le jeu pose les questions en mélangeant les trois types
   * duel et avant/après : on répond 1 ou 2
   * QCM : on répond 1, 2, 3 ou 4
4. Après chaque réponse, le jeu affiche les vraies dates
5. A la fin, le score est enregistré et on voit le classement

## Structure du projet

```
questions-pour-un-python/
├── src/
│   └── questions_pour_un_python/
│       ├── __init__.py
│       ├── __main__.py    # menu et lancement du jeu
│       ├── joueur.py      # classe Joueur
│       ├── partie.py      # classe Partie (boucle de jeu, questions)
│       ├── donnees.py     # chargement des repères et tirages
│       └── scores.py      # sauvegarde des scores et statistiques
├── data/
│   └── reperes_histoire.csv
├── scores.csv             # créé automatiquement à la première partie
├── pyproject.toml         # dépendances du projet (uv)
├── uv.lock                # versions exactes installées
└── README.md
```

## Les données

Les dates viennent des repères officiels des programmes d'histoire :

* Éduscol, "Fixer des repères en histoire-géographie", voie professionnelle (2021) : les repères de la seconde à la terminale bac pro
* le programme de primaire de 2008 (BO hors-série n°3 du 19 juin 2008) : pour les dates plus anciennes (Alésia, Clovis, Charlemagne...)
* la liste des repères du brevet d'un collège de l'académie d'Amiens

Chaque ligne du CSV garde sa source dans une colonne `source`, pour pouvoir vérifier une réponse.

Quelques choix :

* les dates avant J.-C. sont stockées en négatif (Alésia = -52) et affichées "52 av. J.-C."
* pour les périodes (ex : Grande Guerre 1914-1918), le jeu compare l'année de début
* le jeu ne met jamais face à face deux événements de la même année

## Organisation

On a découpé le projet en deux rôles qui peuvent avancer en même temps.

**Sami : données et scores**

- `donnees.py`
- `scores.py`
- préparation des CSV

**Dorothée : moteur de jeu**

- `joueur.py`
- `partie.py`
- `main.py`

Pour que chacun puisse coder sans attendre l'autre, on a fixé au début ce que chaque fonction reçoit et renvoie.

`donnees.py`

- `lister_themes()` : renvoie la liste des thèmes disponibles (noms des fichiers dans `data/`)
- `charger_theme(nom_theme)` : renvoie un DataFrame avec au moins les colonnes `nom`, `valeur`, `unite`, `source`
- `tirer_duel(df, difficulte)` : renvoie deux lignes du DataFrame (sous forme de dictionnaires) avec deux valeurs différentes
- `tirer_reference(df, difficulte)` : renvoie l'élément de référence (dont on montre la valeur) et l'élément à deviner, avec deux valeurs différentes
- `tirer_qcm(df, nb_choix, difficulte)` : renvoie l'élément de la question, la liste des valeurs proposées (déjà mélangée, toutes différentes) et la position de la bonne réponse

Pour la difficulté : en facile, les valeurs tirées sont éloignées les unes des autres, en difficile elles sont proches.

`scores.py`

- `charger_scores(chemin)` : renvoie un DataFrame des scores, vide si le fichier n'existe pas encore
- `enregistrer_score(chemin, pseudo, theme, score)` : ajoute une ligne au fichier
- `afficher_stats(df_scores)` : affiche le classement et quelques stats

`joueur.py`

- classe `Joueur(pseudo)` avec `score`, `vies`, `serie`
- méthodes `bonne_reponse()`, `mauvaise_reponse()`, `est_vivant()`

`partie.py`

- classe `Partie(joueur, df_theme, difficulte)`
- `choisir_type_question()` : tire au hasard "duel", "reference" ou "qcm"
- `poser_duel()`, `poser_reference()`, `poser_qcm()` : une méthode par type de question, chacune renvoie True si le joueur a bon
- `jouer_tour()` : choisit le type, pose la question, met à jour le joueur
- `lancer()` : enchaîne les tours tant que le joueur a des vies

### Git

- une branche par fonctionnalité : `feature/chargement-donnees`, `feature/classe-joueur`, `feature/boucle-partie`, `feature/scores`...
- messages de commit du type `feat: ...`, `fix: ...`, `docs: ...`

## Planning

**Jour 1 matin**

- [X] création du dépôt et du README
- [X] CSV histoire (généré à partir de pdfs)

**Jour 1 après-midi**

- [X] Sami : chargement des thèmes & questions
- [X] Dorothée : classes Joueur et Partie + niveaux de difficulté
- [X] Ensemble : première fusion
- [ ] Sami : scores et classement

**Jour 2 matin**

- [ ] Dorothée : préparation de la démo

## Notions du cours utilisées

- variables, types, conditions, boucles (la boucle de jeu)
- fonctions
- listes et dictionnaires
- fichier (lecture de CSV, sauvegarde des scores)
- POO (classes Joueur et Partie)
- modules (un fichier par rôle)
- gestion des erreurs (try / except sur les saisies et les fichiers)
- pandas pour les données, numpy pour les tirages au hasard
