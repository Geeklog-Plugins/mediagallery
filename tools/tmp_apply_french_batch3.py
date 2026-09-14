from pathlib import Path
import re

path = Path('language/french_france_utf-8.php')
text = path.read_text(encoding='utf-8').rstrip() + '\n\n'

block = r'''// ---------------------------------------------------------------------------
// French localization coverage - batch 3
// ---------------------------------------------------------------------------

// Remaining administration/upload/technical labels
$LANG_MG01['asf'] = 'WMV';
$LANG_MG01['bmp'] = 'BMP';
$LANG_MG01['coppermine_import'] = 'Coppermine';
$LANG_MG01['flowplayer'] = 'FlowPlayer';
$LANG_MG01['flv'] = 'FLV';
$LANG_MG01['fourimages_import'] = '4images';
$LANG_MG01['gallery_import'] = 'Gallery v1.x';
$LANG_MG01['gallery_v2_import'] = 'Gallery v2';
$LANG_MG01['geekary_import'] = 'Geekary';
$LANG_MG01['gif'] = 'GIF';
$LANG_MG01['inm_import'] = 'Inmemoriam';
$LANG_MG01['jpg'] = 'JPEG';
$LANG_MG01['js_slideshow'] = 'JavaScript';
$LANG_MG01['lightbox'] = 'Lightbox';
$LANG_MG01['mgflv'] = 'Lecteur Flash MG';
$LANG_MG01['mov'] = 'MOV';
$LANG_MG01['mp3'] = 'MP3';
$LANG_MG01['mp3ribbon'] = 'Lecteur ruban MP3';
$LANG_MG01['mp4'] = 'MP4';
$LANG_MG01['mpg'] = 'MPEG';
$LANG_MG01['no_applet'] = 'Votre navigateur ne prend pas en charge les applets Java ou celles-ci sont désactivées.';
$LANG_MG01['ogg'] = 'OGG';
$LANG_MG01['ok'] = 'OK';
$LANG_MG01['png'] = 'PNG';
$LANG_MG01['psd'] = 'PSD';
$LANG_MG01['quicktime'] = 'Lecteur QuickTime';
$LANG_MG01['quicktime_player'] = 'Lecteur QuickTime';
$LANG_MG01['rflv'] = 'FLV distant';
$LANG_MG01['seperator'] = 'Séparateur du fil d’Ariane';
$LANG_MG01['size_500x375'] = 'Taille 500x375';
$LANG_MG01['size_600x450'] = 'Taille 600x450';
$LANG_MG01['size_620x465'] = 'Taille 620x465';
$LANG_MG01['size_720x540'] = 'Taille 720x540';
$LANG_MG01['size_800x600'] = 'Taille 800x600';
$LANG_MG01['size_912x684'] = 'Taille 912x684';
$LANG_MG01['size_1024x768'] = 'Taille 1024x768';
$LANG_MG01['size_1152x864'] = 'Taille 1152x864';
$LANG_MG01['size_1280x1024'] = 'Taille 1280x1024';
$LANG_MG01['size_custom'] = 'Personnalisée - ';
$LANG_MG01['swf'] = 'SWF';
$LANG_MG01['tga'] = 'TGA';
$LANG_MG01['tif'] = 'TIF';
$LANG_MG01['tn_size_help'] = 'Sélectionnez la taille des miniatures affichées dans les albums.';
$LANG_MG01['top_left'] = 'En haut à gauche';
$LANG_MG01['top_center'] = 'En haut au centre';
$LANG_MG01['top_right'] = 'En haut à droite';
$LANG_MG01['total_items'] = 'Nombre total d’éléments à traiter';
$LANG_MG01['up_av_override'] = 'Autoriser l’utilisateur à définir les options de lecture audio/vidéo';
$LANG_MG01['up_columns_override'] = 'Autoriser l’utilisateur à définir le nombre de colonnes';
$LANG_MG01['up_mp3_override'] = 'Autoriser l’utilisateur à définir le lecteur MP3';
$LANG_MG01['up_overrides'] = 'Préférences utilisateur';
$LANG_MG01['up_rows_override'] = 'Autoriser l’utilisateur à définir le nombre de lignes';
$LANG_MG01['up_tn_override'] = 'Autoriser l’utilisateur à définir la taille des miniatures';
$LANG_MG01['update'] = 'Mettre à jour';
$LANG_MG01['upload_allowed_types'] = '<strong>Types de fichiers autorisés :</strong> ';
$LANG_MG01['upload_approved'] = 'Votre téléversement a été approuvé';
$LANG_MG01['upload_cancel_all'] = 'Annuler tous les téléversements';
$LANG_MG01['upload_cancelled'] = 'Annulé';
$LANG_MG01['upload_complete'] = 'Terminé';
$LANG_MG01['upload_continue'] = 'Continuer';
$LANG_MG01['upload_err_album_id'] = 'Impossible de déterminer l’album de destination';
$LANG_MG01['upload_err_filesize'] = 'Le fichier est trop volumineux';
$LANG_MG01['upload_err_filetype'] = 'Type de fichier non valide';
$LANG_MG01['upload_err_general'] = 'Erreur de téléversement';
$LANG_MG01['upload_err_session'] = 'Informations de session indisponibles - rechargez la page';
$LANG_MG01['upload_err_zerosize'] = 'Le fichier a une taille de zéro octet';
$LANG_MG01['upload_error'] = 'Erreur de téléversement :';
$LANG_MG01['upload_fail_validation'] = 'Échec de la validation. Téléversement ignoré.';
$LANG_MG01['upload_failed'] = 'Échec du téléversement';
$LANG_MG01['upload_file'] = 'fichier';
$LANG_MG01['upload_file_size_limit'] = '<strong>Taille maximale :</strong> ';
$LANG_MG01['upload_files'] = 'fichiers';
$LANG_MG01['upload_io_error'] = 'Erreur serveur (E/S)';
$LANG_MG01['upload_limit_exceeded'] = 'Limite de téléversement dépassée';
$LANG_MG01['upload_one_file'] = 'un fichier';
$LANG_MG01['upload_pending'] = 'En attente…';
$LANG_MG01['upload_q_limit'] = 'Vous avez atteint la limite de téléversement.';
$LANG_MG01['upload_q_select'] = 'Vous pouvez sélectionner';
$LANG_MG01['upload_q_too_many'] = 'Vous avez tenté d’ajouter trop de fichiers à la file.\n';
$LANG_MG01['upload_q_up_to'] = 'jusqu’à';
$LANG_MG01['upload_queue'] = 'File de téléversement';
$LANG_MG01['upload_sec_error'] = 'Erreur de sécurité';
$LANG_MG01['upload_stopped'] = 'Arrêté';
$LANG_MG01['upload_types_desc'] = 'Types de fichiers sélectionnés';
$LANG_MG01['upload_unhandled'] = 'Erreur non gérée :';
$LANG_MG01['upload_uploaded'] = 'téléversé';
$LANG_MG01['upload_uploading'] = 'Téléversement…';
$LANG_MG01['upload_usage'] = "<p>Sélectionnez l’album de destination, puis cliquez sur « Téléverser » pour afficher le sélecteur de fichiers. Vous pouvez sélectionner plusieurs fichiers en maintenant Ctrl, ou une plage avec Maj.</p>";
$LANG_MG01['upload_warning'] = 'La configuration autorise uniquement les fichiers de %s Mo ou moins, et le total téléversé ne doit pas dépasser %s Mo.';
$LANG_MG01['usage_report_help'] = 'Générez les rapports d’utilisation Media Gallery par utilisateur et par date. Évitez de demander tous les utilisateurs pour toutes les dates simultanément.';
$LANG_MG01['use_mms'] = 'Utiliser les liens mms: pour les médias Microsoft compatibles';
$LANG_MG01['used'] = 'Utilisé';
$LANG_MG01['user_prefs_title'] = 'Options utilisateur de Media Gallery';
$LANG_MG01['user_quota'] = 'Votre quota est de %d Ko ; %d Ko sont utilisés et %d Ko restent disponibles.<br' . XHTML . '><br' . XHTML . '>';
$LANG_MG01['userid'] = 'ID utilisateur';
$LANG_MG01['username'] = 'Nom d’utilisateur';
$LANG_MG01['utilities'] = 'Utilitaires';
$LANG_MG01['verbose'] = 'Détaillé (journalisation de débogage)';
$LANG_MG01['watermark_auto'] = 'Appliquer automatiquement un filigrane au téléversement';
$LANG_MG01['watermark_image'] = 'Image de filigrane';
$LANG_MG01['watermark_location'] = 'Position du filigrane';
$LANG_MG01['watermark_opacity'] = 'Opacité du filigrane';
$LANG_MG01['watermark_redirect'] = 'Cliquez <a href="%s">ici</a> pour revenir à la gestion des filigranes.';
$LANG_MG01['watermarked'] = 'Filigrané';
$LANG_MG01['whatsnew_time'] = 'Durée d’affichage dans Quoi de neuf';
$LANG_MG01['windows_media_player'] = 'Windows Media Player';
$LANG_MG01['wm_upload_help'] = 'Sélectionnez une image de filigrane à téléverser. Formats pris en charge : GIF, PNG, JPG. Taille maximale : 64 Ko.';
$LANG_MG01['wn_title_length'] = 'Longueur du titre dans Quoi de neuf';
$LANG_MG01['xp_pub'] = 'Publication XP';
$LANG_MG01['xppubwizard_install'] = 'Installation de l’assistant de publication XP';
$LANG_MG01['zero_unlimited'] = '0 = illimité';
$LANG_MG01['zip'] = 'ZIP';
$LANG_MG01['zip_enable'] = 'Activer les téléversements ZIP';
$LANG_MG01['zip_path'] = 'Chemin vers le programme de décompression';

// Remaining main interface labels
$LANG_MG03['agree'] = 'J’accepte';
$LANG_MG03['album'] = 'Album';
$LANG_MG03['album_id_display'] = 'ID album : ';
$LANG_MG03['artist'] = 'Artiste';
$LANG_MG03['by'] = 'par';
$LANG_MG03['cast'] = 'Distribution';
$LANG_MG03['click_here'] = 'Cliquez ici';
$LANG_MG03['download'] = 'Télécharger';
$LANG_MG03['enroll_title'] = 'Inscription à un album membre';
$LANG_MG03['existing_member_album'] = 'Vous possédez déjà un album membre.';
$LANG_MG03['ftp_help'] = 'Sélectionnez les fichiers FTP à ajouter à l’album.';
$LANG_MG03['genre'] = 'Genre';
$LANG_MG03['info'] = 'Informations';
$LANG_MG03['js_warning'] = 'JavaScript doit être activé pour utiliser cette fonction.';
$LANG_MG03['large'] = 'Grande';
$LANG_MG03['list_desc'] = 'Description';
$LANG_MG03['list_size'] = 'Taille';
$LANG_MG03['list_title'] = 'Titre';
$LANG_MG03['list_updated'] = 'Mis à jour';
$LANG_MG03['list_user'] = 'Utilisateur';
$LANG_MG03['media_properties'] = 'Propriétés du média';
$LANG_MG03['member_album_overview'] = 'Présentation des albums des membres';
$LANG_MG03['member_album_signup'] = 'Créer mon album membre';
$LANG_MG03['member_album_terms'] = 'Conditions d’utilisation des albums membres';
$LANG_MG03['no_comments'] = 'Aucun commentaire';
$LANG_MG03['no_flash'] = 'Flash n’est pas disponible.';
$LANG_MG03['no_new_items'] = 'Aucun nouvel élément';
$LANG_MG03['no_quicktime'] = 'QuickTime n’est pas disponible.';
$LANG_MG03['no_search_found'] = 'Aucun résultat trouvé.';
$LANG_MG03['normal'] = 'Normale';
$LANG_MG03['on'] = 'le';
$LANG_MG03['play_full_album'] = 'Lire tout l’album';
$LANG_MG03['published'] = 'Publié';
$LANG_MG03['return_to_index'] = 'Retour à l’index';
$LANG_MG03['search_results'] = 'Résultats de recherche';
$LANG_MG03['song'] = 'Morceau';
$LANG_MG03['track'] = 'Piste';
$LANG_MG03['upload_help'] = 'Sélectionnez les médias à téléverser dans cet album.';
$LANG_MG03['upload_size'] = 'Taille du téléversement';
$LANG_MG03['vote'] = 'vote';
$LANG_MG03['votes'] = 'votes';
$LANG_MG03['year'] = 'Année';
$LANG_MG03['your_member_album'] = 'Votre album membre';
$LANG_MG03['zip_file_help'] = 'Les fichiers ZIP seront extraits et leur contenu ajouté à votre album après le téléversement.';

// Slideshow transition names
$LANG_MG05['blend'] = 'Fondu';
$LANG_MG05['blinds'] = 'Stores';
$LANG_MG05['checkerboard'] = 'Damier';
$LANG_MG05['diagonal'] = 'Diagonale';
$LANG_MG05['doors'] = 'Portes';
$LANG_MG05['gradient'] = 'Dégradé';
$LANG_MG05['iris'] = 'Iris';
$LANG_MG05['pinwheel'] = 'Moulinet';
$LANG_MG05['pixelate'] = 'Pixellisation';
$LANG_MG05['radial'] = 'Radial';
$LANG_MG05['rain'] = 'Pluie';
$LANG_MG05['slide'] = 'Glissement';
$LANG_MG05['snow'] = 'Neige';
$LANG_MG05['spiral'] = 'Spirale';
$LANG_MG05['stretch'] = 'Étirement';
$LANG_MG05['random'] = 'Aléatoire';

// Playback options
$LANG_MG07['playback_options'] = 'Options de lecture';
$LANG_MG07['none'] = 'aucun';
$LANG_MG07['mini'] = 'mini';
$LANG_MG07['full'] = 'complet';
$LANG_MG07['low'] = 'faible';
$LANG_MG07['high'] = 'élevée';
$LANG_MG07['showall'] = 'Tout afficher';
$LANG_MG07['noborder'] = 'Sans bordure';
$LANG_MG07['exactfit'] = 'Ajustement exact';
$LANG_MG07['window'] = 'Fenêtre';
$LANG_MG07['opaque'] = 'Opaque';
$LANG_MG07['transparent'] = 'Transparent';
$LANG_MG07['to_fit'] = 'Ajuster';
$LANG_MG07['aspect'] = 'Conserver les proportions';
$LANG_MG07['normal_size'] = 'Taille normale';
$LANG_MG07['description'] = 'Description';
$LANG_MG07['option'] = 'Option';
$LANG_MG07['on'] = 'Activé';
$LANG_MG07['off'] = 'Désactivé';
$LANG_MG07['auto_start'] = 'Démarrage automatique';
$LANG_MG07['auto_start_help'] = 'Démarre automatiquement la lecture lorsque le lecteur estime que suffisamment de données sont disponibles.';
$LANG_MG07['enable_context_menu'] = 'Activer le menu contextuel';
$LANG_MG07['enable_context_menu_help'] = 'Affiche le menu contextuel lors d’un clic droit.';
$LANG_MG07['stretch_to_fit'] = 'Étendre pour ajuster';
$LANG_MG07['stretch_to_fit_help'] = 'Étire la vidéo pour remplir la zone d’affichage du lecteur.';
$LANG_MG07['status_bar'] = 'Afficher la barre d’état';
$LANG_MG07['status_bar_help'] = 'Affiche la barre d’état du lecteur.';
$LANG_MG07['ui_mode'] = 'Mode d’interface utilisateur';
$LANG_MG07['ui_mode_help'] = 'Définit les commandes affichées dans l’interface du lecteur.';
$LANG_MG07['height'] = 'Hauteur';
$LANG_MG07['width'] = 'Largeur';
$LANG_MG07['height_help'] = 'Taille de la fenêtre de lecture';
$LANG_MG07['width_help'] = 'Taille de la fenêtre de lecture';
$LANG_MG07['menu'] = 'Menu';
$LANG_MG07['menu_help'] = 'Affiche le menu complet du lecteur.';
$LANG_MG07['quality'] = 'Qualité';
$LANG_MG07['quality_help'] = 'Qualité de lecture';
$LANG_MG07['flash_vars'] = 'Variables Flash';
$LANG_MG07['auto_ref'] = 'Référence automatique';
$LANG_MG07['auto_ref_help'] = 'Charge automatiquement le média sans attendre un clic.';
$LANG_MG07['controller'] = 'Contrôleur';
$LANG_MG07['controller_help'] = 'Affiche les commandes du lecteur.';
$LANG_MG07['kiosk_mode'] = 'Mode kiosque';
$LANG_MG07['kiosk_mode_help'] = 'En mode kiosque, certaines commandes contextuelles et le glisser-déposer sont désactivés.';
$LANG_MG07['scale'] = 'Échelle';
$LANG_MG07['scale_help'] = 'Définit la manière dont le média est ajusté à la zone intégrée.';
$LANG_MG07['swf_scale_help'] = 'Définit la manière dont le contenu Flash est ajusté à la zone disponible.';
$LANG_MG07['wmode'] = 'Mode de fenêtre';
$LANG_MG07['wmode_help'] = 'Définit le mode de fenêtre du contenu Flash pour la transparence et le positionnement.';
$LANG_MG07['loop'] = 'Boucle';
$LANG_MG07['loop_help'] = 'Définit si la lecture recommence automatiquement.';
$LANG_MG07['always'] = 'Toujours';
$LANG_MG07['sameDomain'] = 'Même domaine';
$LANG_MG07['never'] = 'Jamais';
$LANG_MG07['asa'] = 'Autoriser l’accès aux scripts';
$LANG_MG07['asa_help'] = 'Contrôle si ActionScript peut appeler JavaScript dans la page HTML.';
$LANG_MG07['bgcolor'] = 'Couleur d’arrière-plan';
$LANG_MG07['bgcolor_help'] = 'Définit la couleur d’arrière-plan de la fenêtre de lecture.';
$LANG_MG07['clsid'] = 'ID de classe de l’objet';
$LANG_MG07['codebase'] = 'Base de code';
$LANG_MG07['playcount'] = 'Nombre de lectures';
$LANG_MG07['playcount_help'] = 'Nombre de répétitions du fichier.';
$LANG_MG07['wmp_options'] = 'Windows Media Player';
$LANG_MG07['qt_options'] = 'Lecteur QuickTime';
$LANG_MG07['mp3_options'] = 'Lecture MP3';
$LANG_MG07['swf_options'] = 'Lecteur Flash';
$LANG_MG07['swf_version_help'] = 'Version de Flash requise pour lire ce fichier.';
$LANG_MG07['resolution'] = 'Résolution (LxH)';
$LANG_MG07['resolution_x_help'] = 'Résolution horizontale de la vidéo';
$LANG_MG07['resolution_y_help'] = 'Résolution verticale de la vidéo';
$LANG_MG07['resolution_x'] = 'Largeur vidéo';
$LANG_MG07['resolution_y'] = 'Hauteur vidéo';

// Success messages
$LANG_MG09[1] = 'Tri effectué avec succès';
$LANG_MG09[2] = 'Options de configuration enregistrées avec succès';
$LANG_MG09[3] = 'Données EXIF/IPTC enregistrées avec succès';
$LANG_MG09[4] = 'Paramètres par défaut des albums enregistrés avec succès';
$LANG_MG09[5] = 'Paramètres audio/vidéo par défaut enregistrés avec succès';
$LANG_MG09[6] = 'Options RSS enregistrées avec succès';
$LANG_MG09[7] = 'Flux reconstruits avec succès';
$LANG_MG09[8] = 'Albums membres sélectionnés supprimés avec succès';
$LANG_MG09[9] = 'Configuration système réinitialisée aux valeurs d’installation';
$LANG_MG09[10] = 'Permissions globales appliquées avec succès';
$LANG_MG09[11] = 'Attributs globaux des albums appliqués avec succès';
$LANG_MG09[12] = 'Options des albums membres enregistrées avec succès';
$LANG_MG09[13] = 'Albums membres sélectionnés créés avec succès';
$LANG_MG09[14] = 'Indicateur des albums membres réinitialisé avec succès';
$LANG_MG09[15] = 'Albums sélectionnés supprimés avec succès';
$LANG_MG09[16] = 'Quotas utilisateurs reconstruits avec succès';
$LANG_MG09[17] = 'Fichiers sélectionnés supprimés avec succès';

// Profile
$LANG_MG10['last_10'] = '5 derniers médias téléversés par l’utilisateur ';
$LANG_MG10['albums_owned'] = 'Albums de la galerie appartenant à l’utilisateur ';
$LANG_MG10['thumbnail'] = 'Miniature';
$LANG_MG10['upload_date'] = 'Date de téléversement';
$LANG_MG10['title'] = 'Titre';
$LANG_MG10['album'] = 'Album';
$LANG_MG10['album_desc'] = 'Description';

// Plugin messages
$PLG_mediagallery_MESSAGE1 = 'Mise à niveau du plugin Media Gallery : mise à jour terminée avec succès.';
$PLG_mediagallery_MESSAGE2 = 'Mise à niveau du plugin Media Gallery : cette version ne peut pas être mise à jour automatiquement. Consultez la documentation du plugin.';
$PLG_mediagallery_MESSAGE3 = 'Échec de la mise à niveau de Media Gallery - consultez error.log.';
$PLG_mediagallery_MESSAGE4 = 'Merci d’avoir noté ce média.';
$PLG_mediagallery_MESSAGE5 = 'Vous avez déjà noté cet élément.';
$PLG_mediagallery_MESSAGE6 = 'Une erreur est survenue lors de l’enregistrement de votre note. Contactez l’administrateur.';
$PLG_mediagallery_MESSAGE7 = 'Aucun élément à traiter.';
$PLG_mediagallery_MESSAGE10 = 'Une erreur est survenue lors du remplacement du fichier média. Consultez error.log.';

// Geeklog configuration UI
$LANG_configsections['mediagallery']['label'] = 'Galerie multimédia';
$LANG_configsections['mediagallery']['title'] = 'Configuration de Media Gallery';

$LANG_confignames['mediagallery']['gallery_only'] = 'Media Gallery remplace la page d’index Geeklog';
$LANG_confignames['mediagallery']['loginrequired'] = 'Connexion obligatoire';
$LANG_confignames['mediagallery']['htmlallowed'] = 'Autoriser le HTML dans les titres';
$LANG_confignames['mediagallery']['usage_tracking'] = 'Suivi de l’utilisation';
$LANG_confignames['mediagallery']['whatsnew'] = 'Activer l’affichage dans Quoi de neuf';
$LANG_confignames['mediagallery']['title_length'] = 'Longueur du titre dans Quoi de neuf (octets)';
$LANG_confignames['mediagallery']['whatsnew_time'] = 'Durée dans Quoi de neuf (jours)';
$LANG_confignames['mediagallery']['preserve_filename'] = 'Conserver le nom de fichier original';
$LANG_confignames['mediagallery']['discard_original'] = 'Supprimer les images originales';
$LANG_confignames['mediagallery']['verbose'] = 'Détaillé (journalisation de débogage)';
$LANG_confignames['mediagallery']['disable_whatsnew_comments'] = 'Désactiver les commentaires dans Quoi de neuf';
$LANG_confignames['mediagallery']['profile_hook'] = 'Afficher les informations Media Gallery dans le profil utilisateur';
$LANG_confignames['mediagallery']['root_album_name'] = 'Nom de l’album racine';
$LANG_confignames['mediagallery']['at_border'] = 'Bordure';
$LANG_confignames['mediagallery']['at_align'] = 'Alignement';
$LANG_confignames['mediagallery']['at_width'] = 'Largeur';
$LANG_confignames['mediagallery']['at_height'] = 'Hauteur';
$LANG_confignames['mediagallery']['at_src'] = 'Source du média';
$LANG_confignames['mediagallery']['at_autoplay'] = 'Lecture automatique';
$LANG_confignames['mediagallery']['at_enable_link'] = 'Activer le lien vers le média';
$LANG_confignames['mediagallery']['at_delay'] = 'Délai du diaporama';
$LANG_confignames['mediagallery']['at_showtitle'] = 'Afficher les titres du diaporama';
$LANG_confignames['mediagallery']['rss_full_enabled'] = 'Créer le flux complet de l’album';
$LANG_confignames['mediagallery']['rss_feed_type'] = 'Type de flux';
$LANG_confignames['mediagallery']['rss_ignore_empty'] = 'Exclure les albums vides du flux';
$LANG_confignames['mediagallery']['rss_anonymous_only'] = 'Inclure uniquement les albums accessibles au public';
$LANG_confignames['mediagallery']['hide_author_email'] = 'Masquer l’e-mail de l’auteur dans le flux';
$LANG_confignames['mediagallery']['rss_feed_name'] = 'Nom de fichier de base du flux';
$LANG_confignames['mediagallery']['dfid'] = 'Format de date';
$LANG_confignames['mediagallery']['displayblocks'] = 'Afficher les blocs Geeklog';
$LANG_confignames['mediagallery']['album_display_columns'] = 'Colonnes d’affichage de l’album racine';
$LANG_confignames['mediagallery']['album_display_rows'] = 'Lignes d’affichage de l’album racine';
$LANG_confignames['mediagallery']['subalbum_select'] = 'Afficher les sous-albums dans la liste de sélection';
$LANG_confignames['mediagallery']['indextheme'] = 'Thème de l’album racine';
$LANG_confignames['mediagallery']['indexskin'] = 'Habillage de l’album racine';
$LANG_confignames['mediagallery']['jpg_orig_quality'] = 'Qualité JPG de l’original';
$LANG_confignames['mediagallery']['jpg_quality'] = 'Qualité JPG d’affichage';
$LANG_confignames['mediagallery']['tn_jpg_quality'] = 'Qualité JPG des miniatures';
$LANG_confignames['mediagallery']['gallery_tn_size'] = 'Taille des miniatures de la galerie';
$LANG_confignames['mediagallery']['gallery_tn_height'] = 'Hauteur personnalisée des miniatures';
$LANG_confignames['mediagallery']['gallery_tn_width'] = 'Largeur personnalisée des miniatures';
$LANG_confignames['mediagallery']['enable_media_id'] = 'Afficher l’identifiant du média';
$LANG_confignames['mediagallery']['full_in_popup'] = 'Afficher l’image originale dans une fenêtre contextuelle';
$LANG_confignames['mediagallery']['commentbar'] = 'Afficher la barre complète des commentaires';
$LANG_confignames['mediagallery']['seperator'] = 'Séparateur du fil d’Ariane';
$LANG_confignames['mediagallery']['use_flowplayer'] = 'Lecteur vidéo Flash';
$LANG_confignames['mediagallery']['custom_image_height'] = 'Hauteur d’image personnalisée';
$LANG_confignames['mediagallery']['custom_image_width'] = 'Largeur d’image personnalisée';
$LANG_confignames['mediagallery']['popup_from_album'] = 'Lire les médias audio/vidéo directement depuis la vue album';
$LANG_confignames['mediagallery']['autotag_caption'] = 'Utiliser le titre du média ou de l’album comme légende des autotags';
$LANG_confignames['mediagallery']['random_width'] = 'Largeur du bloc Image aléatoire';
$LANG_confignames['mediagallery']['random_skin'] = 'Habillage de l’image aléatoire';
$LANG_confignames['mediagallery']['truncate_breadcrumb'] = 'Tronquer le fil d’Ariane';
$LANG_confignames['mediagallery']['search_columns'] = 'Colonnes des résultats de recherche';
$LANG_confignames['mediagallery']['search_rows'] = 'Lignes des résultats de recherche';
$LANG_confignames['mediagallery']['search_playback_type'] = 'Type de lecture audio/vidéo des résultats';
$LANG_confignames['mediagallery']['search_enable_views'] = 'Afficher le compteur de vues dans les résultats';
$LANG_confignames['mediagallery']['search_enable_rating'] = 'Afficher la note dans les résultats';
$LANG_confignames['mediagallery']['search_album_skin'] = 'Thème des résultats de recherche';
$LANG_confignames['mediagallery']['search_frame_skin'] = 'Habillage des miniatures des résultats';
$LANG_confignames['mediagallery']['search_tn_size'] = 'Taille des miniatures des résultats';
$LANG_confignames['mediagallery']['def_refresh_rate'] = 'Fréquence d’actualisation';
$LANG_confignames['mediagallery']['def_item_limit'] = 'Nombre maximal d’éléments par cycle';
$LANG_confignames['mediagallery']['def_time_limit'] = 'Temps d’exécution maximal autorisé';
$LANG_confignames['mediagallery']['up_display_rows_enabled'] = 'Autoriser l’utilisateur à définir le nombre de lignes';
$LANG_confignames['mediagallery']['up_display_columns_enabled'] = 'Autoriser l’utilisateur à définir le nombre de colonnes';
$LANG_confignames['mediagallery']['up_av_playback_enabled'] = 'Autoriser l’utilisateur à définir les options de lecture audio/vidéo';
$LANG_confignames['mediagallery']['up_thumbnail_size_enabled'] = 'Autoriser l’utilisateur à définir la taille des miniatures';
$LANG_confignames['mediagallery']['jhead_enabled'] = 'Activer JHEAD';
$LANG_confignames['mediagallery']['jhead_path'] = 'Chemin vers le binaire jhead';
$LANG_confignames['mediagallery']['jpegtran_enabled'] = 'Activer JPEGTRAN';
$LANG_confignames['mediagallery']['jpegtran_path'] = 'Chemin vers le binaire jpegtran';
$LANG_confignames['mediagallery']['ffmpeg_enabled'] = 'Activer FFMPEG';
$LANG_confignames['mediagallery']['ffmpeg_path'] = 'Chemin vers FFMPEG';
$LANG_confignames['mediagallery']['zip_enabled'] = 'Activer les téléversements ZIP';
$LANG_confignames['mediagallery']['zip_path'] = 'Chemin vers le programme de décompression';
$LANG_confignames['mediagallery']['tmp_path'] = 'Chemin du répertoire temporaire';
$LANG_confignames['mediagallery']['ftp_path'] = 'Répertoire FTP';

$mg_fr_album_labels = array(
    'ad_skin' => 'Thème de l’album', 'ad_enable_comments' => 'Autoriser les commentaires',
    'ad_exif_display' => 'Activer EXIF', 'ad_enable_rating' => 'Activer les notes',
    'ad_enable_album_views' => 'Afficher le compteur de vues des albums',
    'ad_enable_views' => 'Afficher le compteur de vues des médias',
    'ad_enable_keywords' => 'Activer les mots-clés', 'ad_display_album_desc' => 'Afficher la description de l’album',
    'ad_filename_title' => 'Utiliser le nom de fichier comme légende', 'ad_enable_rss' => 'Activer le flux de l’album',
    'ad_rsschildren' => 'Inclure les sous-albums dans le flux', 'ad_podcast' => 'Flux podcast',
    'ad_mp3ribbon' => 'Lecteur ruban MP3', 'ad_enable_sort' => 'Activer le tri côté client',
    'ad_album_sort_order' => 'Tri par défaut des albums au téléversement', 'ad_playback_type' => 'Options de lecture audio/vidéo',
    'ad_enable_slideshow' => 'Activer le diaporama', 'ad_enable_random' => 'Inclure dans le bloc Image aléatoire',
    'ad_albums_first' => 'Afficher les sous-albums avant les images', 'ad_allow_download' => 'Autoriser le téléchargement des médias',
    'ad_full_display' => 'Afficher l’image originale', 'ad_tn_size' => 'Taille des miniatures',
    'ad_tn_width' => 'Largeur personnalisée des miniatures', 'ad_tn_height' => 'Hauteur personnalisée des miniatures',
    'ad_max_image_width' => 'Largeur maximale des images (pixels)', 'ad_max_image_height' => 'Hauteur maximale des images (pixels)',
    'ad_max_filesize' => 'Taille maximale des fichiers', 'ad_display_image_size' => 'Taille de l’image affichée',
    'ad_display_rows' => 'Lignes affichées', 'ad_display_columns' => 'Colonnes affichées',
    'ad_image_skin' => 'Habillage de l’image', 'ad_display_skin' => 'Habillage de l’image affichée',
    'ad_album_skin' => 'Habillage de l’album', 'ad_wm_auto' => 'Appliquer automatiquement un filigrane au téléversement',
    'ad_wm_opacity' => 'Opacité du filigrane', 'ad_wm_location' => 'Position du filigrane',
    'ad_wm_id' => 'Image de filigrane', 'ad_member_uploads' => 'Autoriser les utilisateurs enregistrés à téléverser des médias',
    'ad_moderate' => 'Activer la modération pour cet album', 'ad_mod_group_id' => 'Groupe de modération',
    'ad_email_mod' => 'Envoyer un e-mail aux modérateurs lors d’une soumission', 'ad_group_id' => 'Groupe',
    'ad_permissions' => 'Permissions par défaut de l’album'
);
foreach ($mg_fr_album_labels as $mg_fr_key => $mg_fr_value) {
    $LANG_confignames['mediagallery'][$mg_fr_key] = $mg_fr_value;
}
unset($mg_fr_album_labels, $mg_fr_key, $mg_fr_value);

$LANG_configsubgroups['mediagallery']['sg_main'] = 'Paramètres système';
$LANG_configsubgroups['mediagallery']['sg_album'] = 'Paramètres par défaut des albums';
$LANG_configsubgroups['mediagallery']['sg_av'] = 'Paramètres audio/vidéo par défaut';
$LANG_configsubgroups['mediagallery']['sg_member_album'] = 'Albums des membres';

$LANG_tab['mediagallery']['tab_main'] = 'Options générales';
$LANG_tab['mediagallery']['tab_display'] = 'Options d’affichage';
$LANG_tab['mediagallery']['tab_batch'] = 'Options des traitements par lot';
$LANG_tab['mediagallery']['tab_userprefs'] = 'Préférences utilisateur';
$LANG_tab['mediagallery']['tab_graphics'] = 'Bibliothèque graphique';
$LANG_tab['mediagallery']['tab_album'] = 'Paramètres par défaut des albums';
$LANG_tab['mediagallery']['tab_watermark'] = 'Filigrane';
$LANG_tab['mediagallery']['tab_allowedmediatypes'] = 'Types de médias autorisés';
$LANG_tab['mediagallery']['tab_useruploads'] = 'Téléversements des utilisateurs';
$LANG_tab['mediagallery']['tab_accessrights'] = 'Droits d’accès';
$LANG_tab['mediagallery']['tab_wmedia'] = 'Windows Media';
$LANG_tab['mediagallery']['tab_quicktime'] = 'QuickTime';
$LANG_tab['mediagallery']['tab_mp3'] = 'MP3';
$LANG_tab['mediagallery']['tab_flashmedia'] = 'Médias Flash';
$LANG_tab['mediagallery']['tab_member_albums'] = 'Albums des membres';
$LANG_tab['mediagallery']['tab_member_allowedmediatypes'] = 'Types de médias autorisés';
$LANG_tab['mediagallery']['tab_member_album_attributes'] = 'Attributs des albums';
$LANG_tab['mediagallery']['tab_member_useruploads'] = 'Téléversements des utilisateurs';
$LANG_tab['mediagallery']['tab_member_accessrights'] = 'Droits d’accès';

$LANG_fs['mediagallery']['fs_main'] = 'Options générales';
$LANG_fs['mediagallery']['fs_autotag'] = 'Paramètres par défaut des autotags';
$LANG_fs['mediagallery']['fs_rssfeed'] = 'Options RSS';
$LANG_fs['mediagallery']['fs_display'] = 'Options d’affichage';
$LANG_fs['mediagallery']['fs_searchresults'] = 'Options des résultats de recherche';
$LANG_fs['mediagallery']['fs_batch'] = 'Options des traitements par lot';
$LANG_fs['mediagallery']['fs_userprefs'] = 'Préférences utilisateur';
$LANG_fs['mediagallery']['fs_graphics'] = 'Bibliothèque graphique';
$LANG_fs['mediagallery']['fs_album'] = 'Attributs de l’album';
$LANG_fs['mediagallery']['fs_root_album'] = 'Album racine';
$LANG_fs['mediagallery']['fs_watermark'] = 'Filigrane';
$LANG_fs['mediagallery']['fs_allowedmediatypes'] = 'Types de médias autorisés';
$LANG_fs['mediagallery']['fs_image_format'] = 'Image';
$LANG_fs['mediagallery']['fs_audio_format'] = 'Audio';
$LANG_fs['mediagallery']['fs_video_format'] = 'Vidéo';
$LANG_fs['mediagallery']['fs_other_format'] = 'Autre';
$LANG_fs['mediagallery']['fs_useruploads'] = 'Téléversements des utilisateurs';
$LANG_fs['mediagallery']['fs_accessrights'] = 'Droits d’accès';
$LANG_fs['mediagallery']['fs_permissions'] = 'Permissions de l’album';
$LANG_fs['mediagallery']['fs_wmedia'] = 'Windows Media';
$LANG_fs['mediagallery']['fs_quicktime'] = 'QuickTime';
$LANG_fs['mediagallery']['fs_mp3'] = 'MP3';
$LANG_fs['mediagallery']['fs_flashmedia'] = 'Médias Flash';
$LANG_fs['mediagallery']['fs_member_albums'] = 'Albums des membres';
$LANG_fs['mediagallery']['fs_member_allowedmediatypes'] = 'Types de médias autorisés';
$LANG_fs['mediagallery']['fs_member_album_attributes'] = 'Attributs des albums';
$LANG_fs['mediagallery']['fs_member_useruploads'] = 'Téléversements des utilisateurs';
$LANG_fs['mediagallery']['fs_member_permissions'] = 'Permissions des albums membres';

// Replace the small set of configuration choices that are hard-coded in the English language file.
$LANG_configselects['mediagallery'][0] = array('Vrai' => 1, 'Faux' => 0);
$LANG_configselects['mediagallery'][1] = array('Vrai' => TRUE, 'Faux' => FALSE);
$LANG_configselects['mediagallery'][5] = array('Haut de page' => 1, 'Après l’article mis en avant' => 2, 'Bas de page' => 3);
$LANG_configselects['mediagallery'][6] = array('Blocs de gauche' => 'leftblocks', 'Blocs de droite' => 'rightblocks', 'Tous les blocs' => 'allblocks', 'Aucun bloc' => 'noblocks');
$LANG_configselects['mediagallery'][7] = array('Aucun' => 'none', 'Auto' => 'auto', 'Gauche' => 'left', 'Droite' => 'right', 'Centre' => 'center');
$LANG_configselects['mediagallery'][8] = array('Miniature' => 'tn', 'Image d’affichage' => 'disp', 'Image originale' => 'orig');
$LANG_configselects['mediagallery'][9] = array('Vrai' => 1, 'Faux' => 0, 'Lightbox' => 2);
$LANG_configselects['mediagallery'][12] = array('Aucun accès' => 0, 'Lecture seule' => 2, 'Lecture-écriture' => 3);
$LANG_configselects['mediagallery'][24] = array('Aucun' => 'none', 'Mini' => 'mini', 'Complet' => 'full');
'''

text += block + '\n'

# Keep only the last direct LANG_MG assignment for a key.
lines = text.splitlines()
last = {}
for index, line in enumerate(lines):
    match = re.match(r"\$(LANG_MG\d+)\['([^']+)'\]\s*=", line)
    if match:
        last[(match.group(1), match.group(2))] = index
out = []
for index, line in enumerate(lines):
    match = re.match(r"\$(LANG_MG\d+)\['([^']+)'\]\s*=", line)
    if match and last[(match.group(1), match.group(2))] != index:
        continue
    out.append(line)
path.write_text('\n'.join(out) + '\n', encoding='utf-8')
