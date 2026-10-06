# Validation et critères de qualité

[Sommaire](README.md)

## Contrôles automatisés

| Famille | Contrôles couverts |
|---|---|
| Corpus | Empreinte des PDF et textes, citations présentes, séparation des campagnes |
| Prompts | Exclusion des références attendues |
| Notation | Champs manquants, `null`, types numériques, JSON mal formé, champs supplémentaires |
| Preuves | Page inexistante, citation inventée, distinction entre présence et pertinence |
| Client | Réponse en streaming, flux inachevé, erreur moteur, URL locale uniquement |
| Statistiques | Échecs conservés dans les dénominateurs, répétitions distinguées des cas |
| Export | Rapport sans PDF, neutralisation des fermetures de balise HTML injectées |
| Résultats archivés | Agrégats recalculables, observations dupliquées refusées, prévisualisation hors ligne |

```bash
python3 scripts/preview_results.py --verify-only
python3 -m unittest discover -s tests -p test_saved_results.py -v
```

Ces deux commandes fonctionnent sur un clone sans corpus téléchargé. Pour la suite complète, préparer les PDF avant `python -m unittest discover -s tests -v`. La suite initiale comportait 19 tests ; quatre tests supplémentaires couvrent la consultation des résultats publiés.

## Vérifications effectuées localement

Installation dans un environnement Python vierge ; préparation et validation du corpus ; exécution réelle des deux LLM ; consultation de l'interface, des filtres, des réponses et des sources dans le navigateur. Le rapport du pilote distingue les réponses tronquées et les formats incorrects.

Le workflow GitHub est versionné dans `.github/workflows/test.yml`. Son existence ne prouve pas qu'une exécution distante a réussi : vérifier le statut dans l'onglet Actions après publication.

## Ce qui reste à vérifier

- Double annotation humaine et arbitrage des références.
- Fidélité, couverture et pertinence des citations dans les synthèses.
- Représentativité d'un corpus élargi, avec des campagnes indépendantes.
- Nouvel ensemble final après les ajustements motivés par ce pilote.
- Exécution sur d'autres environnements et vérification de l'URL après hébergement public.
- Débit sous charge, énergie, tests d'injection de prompt et robustesse sur PDF scannés.

## Règle de communication

Dire « les tests du logiciel passent » lorsque la suite l'atteste. Dire « les références sont validées par un expert » seulement après une relecture réellement réalisée et tracée. Les deux affirmations portent sur des objets différents.
