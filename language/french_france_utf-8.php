<?php
// +---------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                            |
// +---------------------------------------------------------------------------+
// | French (France) UTF-8 language overlay                                    |
// +---------------------------------------------------------------------------+
// | MediaGallery 1.8.0                                                        |
// |                                                                           |
// | The English language file is used as a complete fallback so that new      |
// | MediaGallery strings remain available even when a French translation has  |
// | not yet been added. French translations below override matching strings.  |
// +---------------------------------------------------------------------------+

if (stripos($_SERVER['PHP_SELF'], basename(__FILE__)) !== false) {
    die('This file can not be used on its own!');
}

require dirname(__FILE__) . '/english_utf-8.php';

$MG_FR_TRANSLATIONS = array(
    // General
    'Media Gallery' => 'Galerie multimédia',
    'Access Denied' => 'Accès refusé',
    'Warning! Plugin is still Enabled' => 'Attention ! Le plugin est toujours activé',
    'Disable plugin before uninstalling.' => 'Désactivez le plugin avant de le désinstaller.',
    'Media Item' => 'Média',
    'Media Gallery Search Results' => 'Résultats de recherche de la galerie multimédia',
    'Views' => 'Vues',
    'No Date' => 'Aucune date',
    'Rating' => 'Note',
    'No media title available' => 'Aucun titre disponible pour ce média',
    'Album: ' => 'Album : ',

    // Common actions
    'Help' => 'Aide',
    'Save' => 'Enregistrer',
    'Yes' => 'Oui',
    'No' => 'Non',
    'Submit' => 'Envoyer',
    'Cancel' => 'Annuler',
    'Reset' => 'Réinitialiser',
    'Delete' => 'Supprimer',
    'All' => 'Tous',
    'Top' => 'Haut',
    'Bottom' => 'Bas',
    'Edit' => 'Modifier',
    'Move Up' => 'Monter',
    'Move Down' => 'Descendre',
    'Rotate Left' => 'Pivoter à gauche',
    'Rotate Right' => 'Pivoter à droite',
    'Continue' => 'Continuer',
    'Recheck' => 'Revérifier',
    'Check All' => 'Tout sélectionner',
    'Uncheck All' => 'Tout désélectionner',
    'Approve' => 'Approuver',
    'Options' => 'Options',
    'Details ' => 'Détails ',
    'None' => 'Aucun',
    'Both' => 'Les deux',
    'Ascending' => 'Croissant',
    'Descending' => 'Décroissant',
    'Date' => 'Date',
    'Time' => 'Heure',
    'Title' => 'Titre',
    'Description' => 'Description',
    'File' => 'Fichier',
    'Directory' => 'Répertoire',
    'Action' => 'Action',
    'Status' => 'État',
    'Count' => 'Nombre',
    'Order' => 'Ordre',
    'Select' => 'Sélectionner',
    'User Name' => 'Nom d’utilisateur',
    'User ID' => 'ID utilisateur',
    'Active' => 'Actif',

    // Albums
    'Root Album' => 'Album racine',
    'Root Album - No image upload allowed' => 'Album racine - aucun téléversement d’image autorisé',
    'Root Album Skin' => 'Habillage de l’album racine',
    'Root Album Name' => 'Nom de l’album racine',
    'Root Album Display Colums' => 'Colonnes d’affichage de l’album racine',
    'Root Album Display Rows' => 'Lignes d’affichage de l’album racine',
    'Root Album Theme' => 'Thème de l’album racine',
    'New Album' => 'Nouvel album',
    'Edit Album' => 'Modifier l’album',
    'Create Album' => 'Créer un album',
    'Delete Album' => 'Supprimer l’album',
    'Album Title / Description' => 'Titre / description de l’album',
    'Albums' => 'Albums',
    'Album' => 'Album',
    'Album Title' => 'Titre de l’album',
    'Parent Album' => 'Album parent',
    'Featured Album' => 'Album mis en avant',
    'Set as Featured' => 'Mettre en avant',
    'Album Link' => 'Lien de l’album',
    'Album Cover' => 'Couverture de l’album',
    'Album Attributes' => 'Attributs de l’album',
    'Sub Albums' => 'Sous-albums',
    'Destination Album' => 'Album de destination',
    'Sort Albums' => 'Trier les albums',
    'Quick Album Create' => 'Création rapide d’un album',
    'Member Albums' => 'Albums des membres',
    'Enable Member Albums' => 'Activer les albums des membres',
    'Member Albums Root Album' => 'Album racine des albums des membres',
    'Allow Creation under Member Root' => 'Autoriser la création sous la racine des membres',
    'Archive Deleted Member Albums' => 'Archiver les albums de membres supprimés',
    'Create Member Albums' => 'Créer les albums des membres',
    'Auto Create Albums' => 'Créer automatiquement les albums',

    // Media
    'Upload Media' => 'Téléverser des médias',
    'FTP Media' => 'Médias FTP',
    'Media Queue' => 'File d’attente des médias',
    'Media Management' => 'Gestion des médias',
    'Manage Media' => 'Gérer les médias',
    'Edit Media Item' => 'Modifier le média',
    'Media Title' => 'Titre du média',
    'Media Attributes' => 'Attributs du média',
    'Add Media' => 'Ajouter un média',
    'Sort Media' => 'Trier les médias',
    'No media items found in this album' => 'Aucun média trouvé dans cet album',
    'No caption' => 'Aucune légende',
    'Caption' => 'Légende',
    'Images' => 'Images',
    'Thumbnail' => 'Miniature',
    'Attached Thumbnail' => 'Miniature associée',
    'Album Cover' => 'Couverture de l’album',
    'Capture Time' => 'Date de prise de vue',
    'Uploaded by' => 'Téléversé par',
    'Media Capture Time' => 'Date de capture du média',
    'Media Upload Time' => 'Date de téléversement du média',
    'Delete Source Files' => 'Supprimer les fichiers source',
    'Delete All Media Items in Album' => 'Supprimer tous les médias de l’album',
    'Move All Media' => 'Déplacer tous les médias',
    'File List' => 'Liste des fichiers',
    'FTP Path Directory' => 'Répertoire FTP',
    'into album' => 'dans l’album',
    'Web Browser Upload' => 'Téléversement depuis le navigateur',

    // Display / navigation
    'Homepage Only' => 'Page d’accueil uniquement',
    'Display Rows' => 'Lignes affichées',
    'Display Columns' => 'Colonnes affichées',
    'General Options' => 'Options générales',
    'Display Options' => 'Options d’affichage',
    'Image Properties' => 'Propriétés de l’image',
    'Left blocks only' => 'Blocs de gauche uniquement',
    'Right blocks only' => 'Blocs de droite uniquement',
    'Left and right blocks' => 'Blocs de gauche et de droite',
    'Display Geeklog Blocks' => 'Afficher les blocs Geeklog',
    'Show Sub-Albums in Select Box' => 'Afficher les sous-albums dans la liste de sélection',
    'Image Skin' => 'Habillage de l’image',
    'Album Skin' => 'Habillage de l’album',
    'Display Image Skin' => 'Habillage de l’image affichée',
    'Gallery View Thumbnail Size' => 'Taille des miniatures de la galerie',
    'Custom Thumbnail Height' => 'Hauteur personnalisée des miniatures',

    // Administration / configuration
    'Media Gallery Administration' => 'Administration de la galerie multimédia',
    'Media Gallery Configuration' => 'Configuration de la galerie multimédia',
    'Media Gallery Configuration Options' => 'Options de configuration de la galerie multimédia',
    'Media Gallery Album Maintenance' => 'Maintenance des albums de la galerie multimédia',
    'Media Gallery Media Edit' => 'Modification des médias de la galerie multimédia',
    'Media Gallery Usage Reports' => 'Rapports d’utilisation de la galerie multimédia',
    'Admin Home' => 'Accueil administration',
    'Configuration' => 'Configuration',
    'Usage Reports' => 'Rapports d’utilisation',
    'Usage Tracking' => 'Suivi de l’utilisation',
    'Graphics Package' => 'Bibliothèque graphique',
    'Graphics Package Path' => 'Chemin de la bibliothèque graphique',
    'Allow Comments' => 'Autoriser les commentaires',
    'Enable EXIF' => 'Activer EXIF',
    'Enable Ratings' => 'Activer les notes',
    'Disable EXIF Display' => 'Désactiver l’affichage EXIF',
    'Enable Slideshow' => 'Activer le diaporama',
    'Include in Random Image block' => 'Inclure dans le bloc d’image aléatoire',
    'Thumbnail size' => 'Taille des miniatures',
    'System Default' => 'Valeur par défaut du système',
    'Date Format' => 'Format de date',
    'Version Information' => 'Informations de version',
    'Your installation is up to date, no updates are available for your version of Media Gallery' => 'Votre installation est à jour, aucune mise à jour n’est disponible pour votre version de MediaGallery',
    'Unable to determine latest version of Media Gallery.' => 'Impossible de déterminer la dernière version de MediaGallery.',

    // Slideshow / playback
    'Slideshow' => 'Diaporama',
    'Play' => 'Lecture',
    'Stop' => 'Arrêter',
    'Previous' => 'Précédent',
    'Next' => 'Suivant',
    'Home' => 'Accueil',
    'Return to Album' => 'Retour à l’album',
    'Normal Size' => 'Taille normale',
    'Full Size' => 'Taille originale',
    'Loop' => 'Boucle',
    'Seconds' => 'Secondes',
    'Transition' => 'Transition',
    'Delay' => 'Délai',
    'Picture Loading' => 'Chargement de l’image',
    'Please Wait' => 'Veuillez patienter',
    'Play Inline' => 'Lire dans la page',
    'Play in Popup Window' => 'Lire dans une fenêtre contextuelle',
    'Download to local computer' => 'Télécharger sur l’ordinateur',

    // Miscellaneous
    'Not Found' => 'Introuvable',
    'NOT Writable' => 'NON inscriptible',
    'Directory NOT writable' => 'Répertoire NON inscriptible',
    'Documentation' => 'Documentation',
    'Usage Documentation' => 'Documentation d’utilisation',
    'PHP Information' => 'Informations PHP',
    'Error in Autotag' => 'Erreur dans l’autotag',
    'Thank you for your submission' => 'Merci pour votre contribution',
    'Your media upload has been approved' => 'Votre média téléversé a été approuvé',
    'Select Date' => 'Sélectionner une date',
    'Select User' => 'Sélectionner un utilisateur',
    'All Dates' => 'Toutes les dates',
    'New Report' => 'Nouveau rapport',
    'Quota Reports' => 'Rapports de quota',
    'Default Member Quota' => 'Quota par défaut des membres',
    'Small (100x100)' => 'Petite (100x100)',
    'Medium (150x150)' => 'Moyenne (150x150)',
    'Large (200x200)' => 'Grande (200x200)'
);

// Apply translations to every MediaGallery language array loaded by the
// English fallback. Exact-value matching keeps keys and placeholders intact.
foreach ($GLOBALS as $MG_FR_NAME => &$MG_FR_VALUES) {
    if (strpos($MG_FR_NAME, 'LANG_MG') !== 0 || !is_array($MG_FR_VALUES)) {
        continue;
    }

    array_walk_recursive($MG_FR_VALUES, function (&$MG_FR_VALUE) use ($MG_FR_TRANSLATIONS) {
        if (is_string($MG_FR_VALUE) && isset($MG_FR_TRANSLATIONS[$MG_FR_VALUE])) {
            $MG_FR_VALUE = $MG_FR_TRANSLATIONS[$MG_FR_VALUE];
        }
    });
}
unset($MG_FR_VALUES, $MG_FR_NAME, $MG_FR_TRANSLATIONS);
