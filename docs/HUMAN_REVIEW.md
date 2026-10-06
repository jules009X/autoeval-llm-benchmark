# Protocole de relecture humaine — à exécuter

La v0.1 ne contient aucune note humaine. Les contrôles automatiques ne constituent pas une validation experte.

## Préparer les références

Relire chaque document et chaque champ attendu. Vérifier les pages, la distinction prévu/réalisé, les hypothèses et les informations absentes. Consigner le nom ou pseudonyme du relecteur, la date, le cas, le point discuté et la résolution. L'auteur de la première annotation ne doit pas être l'unique juge de sa propre référence.

## Évaluer les synthèses en aveugle

Masquer le modèle et randomiser l'ordre. Lire le document et appliquer les cinq critères factuels propres au cas dans `data/cases.json`. Pour chaque critère : 0 absent/incorrect, 1 partiel, 2 complet et fidèle. La couverture provisoire est la somme / 10.

Consigner séparément :

- Toute affirmation non appuyée ou contradiction avec le document, avec citation de la réponse et passage de référence.
- Les prévisions présentées comme des faits réalisés.
- La pertinence de chaque citation (étaye / n'étaye pas / ambigu).
- Lisibilité pour une revue qualité : 0 difficile, 1 exploitable avec réécriture, 2 directement lisible.
- Respect des réserves : 0 certitude injustifiée, 1 nuance partielle, 2 incertitude correctement formulée.

**Une erreur factuelle critique empêche l'acceptation, même si la couverture est élevée.** Ne pas ajouter mécaniquement toutes les dimensions : couverture, fidélité et pertinence se recouvrent partiellement.

## Trace à conserver

```json
{
  "run_id": "identifiant réel",
  "case_id": "identifiant réel",
  "model_digest": "empreinte réelle",
  "repeat": 0,
  "reviewer": "identifiant du relecteur",
  "reviewed_at": "date ISO",
  "rubric_points": [null, null, null, null, null],
  "critical_errors": [],
  "citation_assessments": [],
  "notes": ""
}
```

Les `null` indiquent une évaluation non effectuée, jamais zéro. Pour une version aboutie, faire noter un sous-ensemble commun par deux évaluateurs, analyser les désaccords et les arbitrer. N'annoncer un accord inter-évaluateurs que s'il a réellement été mesuré. L'intégration de ces notes dans l'application reste une extension, non implémentée dans cette version.
