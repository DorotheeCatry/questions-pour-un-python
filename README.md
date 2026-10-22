# Questions pour un Python
**Un quiz d'histoire en console**

Petit jeu fait en Python pendant la game jam de la formation.

Le principe : à chaque tour, le jeu tire au hasard un type de question parmi trois, sur des grandes dates de l'histoire de France et du monde.

Le duel : deux événements, il faut trouver lequel s'est passé en premier
"Qu'est-ce qui s'est passé en premier : le Code noir ou la guerre de Sept Ans ?"
Avant ou après : le jeu donne la date d'un événement, il faut dire si le deuxième était avant ou après
"La Bastille a été prise le 14 juillet 1789. Le couronnement de Charlemagne, c'était avant ou après ?"
Le QCM : une question, quatre années proposées, une seule est juste
"En quelle année : chute du mur de Berlin ?"

Comme on ne sait jamais quelle question va tomber, ça évite que le jeu devienne répétitif.

On gagne des points à chaque bonne réponse (un peu plus pour le QCM), avec un bonus si on enchaîne. Au bout de 3 erreurs, la partie est finie.

> Projet réalisé en binôme : Sami Kabdani & Dorothée Catry

## Lancer le jeu

Il faut Python 3.10 ou plus.

```bash
pip install -r requirements.txt
python main.py
```

## Comment on joue

1. On entre son pseudo
2. On choisit un thème (histoire, villes de France, pays...)
3. On choisit la difficulté
   - facile : les deux valeurs sont très différentes
   - difficile : les valeurs sont proches, il faut vraiment savoir
4. Le jeu pose les questions en mélangeant les trois types
   - duel : on répond 1 ou 2
   - plus ou moins / avant ou après : on répond + ou -
   - QCM : on répond 1, 2, 3 ou 4
5. Après chaque réponse, le jeu affiche les vraies valeurs
6. A la fin, le score est enregistré et on voit le classement

## Structure du projet

```
questions-pour-un-python/
├── main.py            # menu et lancement du jeu
├── joueur.py          # classe Joueur
├── partie.py          # classe Partie (boucle de jeu, règles)
├── donnees.py         # chargement et préparation des CSV
├── scores.py          # sauvegarde des scores et statistiques
├── data/
│   ├── reperes_histoire.csv
│   └── ...            # les autres thèmes
├── scores.csv         # créé automatiquement à la première partie
├── requirements.txt
└── README.md
```

## Les données

| Thème | Source | Etat |
|---|---|---|
| Histoire | Repères officiels : Éduscol (voie pro, 2021), programme de primaire 2008 (BO hors-série du 19 juin 2008), liste brevet d'un collège de l'académie d'Amiens | fait |
| Villes de France | data.gouv.fr, "Communes et villes de France" (population INSEE) | à faire |
| Pays | Banque mondiale (population) | à faire |
| Vin | Douane, open data production de vins | bonus si le temps |

Chaque fichier garde une colonne `source` pour pouvoir vérifier une réponse.

Pour l'histoire, les dates avant J.-C. sont stockées en négatif (Alésia = -52). Les périodes (ex : Grande Guerre 1914-1918) ont une année de début et une année de fin, le jeu compare l'année de début.

## Organisation

On a découpé le projet en deux rôles qui peuvent avancer en même temps.

**SAMI : données et scores**
- `donnees.py`
- `scores.py`
- préparation des CSV

**Dorothée : moteur de jeu**
- `joueur.py`
- `partie.py`
- `main.py`

### Les "contrats" entre les deux rôles

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

- `main` doit toujours être jouable
- une branche par fonctionnalité : `feature/chargement-donnees`, `feature/classe-joueur`, `feature/boucle-partie`, `feature/scores`...
- à chaque relecture on vérifie le PEP 8 (avec flake8)
- messages de commit du type `feat: ...`, `fix: ...`, `docs: ...`

Le suivi des tâches est sur le tableau GitHub Projects (à faire / en cours / terminé), avec une étiquette par rôle.

## Planning

**Jour 1 matin**
- [x] création du dépôt et du README
- [x] CSV histoire (généré à partir de pdfs)

**Jour 1 après-midi**
- [x] Sami : chargement des thèmes et `tirer_duel`
- [ ] Dorothée : classes Joueur et Partie, avec seulement le duel pour commencer
- [x] Ensemble : première fusion
- [ ] Sami : ajout des questions avant/après et QCM
- [ ] Dorothée : scores et classement
- [ ] Sami : niveaux de difficulté

**Jour 2 matin**
- [ ] Dorothée : préparation de la démo

## Notions du cours utilisées

- variables, types, conditions, boucles (la boucle de jeu)
- fonctions
- listes et dictionnaires (les duels, les thèmes)
- fichiers (lecture des CSV, sauvegarde des scores)
- POO (classes Joueur et Partie)
- modules (un fichier par rôle)
- gestion des erreurs (try / except sur les saisies et les fichiers)
- pandas pour les données, numpy pour les tirages au hasard