# smartpot_db

Elaboration de la base de données pour le projet Smart Pot'

Déroulement du projet et du module
1 – Travail préliminaire
-	Familiarisation avec SQL
-	Choix et téléchargent des outils utilisés
2 – Création de la BDD
-	Définition des données souhaitées et nécessaires avec les modules IMA_ANALYSIS et ANDROID.
-	Recherche de BDD en ligne qui répond à nos exigences : système de notation, image, information générale, informations détaillées
-	Création de la BDD par webscrapping : accès automatique à chaque page web d’une bibliothèque avec la librairie requests puis sélection des informations qui nous intéresse avec la librairie beautifulSoup4.
3 – Interaction avec la BDD
-	Ecriture des interfaces avec les autres modules
-	Implémentation des méthodes pour insérer/récupérer/modifier/supprimer les données : relation avec utilisateur.
4 – Evolution graphique : visualisation de données
-	Récupération des valeurs des capteurs (directement sur le serveur)
-	Représentation graphique de l’évolution des principaux paramètres de chaque pot (humidité, éclairage, température) en fonction du temps
5 – Système de recommandation
-	Elaboration d’un système de recommandation de plante plutôt basique : élaboration d’une note pour chaque plante en fonction des différents critères choisis par l’utilisateur
6 – système de notation : aspect social (éventuelle implantation s’il reste du temps)
-	Système de notation : note attribuée par les utilisateurs 
-	Commentaires : possibilité de laisser un commentaire/conseil d’utilisation après la suppression du pot sur l’application


Base de données : smart
 

Description des tables : 
PLANT
Cette table recueille l’ensemble des informations générales (pédagogique) à l’utilisateur mais aussi l’ensemble des caractéristiques nécessaire pour assurer le bon développement de la plante.
Line	Description	Type	Possible values
plant_id	Identifiant unique de chaque plante	Int	0 à 1660
common_name	Nom(s) attribué(s) à la plante	Str	/
latin_name	Nom latin unique attribué à la plante	Str	/
family	Famille à laquelle la plante appartient	Str	/
type	Type de plante	Str	"None", "Arbre", "Arbuste", "Plante comestible", "Plante ornementale"
color	Couleur possible de la fleur de la plante	Str	"blanches", "bleues" "jaunes", "rouges", "roses", "vertes", "violettes", "grises", "oranges", "multicolores ou panachées", "noires"
vegetation	Type de vegetation	Str	"Vivace", "Bisannuelle", "Annuelle"
care	Note evaluant la difficulté de l’occupation de la plante	Int	1 = easy, 2 = intermediate, 3 = hard
humidity	Note évaluant la quantité d’eau nécessaire pour l’entretien de la plante	Int	1 = low, 2 = medium, 3 = high
growth	Note évaluant la vitesse de croissance 	Int	1 = slow, 2 = intermediate, 3 = fast
hardiness	Note évaluant la rusticité (résistance au froid)	Int	1 = low, 2 = medium, 3 = high
soil	Type de sol dans laquelle l’évolution de la plante est la plus favorable	Str	"Sol argileux", "Sol calcaire", "Sol sableux", "Sol caillouteux", "Humifère", "Terre de bruyère", "Terreau"
lighting	Note évaluant la quantité de lumière nécessaire à la plante	Int	1 = low, 2 = medium, 3 = high
image	Adresse d’une image de la plante	Str	Format png
description	Courte description textuelle de la plante	Str	/
plantation	Période de plantation privilégiée pour la plante	Str	Intervalle entre JANV.et DEC.


FEEDBACK
Cette table recueille toutes les notes et les commentaires qu’ont été attribué à chaque plante. On peut retrouver le résultat de chaque plante en faisant une sélection sur l’identifiant.
line	Description	Type	Possible values
plant_id	Identifiant de plante qu’un utilisateur à planté	Int	1 à 1660
grade	Note attribuée par l’utilisateur	Int	Note allant de 0 à 5
comment	Commentaire attribué à la plante par l’utilisateur après sa suppression de l’application	Str	/


CHARACTERISTICS
Cette table enregistre les valeurs des capteurs (s’ils sont branchés) des différents pots.
L’absence de client ne nous a pas facilité le travail, nous avons donc décidé de laisser toutes ses informations publiques même si elles ne vont pas vraiment très utiles pour les autres mais cela permet au moins le partage d’information plus facilement.
Line	Description	Type	Possible values
id_r	Identifiant unique du « pot » selctionné	Int	/
date	Date de l’enregistrement des données	Str	Jour et heure (fonction time() de python)
humidity	Valeur de l’humidité du pot id_r (« None » si pas de capteur)	Flt	0 à100
temperature	Valeur de la température du pot id_r (« None » si pas de capteur)	Flt	0 à 100
lighting	Valeur de l’éclairage du pot id_r (« None » si pas de capteur)	Flt	0 à 100


IMAGE
Cette table enregistre les différentes images qui ont été prises par les caméras installés sur tous les pots.
L’absence de client ne nous a pas facilité le travail, nous avons donc décidé de laisser toutes ses informations publiques même si elles ne vont pas vraiment très utiles pour les autres mais cela permet au moins le partage d’information plus facilement.

image	Description	Type	Valeurs possibles
id_cam	Identifiant de la camera associé à un pot	Int	/
date	Date de l’enregistrement de la photo	Str	Valeur renvoyée par la fonction time() de python
image	Image enregistrée sous format pnj	Str	/






