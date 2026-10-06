# Contribuer à AutoEval

Ce dépôt conserve un pilote expérimental. L'objectif d'une contribution est de rendre la méthode plus fiable, pas d'améliorer artificiellement un classement.

## Installation et contrôles

Suivre le [guide de reproduction](docs/REPRODUCIBILITY.md), puis exécuter :

```bash
python -m unittest discover -s tests -v
python scripts/preview_results.py --verify-only
node --check web/app.js
```

Node.js sert ici seulement à vérifier la syntaxe du JavaScript. Il n'est pas nécessaire à l'exécution du moteur ou à la consultation du site.

## Modifier une source ou un cas

1. Identifier la source, sa version, sa provenance et les conditions de réutilisation.
2. Préserver l'original et son empreinte ; ne jamais corriger silencieusement un document.
3. Documenter la tâche, les types attendus, les informations absentes et les erreurs critiques.
4. Ajouter les preuves, puis faire relire les références.
5. Affecter tous les cas d'une même campagne au même ensemble.
6. Versionner le protocole si les conditions ou la notation changent.

`scripts/seed_cases.py` est le script historique d'annotation initiale. Il **réécrit** les cas et le manifeste : ce n'est pas une commande d'installation ni un outil à relancer pour ajouter des données arbitraires.

## Préserver les résultats

Ne pas modifier `results/pilot-v0.1.json` pour remplacer des erreurs par de meilleures réponses. Créer un autre fichier et un autre rapport pour une nouvelle expérience. Une correction de calcul doit être expliquée, versionnée et recalculée à partir des réponses conservées.

Ne pas mettre dans Git les environnements virtuels, poids, clés, PDF intégraux ou sorties locales contenant les prompts complets. L'export public conserve des références et réponses, mais pas le corpus intégral.

## Décrire une modification

Expliquer le problème, le comportement obtenu, les vérifications exécutées et l'effet éventuel sur la comparabilité des résultats. Distinguer un changement d'interface d'un changement de protocole. Les tests doivent vérifier un comportement utile, en particulier les erreurs et cas limites.
