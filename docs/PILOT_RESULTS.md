# Rapport du pilote — 6 octobre 2026

Campagne : `20261006T180827Z-f6f92b`. Deux modèles locaux, six cas sur deux rapports, trois répétitions : **36 réponses de LLM**, auxquelles s’ajoutent deux sorties de règles. Les trois cas du rapport de mise au point sont analysés séparément.

## Résultats automatiques

| Modèle | Tâche | Réponses | Champs conformes | Format conforme | Échecs / troncatures | Latence médiane |
|---|---|---:|---:|---:|---:|---:|
| llama3.2:3b | chronology | 6 | 50.0 % | 50.0 % | 33.3 % | 19.09 s |
| llama3.2:3b | extraction | 6 | 63.3 % | 83.3 % | 0.0 % | 7.79 s |
| llama3.2:3b | synthesis | 6 | Non notée | 100.0 % | 0.0 % | 10.45 s |
| qwen3:1.7b | chronology | 6 | 40.0 % | 100.0 % | 0.0 % | 6.77 s |
| qwen3:1.7b | extraction | 6 | 0.0 % | 0.0 % | 0.0 % | 3.68 s |
| qwen3:1.7b | synthesis | 6 | Non notée | 100.0 % | 0.0 % | 6.97 s |
| regex-labels-v1 | extraction | 2 | 80.0 % | 100.0 % | 0.0 % | 0.00 s |

Le taux de champs conformes exige que le champ se trouve dans la structure demandée. Une bonne valeur placée dans une structure incorrecte ne reçoit pas de crédit. Ce score mesure la réussite du contrat de sortie, pas une exactitude sémantique indépendante du format. Une citation textuellement retrouvée n’est pas automatiquement pertinente.

## Observations vérifiables

- Qwen renvoie des valeurs directement sous `answers` dans les cas d’extraction, au lieu des objets `value/page/quote` demandés. Son score nul sur cette tâche reflète ce non-respect du contrat, même lorsque certaines valeurs sont justes.
- Dans la première réponse de Qwen à `24V436-timeline`, la date de début de production est confondue avec l’alerte initiale ; plusieurs dates ne suivent pas le format ISO et une valeur absente est rendue comme la chaîne `NR` plutôt que `null`.
- Llama produit deux réponses tronquées sur la chronologie du rapport 24V-436. Elles sont conservées et comptées comme échecs. La limite de sortie était identique pour les deux modèles.
- La méthode à règles atteint 80 % sur l’extraction : quatre champs étiquetés sur cinq, avec abstention sur le fournisseur. Cela ne démontre aucune aptitude de cette méthode à la synthèse ou à l’analyse temporelle.
- Les synthèses ont un format exploitable, mais leur fidélité et la pertinence de leurs citations n’ont pas fait l’objet d’une évaluation humaine indépendante. Aucun gagnant n’est désigné pour cette tâche.

## Recommandation limitée à ce pilote

Ne pas utiliser les sorties de ces deux configurations sans contrôle. Pour les champs explicitement étiquetés, commencer par une extraction déterministe et contrôler les exceptions. Pour les chronologies, imposer la distinction entre événements et prévisions et vérifier les passages cités. La comparaison actuelle évalue le respect d’un format demandé par prompt, sans décodage contraint par schéma.

Une prochaine expérience pourra comparer ce protocole à une sortie contrainte par JSON Schema, avec un prompt plus explicite. Elle devra utiliser une nouvelle version de protocole et de nouvelles campagnes finales, car les erreurs de ce pilote ont désormais été examinées. Les résultats présents ne seront ni remplacés ni présentés comme ceux de cette future expérience.

## Validation réalisée

- Empreintes des trois PDF, texte extrait et citations de référence vérifiés.
- 19 tests automatisés réussis : notation, cas limites, fuites entre ensembles, flux de réponses, agrégation et export.
- Installation standard dans un environnement Python vierge réussie ; commande installée `autoeval validate` vérifiée.
- Interface consultée dans le navigateur : navigation, filtres, réponses, références et sources.
- Frais d’API : 0 €. Énergie et amortissement non mesurés.
- Exécution GitHub Actions préparée mais non exécutée sur GitHub. Déploiement public non effectué.

## Limites

Deux rapports dans le pilote, choisis manuellement, ne permettent pas une conclusion sur un métier ou une marque. Les répétitions sont dépendantes et les mêmes documents peuvent être présents dans l’entraînement des modèles. La validation humaine des annotations et des synthèses reste à réaliser. Les rapports de rappel ne représentent pas la planification interne du développement produit.
