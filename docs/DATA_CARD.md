# Fiche de données

## Provenance

Documents publics hébergés par la NHTSA, soumis par les constructeurs. Catalogue : https://www.nhtsa.gov/nhtsa-datasets-and-apis

Les URL exactes et empreintes sont conservées dans `data/manifest.json`. Trois rapports, 17 pages, neuf cas. Collecte le 6 octobre 2026. Ce corpus initial contient des **rapports de rappel**, pas des plaintes de propriétaires : leur ajout n'est pas réalisé dans v0.1.

## Transformations

Téléchargement du PDF original ; extraction page par page avec pypdf 6.10.0 ; conservation du texte sans correction ; questions et annotations ajoutées séparément. Les faits, dates et anomalies ne sont ni générés ni altérés. Les rapports ont aussi été rendus et inspectés visuellement lors de la préparation.

L'extraction peut conserver les césures, espaces et sauts de ligne. Seuls Unicode, casse et espaces sont normalisés pour vérifier les citations. Les tableaux et les ruptures de page nécessitent une relecture.

## Cas délicats réels

- 24V-720 : pourcentage estimé différent de population potentiellement concernée ; recherche de cause encore en cours ; dates prévues de notification.
- 24V-436 : mises à jour datées de calendrier et distinctions entre groupes de véhicules. Ne pas substituer une ancienne date de tableau à une prévision plus récente dans le récit.
- 19V-627 : pourcentage non estimable ; chronologie complète renvoyée à une pièce jointe absente des quatre pages ; date de soumission postérieure à certains événements.

## Annotation

Préparée par l'assistant à partir des sources et vérifiée automatiquement pour les citations. Aucune double annotation humaine indépendante n'a encore eu lieu. Les valeurs de référence sont inspectables dans `data/cases.json`. Toute correction exige une nouvelle version et une réévaluation ; conserver les anciens résultats avec leur protocole d'origine.

## Réutilisation et publication

L'accès public n'est pas assimilé à une licence générale de redistribution. Les documents sont des soumissions de tiers : aucune déclaration générale de domaine public n'est faite. Les PDF et textes complets sont exclus du dépôt par défaut. Le dépôt fournit les URL et un script de récupération ; l'export public fournit les liens officiels et de courts passages justificatifs. Vérifier les conditions applicables avant toute redistribution élargie. La licence du code ne s'applique pas aux documents.

Ces documents comprennent des coordonnées professionnelles des constructeurs. Le benchmark ne collecte pas de VIN individuels ni de données personnelles de plaignants. Une future extension aux plaintes devra revoir le traitement des données personnelles.

## Usage

Recherche exploratoire et démonstration d'une méthode d'évaluation. Pas de diagnostic automobile, pas de recommandation actuelle à un propriétaire, pas de classement des constructeurs. Le nombre de véhicules rappelés ne permet pas de comparer leur fiabilité sans contexte et dénominateurs pertinents.
