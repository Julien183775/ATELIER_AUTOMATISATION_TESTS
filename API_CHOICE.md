# API Choice

* Étudiant : Julien VALADIER

* API choisie : CATAAS

* URL base : https://cataas.com

* Documentation officielle / README : https://cataas.com

* Auth : None (aucune authentification requise)

* Endpoints testés :

  * GET /cat → retourne une image de chat aléatoire
  * GET /cat/says/{text} → retourne une image avec texte personnalisé
  * GET /api/tags → retourne la liste des tags disponibles (JSON)
  * GET /api/cats?tags=cute&limit=5 → retourne une liste de chats filtrés (JSON)

* Hypothèses de contrat (champs attendus, types, codes) :

  * Code 200 → succès
  * Code 404 → ressource inexistante
  * Code 5xx → erreur serveur
  * Réponses :

    * image/jpeg ou image/png pour les endpoints /cat
    * application/json pour /api/tags et /api/cats
  * Exemple JSON attendu :

    * /api/tags → tableau de chaînes de caractères
    * /api/cats → tableau d’objets contenant au moins :

      * _id : string
      * tags : array

* Limites / rate limiting connu :

  * Aucun rate limiting documenté officiellement
  * API publique donc possible limitation implicite en cas de forte charge

* Risques (instabilité, downtime, CORS, etc.) :

  * API publique non garantie (risque de downtime)
  * Variabilité du temps de réponse
  * réponses parfois lentes ou erreurs 5xx possibles
  * CORS non garanti selon les sources
  * dépendance à un service externe non contrôlé
