# Reproduire et examiner une expérience

[Sommaire](README.md)

## Trois niveaux de vérification

| Niveau | Commande / action | Ce que cela établit |
|---|---|---|
| Résultats publiés | `python3 scripts/preview_results.py --verify-only` | Les agrégats correspondent aux observations de l'export |
| Corpus et code | Collecte, `python -m autoeval validate`, tests | Les versions de documents, références et fonctions passent les contrôles |
| Nouvelle inférence | `python -m autoeval run ...` | Les modèles ont réellement été exécutés dans de nouvelles conditions enregistrées |

Aucun de ces niveaux ne remplace une validation humaine indépendante des corrigés.

## Environnement de l'expérience publiée

- Machine : Apple M3 Pro, 18 Gio de mémoire unifiée.
- Python : 3.12.6 ; extraction : pypdf 6.10.0.
- Ollama : 0.35.1.
- Modèles et empreintes exactes : [models.lock.json](../data/models.lock.json).
- Corpus : [manifest.json](../data/manifest.json).
- Code Python du moteur ayant produit le pilote : [software-manifest.json](../data/software-manifest.json).
- Mise au point : `20261006T180124Z-ec286f` ; pilote : `20261006T180827Z-f6f92b`.

Les identifiants utilisent UTC. Le lancement du pilote correspond au 6 octobre 2026 à 20:08:27 à Paris. Les tags de modèles peuvent évoluer : comparer les empreintes enregistrées, pas seulement les noms. Un autre matériel ou moteur peut produire d'autres réponses et temps.

## Préparer depuis un clone

Exécuter les commandes à la racine du dépôt. Les exemples ciblent macOS/Linux ; Windows n'a pas été testé.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install '.[corpus]'
python scripts/prepare_corpus.py
python -m autoeval validate
python -m unittest discover -s tests -v
```

La préparation télécharge uniquement trois PDF et refuse une version différente. Ne pas désactiver le contrôle d'empreinte pour faire passer la commande : un rapport modifié exige une nouvelle version de corpus et la relecture des références.

## Lancer le moteur local

Installer Ollama depuis [le site officiel](https://ollama.com/download). S'il n'est pas déjà démarré, lancer dans un terminal séparé :

```bash
OLLAMA_NO_CLOUD=1 ollama serve
```

Puis télécharger explicitement les deux modèles :

```bash
ollama pull qwen3:1.7b
ollama pull llama3.2:3b
```

Le runner ne télécharge pas automatiquement de poids. Il utilise par défaut `http://127.0.0.1:11434`. Le Mac ayant servi au pilote utilisait le port `11439`, une copie locale du moteur et `OLLAMA_MAX_LOADED_MODELS=1`. Ce détail explique les commandes historiques ; il n'est pas nécessaire pour consulter l'export publié.

## Paramètres du pilote

| Paramètre | Valeur |
|---|---|
| Entrée | Rapport entier, avec numéros de page |
| Langues | Documents anglais, consignes et explications françaises |
| Sortie | JSON demandé, sans JSON Schema contraignant |
| Température | 0,2 |
| Graines | 41, 42 et 43 |
| Contexte maximal | 16 384 tokens |
| Sortie maximale | 1 400 tokens |
| Réflexion séparée | Désactivée pour Qwen, qui expose cette capacité |
| Répétitions | 3 par modèle et cas |
| Timeout pilote | 300 secondes ; défaut du CLI : 180 secondes |
| Ordre | Séquentiel ; ordre des modèles alterné ; cas mélangés avec graine fixe |
| Relance automatique | Aucune |

```bash
python -m autoeval run --model qwen3:1.7b --split dev --baseline
python -m autoeval run --model qwen3:1.7b --model llama3.2:3b --split pilot --repeats 3 --baseline --timeout 300
```

Ajouter `--base-url http://127.0.0.1:11439` seulement si le serveur écoute sur ce port. Les commandes créent de nouveaux identifiants ; elles ne remplacent pas le pilote publié.

## Conserver et exporter

Chaque campagne locale possède un `manifest.json` et un `results.jsonl`. Le manifeste fige les cas et le texte utilisé ; les lignes de réponse conservent les prompts complets lorsque la requête a été préparée, les paramètres disponibles, le texte et les erreurs.

```bash
python -m autoeval export --run data/runs/REMPLACER_PAR_RUN_ID --dest site
```

On peut répéter `--run` pour comparer visuellement plusieurs campagnes sans les fusionner. L'interface les présente dans un sélecteur distinct. Le dossier `data/runs/` est ignoré par Git : le sauvegarder séparément avant tout nettoyage.

## Dépannage

| Symptôme | Vérification / action |
|---|---|
| `Local model not installed` | Comparer le tag demandé à `ollama list`, puis télécharger explicitement le bon tag |
| Connexion refusée | Vérifier `ollama serve` et le port ; ne pas remplacer l'URL par une API cloud |
| Empreinte PDF différente | La source ou le fichier local a changé ; préserver l'ancienne version et examiner la nouvelle |
| Extraction différente | Vérifier pypdf 6.10.0 et le PDF original |
| Module `pypdf` absent | Réactiver `.venv`, puis installer `.[corpus]` |
| Commande installée après modification du code | Réinstaller le paquet ; les exemples `python -m autoeval` depuis le dépôt utilisent le code du dépôt |
| `truncated` | La limite de sortie a été atteinte ; ne pas présenter la réponse comme complète |
| `prediction aborted` | Erreur du moteur conservée dans la campagne ; ne pas la supprimer du dénominateur |
| JSON correct mais score nul | Vérifier le contrat imbriqué `answers → champ → value/page/quote` et les types |
| Port 8080 occupé | Utiliser un autre port dans `http.server`, puis ouvrir l'URL correspondante |

## Limites de reproduction

Une graine fixe ne garantit pas une sortie identique entre matériels ou moteurs. Les caches, le chargement, la quantification et la température matérielle peuvent modifier les temps. Le timeout et certains paramètres de transport du pilote sont documentés ici mais ne sont pas tous stockés explicitement dans le manifeste v0.1 ; améliorer cet enregistrement fait partie de la feuille de route.
