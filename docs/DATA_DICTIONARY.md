# Dictionnaire des données et résultats

[Sommaire](README.md)

## Sources et cas

`data/manifest.json` contient une liste `sources`. `id` identifie le fichier ; `campaign` identifie la campagne NHTSA ; `document_date` désigne la version du rapport et `retrieved_at` sa date de collecte. `sha256` contrôle les octets du PDF, `text_sha256` le JSON canonique du texte extrait. Ne pas confondre ces deux empreintes.

`data/cases.json` contient les tâches. `source_id` relie un cas à son rapport. `split` vaut `dev` ou `pilot`. `fields` décrit les sorties demandées au modèle, tandis que `expected` contient les corrigés et n'est jamais envoyé dans le prompt. Pour une synthèse, `rubric` remplace le corrigé champ par champ.

Une référence comprend `value`, `page`, `quote` et éventuellement `critical`. `null` signifie information absente dans le document fourni, et ne signifie ni zéro ni absence de problème dans le monde réel.

## Une observation d'exécution

| Clé | Signification |
|---|---|
| `run_id` | Campagne d'exécution ; distincte de la campagne de rappel automobile |
| `model` / `model_digest` | Tag et empreinte du modèle observé |
| `provider` | `ollama` ou `rules` |
| `case_id` / `task` | Cas et famille de tâche |
| `repeat` | Indice commençant à 0 ; l'interface affiche l'essai 1 pour l'indice 0 |
| `seed` | Graine de génération du LLM |
| `prompt_hash` | Empreinte du prompt complet ; le texte complet reste dans les campagnes locales |
| `raw_response` | Texte conservé ; peut être incomplet, erroné ou vide en cas d'erreur |
| `status` | `ok`, `truncated` ou `error` ; `ok` ne signifie pas « réponse correcte » |
| `done_reason` | Raison de fin retournée par le moteur, lorsqu'elle existe |
| `parameters` | Paramètres de génération conservés pour une réponse reçue |
| `score` | Résultats de contrôles automatiques, lorsqu'ils ont pu être calculés |

## Mesures techniques

| Clé de `metrics` | Unité / interprétation |
|---|---|
| `latency_s` | Secondes côté client, jusqu'à la fin de la réponse ou l'erreur |
| `first_content_chunk_s` | Secondes jusqu'au premier fragment non vide ; approximation du TTFT |
| `input_tokens` / `output_tokens` | Compteurs natifs du moteur, dépendants du tokenizer |
| `generation_tokens_per_s` | Tokens produits divisés par le temps de génération déclaré par le moteur |
| `load_s` | Temps de chargement rapporté par Ollama |
| `api_cost_eur` | Frais d'API : zéro pour cette exécution locale |
| `energy_cost_eur` | `null` : non mesuré ; ne pas afficher zéro |

Une clé absente signifie non disponible. La baseline n'a pas de tokenizer ni de premier token. Ses mesures ne doivent pas être comparées comme si elles provenaient d'un LLM.

## Notation et agrégats

`field_accuracy` est une fraction entre 0 et 1 pour les tâches structurées. Elle peut rester `null` lorsque la réponse n'est pas analysable ; lors de l'agrégation structurée, cette observation contribue alors pour zéro. Pour les synthèses, elle reste non applicable.

`quote_validity` mesure la présence textuelle des citations sur les pages annoncées ; elle ne mesure pas leur pertinence. `critical_errors` liste les champs critiques non conformes dans une réponse analysable. `quality_score` reste `null` : aucun score global de qualité sémantique n'est calculé.

`aggregates` regroupe les observations par modèle et tâche : `n` compte les réponses, `distinct_cases` les cas différents, `error_rate` les statuts autres que `ok`, `format_rate` les formats conformes parmi toutes les observations et `latency_median_s` la médiane des durées disponibles. `mean_repeat_range` est la moyenne des écarts max–min d'exactitude pour les cas répétés ; ce n'est pas un intervalle de confiance.

## Export publié

`results/pilot-v0.1.json` est une liste de deux campagnes d'exécution. Elle contient les sources, cas, réponses, scores, agrégats et environnement. Elle exclut les prompts complets et les documents intégraux. Le fichier suffit pour reconstruire la démonstration ; il ne suffit pas, seul, pour recalculer les citations sans récupérer les sources.
