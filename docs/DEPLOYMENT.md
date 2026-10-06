# Déploiement et maintenance

## Architecture

```text
PDF officiels → extraction versionnée → cas et références
                                 ↓
                           runner Python → Ollama local
                                 ↓
                   réponses JSONL + manifeste figé
                                 ↓
                      export HTML/CSS/JS/JSON
                                 ↓
                          hébergement statique
```

L'interface ne lance pas d'inférence et ne communique pas avec Ollama. Son hébergement ne requiert pas de GPU. Aucun secret n'est nécessaire au site. Les coûts éventuels d'hébergement sont distincts du coût d'inférence local.

## Publication

Pour préparer le site à partir des résultats déjà présents dans un clone, exécuter `python3 scripts/preview_results.py`. Aucun moteur local ni téléchargement des rapports n'est nécessaire. Pour une nouvelle campagne locale, utiliser `python -m autoeval export --run data/runs/REMPLACER_PAR_RUN_ID --dest site`.

1. Sélectionner une campagne explicitement identifiée (mise au point ou pilote).
2. Exécuter les tests et vérifier le rapport comparatif.
3. Exporter sans `--include-documents`.
4. Inspecter le dossier exporté : pas de clé, pas de poids, pas de PDF intégral.
5. Publier les seuls fichiers de `site/` sur l'hébergement statique choisi.
6. Vérifier navigation, sources, téléchargement JSON et affichage mobile sur l'URL publiée.

Cette procédure est préparée mais aucun site public n'a été publié. Le serveur local de prévisualisation n'est pas un service de production.

## Maintenance

- Source modifiée : ne pas remplacer silencieusement ; créer une nouvelle entrée avec nouvelle empreinte et date, relire les références.
- Modèle mis à jour : nouvelle campagne, empreinte enregistrée. Un tag seul n'est pas une version immuable.
- Score corrigé : versionner le protocole et recalculer depuis les réponses brutes ; ne pas masquer les anciennes conditions.
- Erreur d'exécution : inspecter `results.jsonl`. Aucun retry automatique ; relancer dans une campagne distincte.
- Texte mal extrait : vérifier l'original. Le corpus actuel ne nécessite pas d'OCR ; les scans ne sont pas pris en charge.
- Ollama inaccessible : vérifier `/api/version` et le port. Le runner n'accepte que les adresses locales.
- Modèle manquant : le télécharger explicitement avant l'exécution ; ne pas compter un modèle non exécuté dans les résultats.

## Stockage

`.local/` contient le moteur et les poids téléchargés sur le poste de travail ; ce dossier est ignoré par Git. `data/runs/` conserve les campagnes brutes ; sauvegarder les campagnes choisies avant suppression. Le rapport est généré depuis les données figées de la campagne, pas depuis les références courantes susceptibles d'avoir changé.
