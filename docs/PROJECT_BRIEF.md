# AutoEval — contexte et démarche du projet

**Projet personnel porté par APEDOH Senam Amenyo Jules, élève en dernière année d’école d’ingénieur.**

## Origine et intention

Je réalise AutoEval dans le cadre de ma préparation à un stage de fin d’études consacré à l’évaluation des modèles de langage. L’offre de stage Stellantis en benchmarking de LLM a orienté la question de départ : comment construire une évaluation utile aux équipes métier, au-delà d’une démonstration de génération de texte ?

Pour travailler sur des données réelles et accessibles, j’ai retenu les rapports publics de rappel automobile de la NHTSA. Le périmètre de ce pilote est l’analyse documentaire : extraire des faits, distinguer une prévision d’un événement et produire une synthèse sourcée. Les deux modèles sont exécutés localement afin de garder l’expérience accessible sans API payante.

Le projet est développé avec une assistance IA. Le dépôt rend visibles le protocole, le code, les sources et les résultats ; les annotations attendent encore une validation humaine indépendante. Il s’agit d’une initiative personnelle, sans mandat ni affiliation à Stellantis, et non d’un projet académique officiellement encadré annoncé comme tel.


## Objectif

Comparer des LLM sous contrainte d'exécution locale pour assister l'analyse de dossiers qualité automobile. La question est : sur ces documents, quels types d'erreurs les modèles commettent-ils, et quels contrôles sont nécessaires avant d'utiliser leurs réponses ?

Le besoin est une hypothèse de projet de candidature. Aucun entretien chez Stellantis ni validation par un expert automobile n'a été réalisé.

## Parties prenantes et catalogue

| Rôle envisagé | Usage | Sortie | Critères | Criticité |
|---|---|---|---|---|
| Analyste qualité | Extraire caractéristiques et volumes | Champs JSON avec preuves | Valeurs exactes, absence reconnue, citation pertinente | Élevée |
| Responsable de suivi | Séparer événements et prévisions | Dates normalisées et sources | Pas de prévision présentée comme réalisée | Élevée |
| Responsable de revue | Préparer une synthèse | 100–180 mots, citations | Fidélité, couverture, prudence, lisibilité | Élevée |

La taxonomie de chaque cas précise famille, complexité, contexte, langues, criticité et ensemble. Le périmètre couvre analyse documentaire, génération de contenu et extraction de connaissances. Il ne couvre pas le codage, un moteur de recherche documentaire complet ou les plannings de développement produit internes.

## Modèle standard de recueil des besoins

1. Quel utilisateur accomplit aujourd'hui cette tâche, avec quelle fréquence ?
2. Quels documents sont réellement disponibles et dans quelles versions ?
3. Quelle décision dépend de la réponse ?
4. Quels champs et faits sont indispensables ?
5. Que doit faire l'outil lorsque l'information manque ?
6. Quelles erreurs sont critiques, même si le reste de la réponse est correct ?
7. Quel délai est acceptable et quelle vérification humaine restera obligatoire ?
8. Qui peut valider les références, puis arbitrer les désaccords ?
9. Quel corpus représentatif sera réservé à l'évaluation ?

## Correspondance avec l'offre Stellantis

| Livrable demandé | Réalisation v0.1 | Limite |
|---|---|---|
| Catalogue | Fiches ci-dessus et cas JSON | Besoins supposés, pas d'ateliers réels |
| Taxonomie | Famille, complexité, contexte, langue, criticité | Trois familles seulement |
| Bibliothèque reproductible | PDF versionnés par empreinte, références et prompts | Trois dossiers |
| Cadre de notation | Contrôles automatiques et grille humaine | Validation humaine et score global non finalisés |
| Automatisation | Runner Ollama, répétitions, journalisation | Exécution séquentielle locale |
| Rapport comparatif | Export par tâche et réponse | Pas de conclusion industrielle |
| Visualisation | Interface statique navigable | Pas de lancement public d'inférence |
| Documentation | Installation, protocole, données, déploiement | Dépôt public ; démonstration hébergée à venir |
| Recommandations | Analyse des erreurs observées | Extension du corpus nécessaire avant sélection métier |

## Critères d'acceptation du logiciel

- Toutes les sources doivent être récupérables et correspondre aux empreintes figées.
- Chaque citation de référence doit exister sur la page déclarée.
- Les réponses attendues ne doivent jamais être fournies au modèle.
- Une campagne ne peut apparaître dans plusieurs ensembles.
- Les sorties erronées, tronquées ou absentes restent enregistrées et comptées.
- Les scores de l'interface doivent provenir des réponses conservées.
- Le rapport doit afficher explicitement les évaluations non réalisées.

## Étapes nécessaires avant une version de candidature aboutie

Étendre le corpus à davantage de campagnes indépendantes ; faire relire les références ; ajouter une évaluation humaine en aveugle des synthèses ; figer un nouvel ensemble final ; exécuter le protocole ; rédiger une recommandation limitée aux résultats ; héberger la démonstration (le dépôt est déjà public). Ne pas présenter ce premier pilote comme l'ensemble de ces étapes achevées.
