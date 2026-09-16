"""Définitions d'outils MCP réalistes — version 'naïve' (celle qu'on écrit spontanément)."""

TOOLS = [
# ---------------- CANON (12 outils) ----------------
{
 "name": "canon_get_entity",
 "description": "Récupère la fiche complète d'une entité du canon (personnage, lieu, faction, objet, événement, concept) à partir de son identifiant unique. Renvoie tous les champs typés de l'entité, ses relations sortantes et entrantes, ses périodes de validité, et la provenance de chaque fait (scène ou chapitre qui l'a produit). Utiliser cet outil quand on connaît déjà l'identifiant exact de l'entité recherchée.",
 "inputSchema": {"type":"object","properties":{
   "entity_id":{"type":"string","description":"Identifiant unique de l'entité, au format uuid v4."},
   "include_relations":{"type":"boolean","description":"Si vrai, inclut la liste complète des relations sortantes et entrantes. Par défaut vrai.","default":True},
   "include_provenance":{"type":"boolean","description":"Si vrai, inclut pour chaque fait la scène source et l'horodatage d'enregistrement. Par défaut faux.","default":False},
   "as_of":{"type":"string","description":"Date interne à la fiction (ISO 8601 ou expression relative). Si fournie, ne renvoie que les faits valides à cette date."},
   "known_by":{"type":"string","description":"Identifiant d'un personnage. Si fourni, filtre les faits pour ne renvoyer que ceux que ce personnage connaît à la date demandée."}
 },"required":["entity_id"]}
},
{
 "name": "canon_search",
 "description": "Recherche des entités dans le canon par similarité sémantique, par mots-clés, ou les deux combinés. Permet de filtrer par type d'entité, par faction d'appartenance, par période de validité et par tags. Renvoie une liste d'entités classées par pertinence avec un extrait de leur description. Utiliser cet outil quand on ne connaît pas l'identifiant exact et qu'on cherche par description.",
 "inputSchema": {"type":"object","properties":{
   "query":{"type":"string","description":"Texte de recherche en langage naturel."},
   "entity_types":{"type":"array","items":{"type":"string","enum":["personnage","lieu","faction","objet","evenement","concept"]},"description":"Restreint la recherche à certains types d'entités."},
   "faction_id":{"type":"string","description":"Restreint aux entités liées à cette faction."},
   "mode":{"type":"string","enum":["semantique","mots_cles","hybride"],"description":"Mode de recherche. Hybride par défaut.","default":"hybride"},
   "limit":{"type":"integer","description":"Nombre maximum de résultats. Par défaut 10, maximum 50.","default":10},
   "as_of":{"type":"string","description":"Date interne à la fiction pour filtrer les faits valides."}
 },"required":["query"]}
},
{
 "name": "canon_list_relations",
 "description": "Liste toutes les relations d'une entité donnée, avec leur type (allié, ennemi, parent, membre de, situé à, possède, a tué, connaît), leur direction, leur période de validité et leur force. Permet d'explorer le graphe du monde à partir d'un point de départ, sur une ou plusieurs profondeurs.",
 "inputSchema": {"type":"object","properties":{
   "entity_id":{"type":"string","description":"Identifiant de l'entité de départ."},
   "relation_types":{"type":"array","items":{"type":"string"},"description":"Restreint aux types de relations indiqués."},
   "direction":{"type":"string","enum":["sortante","entrante","les_deux"],"description":"Direction des relations à renvoyer.","default":"les_deux"},
   "depth":{"type":"integer","description":"Profondeur d'exploration du graphe. 1 = voisins directs. Maximum 3.","default":1},
   "as_of":{"type":"string","description":"Date interne à la fiction pour filtrer les relations valides."}
 },"required":["entity_id"]}
},
{
 "name": "canon_propose_fact",
 "description": "Propose un nouveau fait ou une nouvelle entité au canon. Le fait n'est PAS enregistré immédiatement : il entre en statut 'en attente d'audit' et doit passer la relecture avant d'être validé. Renvoie un identifiant de proposition et la liste des vérifications attendues.",
 "inputSchema": {"type":"object","properties":{
   "entity_type":{"type":"string","enum":["personnage","lieu","faction","objet","evenement","concept"],"description":"Type de l'entité concernée."},
   "entity_id":{"type":"string","description":"Identifiant de l'entité si elle existe déjà. Omettre pour créer une nouvelle entité."},
   "payload":{"type":"object","description":"Contenu du fait, conforme au schéma du type d'entité concerné."},
   "valid_from":{"type":"string","description":"Début de validité dans la chronologie interne de la fiction."},
   "valid_to":{"type":"string","description":"Fin de validité dans la chronologie interne. Omettre si le fait est toujours vrai."},
   "revealed_at":{"type":"string","description":"Moment du récit où cette information est révélée au lecteur, si différent du moment où elle devient vraie."},
   "source_scene":{"type":"string","description":"Identifiant de la scène ou du chapitre qui produit ce fait."},
   "confidence":{"type":"string","enum":["certain","probable","rumeur"],"description":"Niveau de certitude du fait dans l'univers.","default":"certain"}
 },"required":["entity_type","payload"]}
},
{
 "name": "canon_commit",
 "description": "Valide définitivement une proposition qui a passé l'audit et l'inscrit dans le canon. Applique les contraintes structurelles et les règles de domaine, ferme les périodes de validité des faits contredits, et renvoie le résultat de la validation. Peut refuser la proposition si une règle est violée.",
 "inputSchema": {"type":"object","properties":{
   "proposal_id":{"type":"string","description":"Identifiant de la proposition à valider."},
   "audit_results":{"type":"array","items":{"type":"object"},"description":"Résultats des relecteurs, requis pour la validation."},
   "force":{"type":"boolean","description":"Ignore les avertissements non bloquants. N'ignore jamais les contraintes dures.","default":False}
 },"required":["proposal_id","audit_results"]}
},
{
 "name": "canon_list_contradictions",
 "description": "Liste les contradictions détectées dans le canon, ouvertes ou résolues. Chaque contradiction indique les faits en conflit, la règle ou l'analyse qui l'a détectée, sa gravité, et les résolutions possibles. Permet de filtrer par entité, par gravité et par statut.",
 "inputSchema": {"type":"object","properties":{
   "entity_id":{"type":"string","description":"Restreint aux contradictions impliquant cette entité."},
   "severity":{"type":"string","enum":["bloquante","majeure","mineure"],"description":"Filtre par gravité."},
   "status":{"type":"string","enum":["ouverte","resolue","ignoree"],"description":"Filtre par statut.","default":"ouverte"},
   "limit":{"type":"integer","description":"Nombre maximum de résultats.","default":20}
 },"required":[]}
},
{
 "name": "canon_resolve_contradiction",
 "description": "Résout une contradiction en indiquant quel fait fait autorité et quel fait doit voir sa période de validité fermée ou être marqué comme rumeur. Enregistre la décision et sa justification.",
 "inputSchema": {"type":"object","properties":{
   "contradiction_id":{"type":"string","description":"Identifiant de la contradiction."},
   "keep_fact_id":{"type":"string","description":"Identifiant du fait qui fait autorité."},
   "action":{"type":"string","enum":["fermer_validite","marquer_rumeur","supprimer","ignorer"],"description":"Action à appliquer au fait perdant."},
   "justification":{"type":"string","description":"Explication de la décision, conservée dans l'historique."}
 },"required":["contradiction_id","keep_fact_id","action"]}
},
{
 "name": "canon_get_schema",
 "description": "Renvoie le schéma d'un type d'entité : ses champs obligatoires et facultatifs, leurs types, les relations autorisées et les contraintes qui s'y appliquent. À consulter avant de proposer un fait pour un type d'entité peu familier.",
 "inputSchema": {"type":"object","properties":{
   "entity_type":{"type":"string","enum":["personnage","lieu","faction","objet","evenement","concept"],"description":"Type dont on veut le schéma."}
 },"required":["entity_type"]}
},
{
 "name": "canon_get_knowledge",
 "description": "Renvoie ce qu'un personnage donné sait, croit à tort, ou ignore, à un moment donné du récit. Distingue la vérité objective de la croyance subjective. Indispensable pour écrire des scènes cohérentes avec l'asymétrie d'information entre personnages.",
 "inputSchema": {"type":"object","properties":{
   "character_id":{"type":"string","description":"Identifiant du personnage."},
   "as_of":{"type":"string","description":"Moment du récit."},
   "about_entity_id":{"type":"string","description":"Restreint à ce que le personnage sait d'une entité précise."},
   "include_false_beliefs":{"type":"boolean","description":"Inclut les croyances erronées du personnage.","default":True}
 },"required":["character_id","as_of"]}
},
{
 "name": "canon_timeline",
 "description": "Renvoie la chronologie des événements du canon, ordonnée par date interne ou par ordre de révélation au lecteur. Permet de filtrer par entité impliquée, par lieu, par faction et par fenêtre temporelle.",
 "inputSchema": {"type":"object","properties":{
   "order":{"type":"string","enum":["chronologique","revelation"],"description":"Ordre de tri des événements.","default":"chronologique"},
   "entity_id":{"type":"string","description":"Restreint aux événements impliquant cette entité."},
   "from":{"type":"string","description":"Début de la fenêtre temporelle."},
   "to":{"type":"string","description":"Fin de la fenêtre temporelle."},
   "limit":{"type":"integer","description":"Nombre maximum d'événements.","default":50}
 },"required":[]}
},
{
 "name": "canon_create_branch",
 "description": "Crée une branche du canon pour explorer une continuité alternative sans toucher à la version principale. La branche est une copie logique : les faits communs ne sont pas dupliqués. Permet de comparer et de fusionner ensuite.",
 "inputSchema": {"type":"object","properties":{
   "name":{"type":"string","description":"Nom de la branche."},
   "from_branch":{"type":"string","description":"Branche de départ. Par défaut la principale.","default":"principale"},
   "description":{"type":"string","description":"Ce que cette branche explore."}
 },"required":["name"]}
},
{
 "name": "canon_diff_branches",
 "description": "Compare deux branches du canon et renvoie la liste des entités et faits qui diffèrent, avec le détail des divergences.",
 "inputSchema": {"type":"object","properties":{
   "branch_a":{"type":"string","description":"Première branche."},
   "branch_b":{"type":"string","description":"Deuxième branche."},
   "entity_types":{"type":"array","items":{"type":"string"},"description":"Restreint la comparaison à certains types."}
 },"required":["branch_a","branch_b"]}
},

# ---------------- FILE DES TRAVAUX (6 outils) ----------------
{
 "name": "jobs_enqueue",
 "description": "Dépose un nouveau travail sur la file d'attente. Le travail sera pris en charge par une machine disponible, qui sera réveillée si nécessaire. Renvoie un identifiant de travail permettant d'en suivre l'avancement. Ne bloque pas : l'appel revient immédiatement.",
 "inputSchema": {"type":"object","properties":{
   "job_type":{"type":"string","enum":["image","lora_image","mesh_3d","retopo","texture","voix","musique","ambiance","export_unreal"],"description":"Type de travail à exécuter."},
   "recipe":{"type":"string","description":"Identifiant de la recette figée à appliquer, avec sa version."},
   "params":{"type":"object","description":"Paramètres à injecter dans la recette. Doivent correspondre au schéma de la recette."},
   "priority":{"type":"string","enum":["basse","normale","haute"],"description":"Priorité dans la file.","default":"normale"},
   "linked_entity_id":{"type":"string","description":"Entité du canon à laquelle rattacher le résultat."},
   "callback":{"type":"string","description":"URL à appeler à la fin du travail."}
 },"required":["job_type","recipe","params"]}
},
{
 "name": "jobs_status",
 "description": "Renvoie l'état d'un travail : en attente, en cours, terminé, échoué, annulé. Inclut l'avancement en pourcentage quand il est disponible, la machine qui l'exécute, la durée écoulée et l'estimation de temps restant.",
 "inputSchema": {"type":"object","properties":{
   "job_id":{"type":"string","description":"Identifiant du travail."},
   "include_logs":{"type":"boolean","description":"Inclut les dernières lignes de log.","default":False}
 },"required":["job_id"]}
},
{
 "name": "jobs_list",
 "description": "Liste les travaux de la file, filtrables par statut, par type, par entité liée et par fenêtre de temps. Permet de voir ce qui attend, ce qui tourne et ce qui a échoué récemment.",
 "inputSchema": {"type":"object","properties":{
   "status":{"type":"array","items":{"type":"string","enum":["attente","en_cours","termine","echoue","annule"]},"description":"Filtre par statut."},
   "job_type":{"type":"string","description":"Filtre par type de travail."},
   "linked_entity_id":{"type":"string","description":"Filtre par entité liée."},
   "limit":{"type":"integer","description":"Nombre maximum de résultats.","default":20}
 },"required":[]}
},
{
 "name": "jobs_cancel",
 "description": "Annule un travail en attente ou en cours. Un travail en cours est interrompu proprement et ses résultats partiels sont conservés quand c'est possible.",
 "inputSchema": {"type":"object","properties":{
   "job_id":{"type":"string","description":"Identifiant du travail à annuler."},
   "reason":{"type":"string","description":"Motif de l'annulation, conservé dans l'historique."}
 },"required":["job_id"]}
},
{
 "name": "jobs_result",
 "description": "Récupère le résultat d'un travail terminé : chemins des fichiers produits, métadonnées, coût en temps de calcul. Ne fonctionne que sur les travaux dont le statut est terminé.",
 "inputSchema": {"type":"object","properties":{
   "job_id":{"type":"string","description":"Identifiant du travail."}
 },"required":["job_id"]}
},
{
 "name": "jobs_list_recipes",
 "description": "Liste les recettes disponibles pour un type de travail donné, avec leur version, leur description et le schéma des paramètres qu'elles attendent. À consulter avant de déposer un travail d'un type peu familier.",
 "inputSchema": {"type":"object","properties":{
   "job_type":{"type":"string","description":"Type de travail dont on veut les recettes."}
 },"required":[]}
},

# ---------------- IMAGES (7 outils) ----------------
{
 "name": "image_generate",
 "description": "Lance une génération d'image via une recette figée. Raccourci qui dépose un travail de type image sur la file et renvoie son identifiant. Le style d'un personnage est appliqué automatiquement si l'entité liée en possède un.",
 "inputSchema": {"type":"object","properties":{
   "recipe":{"type":"string","enum":["portrait_v3","turnaround_v2","environnement_v4","prop_v1","moodboard_v2","illustration_promo_v1"],"description":"Recette de génération à utiliser."},
   "prompt":{"type":"string","description":"Description visuelle. La fiche de style canonique est ajoutée automatiquement."},
   "negative_prompt":{"type":"string","description":"Éléments à éviter."},
   "linked_entity_id":{"type":"string","description":"Entité du canon concernée. Déclenche l'application de son style."},
   "reference_images":{"type":"array","items":{"type":"string"},"description":"Identifiants d'images de référence pour le conditionnement."},
   "variants":{"type":"integer","description":"Nombre de variantes à produire.","default":4},
   "seed":{"type":"integer","description":"Graine aléatoire pour la reproductibilité."}
 },"required":["recipe","prompt"]}
},
{
 "name": "image_train_style",
 "description": "Entraîne un style réutilisable (LoRA) à partir d'images validées, pour qu'un personnage, un lieu ou une esthétique devienne reconnaissable dans toutes les générations futures. Nécessite au minimum quinze images validées. L'entraînement dure environ vingt minutes.",
 "inputSchema": {"type":"object","properties":{
   "linked_entity_id":{"type":"string","description":"Entité du canon dont on entraîne le style."},
   "image_ids":{"type":"array","items":{"type":"string"},"description":"Identifiants des images validées servant de base."},
   "style_name":{"type":"string","description":"Nom du style, servira de déclencheur dans les prompts."},
   "base_model":{"type":"string","description":"Modèle de base sur lequel entraîner."},
   "steps":{"type":"integer","description":"Nombre d'étapes d'entraînement.","default":1500}
 },"required":["linked_entity_id","image_ids","style_name"]}
},
{
 "name": "image_list_styles",
 "description": "Liste les styles entraînés disponibles, avec l'entité à laquelle chacun est rattaché, la date d'entraînement, le nombre d'images sources et le modèle de base.",
 "inputSchema": {"type":"object","properties":{
   "linked_entity_id":{"type":"string","description":"Filtre par entité."},
   "base_model":{"type":"string","description":"Filtre par modèle de base."}
 },"required":[]}
},
{
 "name": "image_get",
 "description": "Récupère une image produite et ses métadonnées : recette utilisée, paramètres, graine, entité liée, statut de validation.",
 "inputSchema": {"type":"object","properties":{
   "image_id":{"type":"string","description":"Identifiant de l'image."}
 },"required":["image_id"]}
},
{
 "name": "image_list",
 "description": "Liste les images produites, filtrables par entité liée, par recette, par statut de validation et par période.",
 "inputSchema": {"type":"object","properties":{
   "linked_entity_id":{"type":"string","description":"Filtre par entité."},
   "recipe":{"type":"string","description":"Filtre par recette."},
   "validated":{"type":"boolean","description":"Ne renvoie que les images validées ou non validées."},
   "limit":{"type":"integer","description":"Nombre maximum de résultats.","default":20}
 },"required":[]}
},
{
 "name": "image_validate",
 "description": "Marque une image comme validée par l'humain. Les images validées deviennent éligibles à l'entraînement d'un style et sont rattachées durablement à leur entité.",
 "inputSchema": {"type":"object","properties":{
   "image_id":{"type":"string","description":"Identifiant de l'image."},
   "note":{"type":"string","description":"Commentaire sur la validation."}
 },"required":["image_id"]}
},
{
 "name": "image_describe",
 "description": "Analyse une image existante avec un modèle de vision et renvoie une description structurée : sujet, composition, palette, éléments notables. Sert à vérifier qu'une image générée correspond à la fiche canonique.",
 "inputSchema": {"type":"object","properties":{
   "image_id":{"type":"string","description":"Identifiant de l'image à analyser."},
   "compare_to_entity_id":{"type":"string","description":"Si fourni, compare l'image à la fiche de cette entité et signale les écarts."}
 },"required":["image_id"]}
},

# ---------------- 3D (8 outils) ----------------
{
 "name": "mesh_generate",
 "description": "Génère un maillage 3D à partir d'une ou plusieurs images de référence. Utilise le modèle local pour l'itération rapide ou un service distant pour la qualité. Le résultat est un maillage brut, non nettoyé, sans topologie exploitable pour l'animation.",
 "inputSchema": {"type":"object","properties":{
   "reference_image_ids":{"type":"array","items":{"type":"string"},"description":"Images de référence, une ou plusieurs vues."},
   "engine":{"type":"string","enum":["local_rapide","local_qualite","distant_qualite"],"description":"Moteur de génération.","default":"local_rapide"},
   "linked_entity_id":{"type":"string","description":"Entité du canon concernée."},
   "target_faces":{"type":"integer","description":"Nombre de faces visé."},
   "with_texture":{"type":"boolean","description":"Génère aussi les textures PBR.","default":True}
 },"required":["reference_image_ids"]}
},
{
 "name": "blender_open",
 "description": "Ouvre un fichier Blender ou importe un maillage dans une nouvelle scène, et renvoie un identifiant de session permettant d'enchaîner les opérations suivantes.",
 "inputSchema": {"type":"object","properties":{
   "file_path":{"type":"string","description":"Chemin du fichier à ouvrir."},
   "import_mesh_id":{"type":"string","description":"Identifiant d'un maillage produit à importer."}
 },"required":[]}
},
{
 "name": "blender_run",
 "description": "Exécute une opération Blender dans une session ouverte : remaillage quad, décimation, dépliage UV, nettoyage de géométrie, application de modificateurs. Renvoie le résultat et les statistiques du maillage.",
 "inputSchema": {"type":"object","properties":{
   "session_id":{"type":"string","description":"Identifiant de la session Blender."},
   "operation":{"type":"string","enum":["remaillage_quad","decimation","depliage_uv","nettoyage","appliquer_modificateurs","lissage_normales"],"description":"Opération à exécuter."},
   "params":{"type":"object","description":"Paramètres de l'opération."}
 },"required":["session_id","operation"]}
},
{
 "name": "blender_bake",
 "description": "Cuit les cartes de texture d'un maillage : normales, occlusion ambiante, courbure, transfert du haute densité vers le basse densité. Renvoie les chemins des cartes produites.",
 "inputSchema": {"type":"object","properties":{
   "session_id":{"type":"string","description":"Identifiant de la session Blender."},
   "maps":{"type":"array","items":{"type":"string","enum":["normale","occlusion","courbure","hauteur","rugosite"]},"description":"Cartes à produire."},
   "resolution":{"type":"integer","description":"Résolution des cartes en pixels.","default":2048},
   "high_poly_id":{"type":"string","description":"Maillage haute densité source pour le transfert."}
 },"required":["session_id","maps"]}
},
{
 "name": "blender_screenshot",
 "description": "Capture la vue actuelle de la session Blender et renvoie une image. Indispensable après chaque opération : sans retour visuel, un agent exécute des opérations valides mais fausses sans que rien ne le signale.",
 "inputSchema": {"type":"object","properties":{
   "session_id":{"type":"string","description":"Identifiant de la session."},
   "view":{"type":"string","enum":["face","profil","dessus","perspective","wireframe"],"description":"Angle de vue.","default":"perspective"}
 },"required":["session_id"]}
},
{
 "name": "blender_export",
 "description": "Exporte le maillage de la session vers un format d'échange, avec ses textures. Le format glTF est préféré pour la fidélité des matériaux PBR.",
 "inputSchema": {"type":"object","properties":{
   "session_id":{"type":"string","description":"Identifiant de la session."},
   "format":{"type":"string","enum":["gltf","fbx","obj","usd"],"description":"Format d'export.","default":"gltf"},
   "include_textures":{"type":"boolean","description":"Inclut les textures.","default":True},
   "linked_entity_id":{"type":"string","description":"Entité du canon à laquelle rattacher l'asset."}
 },"required":["session_id"]}
},
{
 "name": "unreal_import",
 "description": "Importe un asset exporté dans un projet Unreal Engine : crée le static mesh, active Nanite si pertinent, crée les instances de matériaux et corrige l'inversion du canal vert des cartes de normales entre Blender et Unreal.",
 "inputSchema": {"type":"object","properties":{
   "asset_path":{"type":"string","description":"Chemin de l'asset exporté."},
   "destination":{"type":"string","description":"Dossier de destination dans le projet Unreal."},
   "enable_nanite":{"type":"boolean","description":"Active Nanite. Pertinent pour les maillages statiques uniquement.","default":True},
   "flip_green_channel":{"type":"boolean","description":"Corrige le canal vert des normales.","default":True}
 },"required":["asset_path","destination"]}
},
{
 "name": "unreal_screenshot",
 "description": "Capture une vue du niveau ou d'un asset dans Unreal Engine, pour vérification visuelle après import.",
 "inputSchema": {"type":"object","properties":{
   "target":{"type":"string","description":"Nom de l'acteur ou de l'asset à cadrer."},
   "resolution":{"type":"string","description":"Résolution de la capture.","default":"1920x1080"}
 },"required":["target"]}
},

# ---------------- SON (6 outils) ----------------
{
 "name": "voice_generate",
 "description": "Génère une réplique parlée avec la voix d'un personnage. Si le personnage possède une voix enregistrée dans le canon, elle est appliquée automatiquement. Permet de régler l'intensité émotionnelle.",
 "inputSchema": {"type":"object","properties":{
   "text":{"type":"string","description":"Texte à prononcer."},
   "character_id":{"type":"string","description":"Personnage dont on utilise la voix."},
   "emotion":{"type":"string","enum":["neutre","colere","tristesse","joie","peur","mepris"],"description":"Émotion à jouer.","default":"neutre"},
   "intensity":{"type":"number","description":"Intensité de l'émotion, de 0 à 1.","default":0.5},
   "speed":{"type":"number","description":"Vitesse d'élocution, 1 étant la vitesse normale.","default":1.0}
 },"required":["text"]}
},
{
 "name": "voice_clone",
 "description": "Enregistre une nouvelle voix de personnage à partir d'un échantillon audio de quelques secondes, et la rattache à l'entité correspondante du canon.",
 "inputSchema": {"type":"object","properties":{
   "character_id":{"type":"string","description":"Personnage auquel rattacher la voix."},
   "sample_path":{"type":"string","description":"Chemin de l'échantillon audio."},
   "name":{"type":"string","description":"Nom de la voix."}
 },"required":["character_id","sample_path"]}
},
{
 "name": "music_generate",
 "description": "Génère un morceau de musique à partir d'une description. Si un thème de faction ou de lieu existe, il peut être appliqué pour produire une variation cohérente.",
 "inputSchema": {"type":"object","properties":{
   "prompt":{"type":"string","description":"Description du morceau : genre, instruments, ambiance."},
   "theme_id":{"type":"string","description":"Thème existant à décliner."},
   "duration":{"type":"integer","description":"Durée en secondes.","default":120},
   "instrumental":{"type":"boolean","description":"Sans paroles.","default":True},
   "linked_entity_id":{"type":"string","description":"Entité du canon concernée."}
 },"required":["prompt"]}
},
{
 "name": "music_train_theme",
 "description": "Entraîne un thème musical réutilisable à partir de quelques morceaux, pour qu'une faction ou un lieu ait une signature sonore reconnaissable et déclinable.",
 "inputSchema": {"type":"object","properties":{
   "linked_entity_id":{"type":"string","description":"Entité dont on entraîne le thème."},
   "track_ids":{"type":"array","items":{"type":"string"},"description":"Morceaux servant de base."},
   "theme_name":{"type":"string","description":"Nom du thème."}
 },"required":["linked_entity_id","track_ids","theme_name"]}
},
{
 "name": "ambience_find",
 "description": "Cherche des ambiances sonores et des bruitages dans la banque libre, à partir d'une description. Renvoie des candidats avec leur licence et leur durée.",
 "inputSchema": {"type":"object","properties":{
   "query":{"type":"string","description":"Description de l'ambiance recherchée."},
   "duration_min":{"type":"integer","description":"Durée minimale en secondes."},
   "loopable":{"type":"boolean","description":"Ne renvoie que des sons bouclables.","default":False},
   "limit":{"type":"integer","description":"Nombre de résultats.","default":10}
 },"required":["query"]}
},
{
 "name": "ambience_assemble",
 "description": "Assemble plusieurs sons en une ambiance continue, avec fondus, superpositions et variations aléatoires, et renvoie le fichier produit.",
 "inputSchema": {"type":"object","properties":{
   "layers":{"type":"array","items":{"type":"object"},"description":"Couches sonores avec leur volume et leur mode de répétition."},
   "duration":{"type":"integer","description":"Durée totale en secondes.","default":300},
   "linked_entity_id":{"type":"string","description":"Lieu du canon concerné."}
 },"required":["layers"]}
},
]
