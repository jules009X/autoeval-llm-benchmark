# Feuille de route

[Sommaire](README.md)

Les éléments non cochés sont des travaux à réaliser, pas des fonctionnalités disponibles.

## Base pilote

- [x] Rapports réels versionnés par empreinte.
- [x] Catalogue de neuf cas et séparation par campagne de rappel.
- [x] Deux modèles locaux et une baseline à règles.
- [x] Répétitions, réponses brutes, notation et métriques.
- [x] Rapport comparatif et interface statique.
- [x] Consultation des résultats publiés sans moteur ni corpus.
- [x] Documentation métier, technique et méthodologique.

## Priorité 1 — Solidifier l'évaluation

- [ ] Faire relire les annotations et documenter les désaccords.
- [ ] Élargir le corpus à davantage de campagnes indépendantes ; justifier la sélection par une matrice de couverture.
- [ ] Préparer des cas de développement et un nouvel ensemble final qui ne servent pas à ajuster les prompts.
- [ ] Évaluer les synthèses en aveugle avec une grille structurée.
- [ ] Conserver les fragments reçus avant une erreur de streaming et enregistrer tous les paramètres de transport.

Critère de passage : chaque référence finale dispose d'une trace de relecture ; les critères d'acceptation et le protocole sont figés avant l'exécution finale.

## Priorité 2 — Étudier les améliorations

- [ ] Comparer le format demandé par prompt à un JSON Schema contraint.
- [ ] Séparer plus explicitement exactitude factuelle et conformité de structure.
- [ ] Mesurer la pertinence des citations, pas seulement leur présence.
- [ ] Comparer modèles plus capables, règles et approches hybrides selon les ressources disponibles.
- [ ] Justifier d'éventuelles pondérations métier et vérifier leur sensibilité.

Critère de passage : les variantes sont identifiées, leurs résultats conservés séparément et leurs conclusions limitées aux cas testés.

## Priorité 3 — Présentation et usage

- [ ] Publier une démonstration sur un hébergement statique.
- [ ] Vérifier l'affichage et tous les liens sur l'URL publiée.
- [ ] Préparer une présentation d'entretien à partir des résultats validés.
- [ ] Documenter l'extension vers d’autres usages documentaires et techniques : données tabulaires, connaissances d'ingénierie ou tests de code.

Critère de passage : un lecteur extérieur peut installer, consulter les preuves et comprendre ce qui est évalué, sans accès à la machine d'origine.
