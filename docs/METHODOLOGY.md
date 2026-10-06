# Protocole v0.1

## Unités et séparation

Un document correspond à une version précise d'un rapport. Un cas associe ce document à une tâche et une grille. Une réponse est une exécution d'un modèle sur un cas. Trois tâches d'une campagne partagent le contexte et ne sont pas indépendantes.

24V-720 est réservé à la mise au point. 24V-436 et 19V-627 constituent un pilote distinct. Le pilote est trop petit pour une inférence statistique ou une généralisation métier. Après examen de ses erreurs, il devient une ressource de développement : une future évaluation finale exigera d'autres campagnes.

## Entrées et génération

Texte intégral des rapports, pages identifiées, consignes françaises, citations anglaises. Pas de recherche web ni RAG, pas de traduction des originaux. Mêmes tâches et enveloppe de sortie JSON pour les modèles. Les références et grilles ne sont pas transmises. Contexte maximum 16 384 tokens, sortie maximum 1 400 tokens, température 0,2, graines 41, 42, 43. La réflexion séparée est désactivée lorsque le modèle la prend en charge. Ce paramètre est une condition expérimentale, pas une équivalence entre architectures.

Les tags de modèles sont complétés par leurs empreintes et caractéristiques retournées par Ollama. Les modèles sont exécutés séquentiellement ; l'ordre est inversé à chaque répétition et les cas mélangés avec une graine fixe. Pas de nouvelle tentative automatique. Le temps de chargement est conservé ; aucun préchauffage séparé n'est effectué. Les caches et les conditions thermiques peuvent influencer les mesures.

## Notation automatique

Pour extraction et chronologie : exactitude = nombre de champs conformes / nombre de champs attendus. Comparaison exacte des nombres ; normalisation Unicode, casse et espaces des chaînes. Une quantité formatée comme chaîne est refusée lorsque le contrat demande un nombre. `null` est distinct de zéro et de chaîne vide. Un champ absent ne reçoit pas de crédit même si sa référence est `null`.

Format : objet JSON conforme aux clés demandées, sans champ supplémentaire. Citation : page existante et extrait d'au moins 12 caractères normalisés retrouvé dans cette page. La présence textuelle ne démontre pas l'implication sémantique ; cette dernière exige une relecture.

Erreurs critiques : champ marqué critique incorrect ou absent dans une réponse structurée analysable. Une réponse non analysable apparaît comme erreur de format ; il n'est pas possible d'attribuer une erreur sémantique précise. Les colonnes doivent être interprétées ensemble.

Acceptation automatique provisoire : format conforme, tous les champs corrects, toutes les citations retrouvées, aucune erreur critique. Cela n'est **pas une acceptation métier**, car les preuves peuvent être hors sujet.

Pour synthèse : format, longueur et présence des citations seulement. Aucun score de fidélité, couverture ou raisonnement automatique. Voir `HUMAN_REVIEW.md`.

## Agrégation

Comparaisons séparées par tâche et par campagne d'exécution. Les échecs d'exécution, réponses tronquées et JSON invalides valent zéro pour l'exactitude structurée agrégée. Les taux de format et d'échec incluent toutes les observations. La dispersion intra-cas est l'écart maximal-minimal d'exactitude entre répétitions, puis la moyenne de ces écarts. Aucun intervalle de confiance sur ce petit corpus.

La référence à règles extrait seulement les labels explicites de l'extraction ; elle s'abstient sur le fournisseur. Une seule exécution par cas suffit car elle est déterministe. Son périmètre limité est affiché et elle n'est pas intégrée à un classement global.

Une pondération globale n'est pas appliquée dans v0.1 : mélanger des scores structurés automatiques et des synthèses non relues serait trompeur. Après relecture, les poids par domaine devront être justifiés par un besoin métier et soumis à une analyse de sensibilité.

## Mesures

- Latence : durée murale du client, requête jusqu'à fin du flux.
- Premier contenu : durée jusqu'au premier fragment non vide. Approximation du TTFT, sans prétendre mesurer un token individuel.
- Vitesse : `eval_count / eval_duration` retournés par Ollama ; distinction avec durée murale.
- Tokens : compteurs natifs par modèle. Tokenisations différentes, pas d'équivalence token à token.
- Chargement : durée rapportée par le moteur, incluse dans la latence.
- Coût : API = 0 €, énergie/matériel = non mesurés. Ce n'est pas un coût total nul.
- Débit sous charge : non mesuré ; la campagne est séquentielle.

## Menaces sur la validité

Sélection manuelle et petit nombre de sources, textes publics potentiellement vus pendant l'entraînement, dépendance entre cas, absence d'experts annotateurs, contrôle limité des caches et de la température matérielle, contexte anglais et sortie française. Les noms, dates et versions des documents doivent accompagner toute communication des résultats.
