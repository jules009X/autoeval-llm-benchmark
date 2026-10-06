# AutoEval — contexte et démarche du projet

**Projet personnel porté par APEDOH Senam Amenyo Jules, élève en dernière année d’école d’ingénieur.**

## De mon assistant PDF à l’évaluation des modèles

Mon premier assistant documentaire sur PDF combinait une recherche sémantique de passages et la génération de réponses avec Qwen2.5. Le mélange observé de passages concernant plusieurs villes a soulevé une question : comment évaluer la fiabilité des réponses au-delà de leur fluidité ?

AutoEval est mon projet personnel pour approfondir cette question. Je travaille ici sur un périmètre distinct et contrôlé : les documents sont fournis directement aux modèles ; le benchmark ne mesure pas une chaîne RAG complète. Je compare Qwen et Llama sur des tâches documentaires, en conservant leurs réponses, leurs erreurs et les mesures d’exécution.

## La mise en situation métier

J’ai choisi le scénario suivant : une équipe qualité automobile envisage un assistant pour préparer ses revues de dossiers de rappel. Elle veut extraire les caractéristiques des campagnes, distinguer les événements réalisés des actions prévues et obtenir une synthèse accompagnée de preuves.

Mon rôle dans cette mise en situation est de construire le banc d’essai avant le choix d’un modèle. Les besoins de l’équipe sont simulés ; les rapports publics NHTSA et les exécutions des modèles sont réels. Aucun client ni expert métier n’a validé ce scénario.

## Le lien avec ma formation SRI

Ce projet personnel prolonge les thèmes du syllabus SRI 2023–2025. Il ne constitue pas un livrable officiel de ces enseignements.

| Enseignement du syllabus | Ce que j’en prolonge dans AutoEval |
|---|---|
| Agents conversationnels (p. 41) | Métriques et méthodes d’évaluation ; analyse des performances des composants |
| Intégration IA et Interaction (p. 42) | Passage d’un besoin à une application et évaluation des composants intégrés |
| IA – Apprentissage automatique et apprentissage profond (p. 27) | Préparation des données et analyse des risques et limites des modèles |
| Ingénierie logicielle et système (p. 6) | Spécification, tests, validation et gestion des versions |
| Initiation à la recherche et TER 1 et 2 (p. 17 et 28) | Formulation d’un problème, prototypage, expérimentation et restitution critique |

Ces liens sont des prolongements méthodologiques : le syllabus ne décrit pas un cours consacré à ce benchmark de LLM. Mon objectif est de mobiliser ces acquis dans une étude personnelle que je peux expliquer et faire reproduire.

## Ce que je souhaite établir

Sur les documents retenus, quels types d’erreurs les modèles commettent-ils ? Respectent-ils les consignes de sortie ? Leurs citations existent-elles dans les sources ? Quels contrôles humains restent nécessaires ?

Le projet est développé avec une assistance IA. Les annotations doivent encore être validées indépendamment et la qualité sémantique des synthèses reste à évaluer. Les résultats actuels décrivent un petit pilote, pas une recommandation de déploiement industriel.

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

## Du scénario aux livrables

| Livrable du projet | Réalisation v0.1 | Limite |
|---|---|---|
| Catalogue | Fiches ci-dessus et cas JSON | Besoins supposés, pas d'ateliers réels |
| Taxonomie | Famille, complexité, contexte, langue, criticité | Trois familles seulement |
| Bibliothèque reproductible | PDF versionnés par empreinte, références et prompts | Trois dossiers |
| Cadre de notation | Contrôles automatiques et grille humaine | Validation humaine et score global non finalisés |
| Automatisation | Runner Ollama, répétitions, journalisation | Exécution séquentielle locale |
| Rapport comparatif | Export par tâche et réponse | Pas de conclusion industrielle |
| Visualisation | Interface statique navigable | Pas de lancement public d'inférence |
| Documentation | Installation, protocole, données, déploiement | Dépôt public et démonstration sur GitHub Pages |
| Recommandations | Analyse des erreurs observées | Extension du corpus nécessaire avant sélection métier |

## Critères d'acceptation du logiciel

- Toutes les sources doivent être récupérables et correspondre aux empreintes figées.
- Chaque citation de référence doit exister sur la page déclarée.
- Les réponses attendues ne doivent jamais être fournies au modèle.
- Une campagne ne peut apparaître dans plusieurs ensembles.
- Les sorties erronées, tronquées ou absentes restent enregistrées et comptées.
- Les scores de l'interface doivent provenir des réponses conservées.
- Le rapport doit afficher explicitement les évaluations non réalisées.

## Ce que je souhaite approfondir

Étendre le corpus à davantage de campagnes indépendantes ; faire relire les références ; ajouter une évaluation humaine en aveugle des synthèses ; figer un nouvel ensemble final ; exécuter le protocole ; rédiger une recommandation limitée aux résultats ; maintenir le dépôt et la démonstration publique. Ne pas présenter ce premier pilote comme l'ensemble de ces étapes achevées.
