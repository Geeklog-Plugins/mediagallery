from pathlib import Path
import re


def append_keys(path, group, values):
    p = Path(path)
    s = p.read_text(encoding='utf-8').rstrip() + '\n'
    for key, value in values.items():
        needle = "$%s['%s']" % (group, key)
        if needle not in s:
            safe = value.replace('\\', '\\\\').replace("'", "\\'")
            s += "$%s['%s'] = '%s';\n" % (group, key, safe)
    p.write_text(s, encoding='utf-8')


def replace_text(path, old, new, count=0):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit('Expected text not found in %s: %s' % (path, old[:100]))
    s = s.replace(old, new, count) if count else s.replace(old, new)
    p.write_text(s, encoding='utf-8')


def replace_bytes(path, old, new, count=0):
    p = Path(path)
    data = p.read_bytes()
    a = old.encode('ascii')
    b = new.encode('ascii')
    if a not in data:
        raise SystemExit('Expected byte marker not found in %s' % path)
    data = data.replace(a, b, count) if count else data.replace(a, b)
    p.write_bytes(data)

# ---------------------------------------------------------------------------
# Canonical language keys
# ---------------------------------------------------------------------------
append_keys('language/english_utf-8.php', 'LANG_MG03', {
    'open_slideshow': 'Open slideshow',
    'open_album': 'Open this MediaGallery album',
    'download_xspf': 'Download the XSPF playlist',
    'slideshow_pagination': 'Slideshow pagination',
    'media_count_label': 'Media count',
    'flv_unsupported': 'FLV playback is no longer supported by modern browsers.',
    'rating_action_invalid': 'Invalid rating action.',
    'rating_login_required': 'Please log in before rating this media.',
    'rating_request_error': 'An error occurred while processing the rating request.',
    'rating_already_voted': 'You have already voted.',
    'rating_speedlimit': 'Please wait before rating again.',
    'rating_thanks': 'Thanks for your rating.',
    'rating_received': 'Rating received: %s',
    'xml_slideshow_description': 'XML Mini Slideshow for Media Gallery',
})
append_keys('language/french_france_utf-8.php', 'LANG_MG03', {
    'open_slideshow': 'Ouvrir le diaporama',
    'open_album': 'Ouvrir cet album Media Gallery',
    'download_xspf': 'Télécharger la liste de lecture XSPF',
    'slideshow_pagination': 'Pagination du diaporama',
    'media_count_label': 'Nombre de médias',
    'flv_unsupported': 'La lecture FLV n’est plus prise en charge par les navigateurs modernes.',
    'rating_action_invalid': 'Action de notation non valide.',
    'rating_login_required': 'Connectez-vous avant de noter ce média.',
    'rating_request_error': 'Une erreur est survenue lors du traitement de la note.',
    'rating_already_voted': 'Vous avez déjà voté.',
    'rating_speedlimit': 'Veuillez patienter avant de noter à nouveau.',
    'rating_thanks': 'Merci pour votre note.',
    'rating_received': 'Note reçue : %s',
    'xml_slideshow_description': 'Mini-diaporama XML de Media Gallery',
})

export_en = {
    'export_title': 'Media Gallery Export',
    'export_intro_1': 'The Media Gallery export routine prepares your media files for use on your local computer.',
    'export_intro_2': 'First download the original media files to a temporary directory on your local computer, for example by FTP from mediagallery/mediaobjects/orig/.',
    'export_intro_3': 'Then run this export routine to create a script that copies or moves the media files into directories named after your albums.',
    'export_intro_4': 'The source directory is the temporary directory containing the downloaded media files. The destination directory is where the album directories will be created.',
    'export_intro_5': 'Select the operating system on which the generated script will run. For macOS, select Unix.',
    'export_docs': 'Online documentation',
    'export_destination_system': 'Destination system',
    'export_windows': 'Windows',
    'export_unix': 'Unix',
    'export_move_or_copy': 'Move or copy',
    'export_move': 'Move',
    'export_copy': 'Copy',
    'export_temp_directory': 'Temporary directory on destination system',
    'export_base_directory': 'Base directory',
    'export_process': 'Create export script',
    'export_ready_title': 'Media Gallery export script ready for download',
    'export_ready_message': 'Media Gallery has finished creating the export script. Download it to your local system, then run it.',
    'export_download': 'Download',
}
export_fr = {
    'export_title': 'Export Media Gallery',
    'export_intro_1': 'La procédure d’export Media Gallery prépare vos fichiers média pour une utilisation sur votre ordinateur.',
    'export_intro_2': 'Commencez par télécharger les médias originaux dans un répertoire temporaire de votre ordinateur, par exemple par FTP depuis mediagallery/mediaobjects/orig/.',
    'export_intro_3': 'Lancez ensuite cet export pour créer un script qui copiera ou déplacera les médias dans des répertoires portant le nom de vos albums.',
    'export_intro_4': 'Le répertoire source est le répertoire temporaire contenant les médias téléchargés. Le répertoire de destination est celui où seront créés les répertoires des albums.',
    'export_intro_5': 'Sélectionnez le système d’exploitation sur lequel le script généré sera exécuté. Pour macOS, choisissez Unix.',
    'export_docs': 'Documentation en ligne',
    'export_destination_system': 'Système de destination',
    'export_windows': 'Windows',
    'export_unix': 'Unix',
    'export_move_or_copy': 'Déplacer ou copier',
    'export_move': 'Déplacer',
    'export_copy': 'Copier',
    'export_temp_directory': 'Répertoire temporaire sur le système de destination',
    'export_base_directory': 'Répertoire de base',
    'export_process': 'Créer le script d’export',
    'export_ready_title': 'Le script d’export Media Gallery est prêt',
    'export_ready_message': 'Media Gallery a terminé la création du script d’export. Téléchargez-le sur votre ordinateur, puis exécutez-le.',
    'export_download': 'Télécharger',
}
append_keys('language/english_utf-8.php', 'LANG_MG01', export_en)
append_keys('language/french_france_utf-8.php', 'LANG_MG01', export_fr)

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
replace_text('templates/fsat.thtml', '>Open slideshow</a>', '>{lang_open_slideshow}</a>')
replace_text('templates/xspf_radio.thtml', '>Open this MediaGallery album</a>', '>{lang_open_album}</a>')
replace_text('templates/xspf_radio.thtml', '>Download the XSPF playlist</a>', '>{lang_download_xspf}</a>')
replace_text('templates/playall_xspf.thtml', '>Open this MediaGallery album</a>', '>{lang_open_album}</a>')
replace_text('templates/playall_xspf.thtml', '>Download the XSPF playlist</a>', '>{lang_download_xspf}</a>')
replace_text('templates/view_asf.thtml', '>Download media</a>', '>{lang_download}</a>')
replace_text('templates/view_swf.thtml', '>Download legacy SWF media</a>', '>{lang_download}</a>')
replace_text('templates/view_mp3_wmp.thtml', '>Download audio</a>', '>{lang_download}</a>')
replace_text('templates/view_mp3_qt.thtml', '>Download audio</a>', '>{lang_download}</a>')
replace_text('templates/sessions.thtml', '>Continue</a>', '>{lang_continue}</a>')
replace_text('templates/album_page_album_cell.thtml', 'aria-label="Media count"', 'aria-label="{lang_media_count}"')
replace_text('templates/flvfp.thtml', 'FLV playback is no longer supported by modern browsers.', '{lang_flv_unsupported}')

# Export template: all visible prose comes from language variables.
Path('templates/export.thtml').write_text('''<div class="plugin">\n<h1>{lang_export_title}</h1>\n<p>{lang_export_intro_1}</p>\n<p>{lang_export_intro_2}</p>\n<p>{lang_export_intro_3}</p>\n<p>{lang_export_intro_4}</p>\n<p>{lang_export_intro_5}</p>\n<p><a href="http://www.gllabs.org/wiki/doku.php?id=mediagallery:export">{lang_export_docs}</a></p>\n<form method="post" action="{s_form_action}" name="mgexport" enctype="multipart/form-data" id="mgexport" class="uk-form">\n  <table class="mg_admin_table">\n    <tr><td class="mg_alignright" width="35%">{lang_export_destination_system}:</td><td>\n      <input type="radio" id="mg-export-windows" name="unix" value="0"> <label for="mg-export-windows">{lang_export_windows}</label>&nbsp;&nbsp;\n      <input type="radio" id="mg-export-unix" name="unix" value="1"> <label for="mg-export-unix">{lang_export_unix}</label>\n    </td></tr>\n    <tr><td class="mg_alignright" width="35%">{lang_export_move_or_copy}:</td><td>\n      <input type="radio" id="mg-export-move" name="moveorcopy" value="0"> <label for="mg-export-move">{lang_export_move}</label>&nbsp;&nbsp;\n      <input type="radio" id="mg-export-copy" name="moveorcopy" value="1"> <label for="mg-export-copy">{lang_export_copy}</label>\n    </td></tr>\n    <tr><td class="mg_alignright" width="35%"><label for="mg-export-srcroot">{lang_export_temp_directory}:</label></td><td>\n      <input type="text" id="mg-export-srcroot" name="srcroot" size="40" value="">\n    </td></tr>\n    <tr><td class="mg_alignright" width="35%"><label for="mg-export-destroot">{lang_export_base_directory}:</label></td><td>\n      <input type="text" id="mg-export-destroot" name="destroot" size="40" value="">\n    </td></tr>\n  </table>\n  <div class="mg_submit_center"><button type="submit" name="mode" value="process">{lang_export_process}</button></div>\n</form>\n</div>\n''', encoding='utf-8')

# ---------------------------------------------------------------------------
# Renderer wiring
# ---------------------------------------------------------------------------
# Autotags is UTF-8.
p = Path('include/autotags.php')
s = p.read_text(encoding='utf-8')
s = s.replace("                'xhtml'    => XHTML,\n            ));\n            $media = $V->finish($V->parse('output', 'xspf'));",
              "                'xhtml'    => XHTML,\n                'lang_open_album' => $LANG_MG03['open_album'],\n                'lang_download_xspf' => $LANG_MG03['download_xspf'],\n            ));\n            $media = $V->finish($V->parse('output', 'xspf'));", 1)
s = s.replace("                        'xhtml'              => XHTML,\n                    ));\n                    $media = $V->finish($V->parse('output', 'video'));",
              "                        'xhtml'              => XHTML,\n                        'lang_download'       => $LANG_MG03['download'],\n                    ));\n                    $media = $V->finish($V->parse('output', 'video'));", 1)
# SWF block: anchor label.
needle = "                        'movie'        => $orig_media_url,\n                        'xhtml'        => XHTML,\n                    ));"
if needle in s:
    s = s.replace(needle, "                        'movie'        => $orig_media_url,\n                        'xhtml'        => XHTML,\n                        'lang_download'=> $LANG_MG03['download'],\n                    ));", 1)
# FLV player.
needle = "                        'lang_noflash'      => $LANG_MG03['no_flash'],\n"
if needle in s and "'lang_flv_unsupported'" not in s:
    # first occurrence after flvfp is not trivial; adding alongside all noflash vars is harmless.
    s = s.replace(needle, needle + "                        'lang_flv_unsupported' => $LANG_MG03['flv_unsupported'],\n")
# WMA/MP3 fallback.
needle = "                        'movie'             => $orig_media_url,\n                        'xhtml'             => XHTML,\n                    ));\n                    $media = $V->finish($V->parse('output', 'audio'));"
if needle in s:
    s = s.replace(needle, "                        'movie'             => $orig_media_url,\n                        'xhtml'             => XHTML,\n                        'lang_download'      => $LANG_MG03['download'],\n                    ));\n                    $media = $V->finish($V->parse('output', 'audio'));", 1)
# Legacy slideshow autotag.
needle = "                'xhtml'         => XHTML,\n            ));\n            $swfobject = $T->finish($T->parse('output', 'fslideshow'));"
if needle in s:
    s = s.replace(needle, "                'xhtml'         => XHTML,\n                'lang_open_slideshow' => $LANG_MG03['open_slideshow'],\n            ));\n            $swfobject = $T->finish($T->parse('output', 'fslideshow'));", 1)
p.write_text(s, encoding='utf-8')

# lib-media contains legacy bytes; patch ASCII only.
p = Path('include/lib-media.php')
data = p.read_bytes()
data = data.replace(
    b"function MG_displayASF($I, $opt=array())\n{\n    global $_TABLES, $_CONF, $_MG_CONF;",
    b"function MG_displayASF($I, $opt=array())\n{\n    global $_TABLES, $_CONF, $_MG_CONF, $LANG_MG03;",
    1,
)
data = data.replace(
    b"                'movie'              => Media::getFileUrl('orig', $I['media_filename'], $I['media_mime_ext']),\n            ));",
    b"                'movie'              => Media::getFileUrl('orig', $I['media_filename'], $I['media_mime_ext']),\n                'lang_download'      => $LANG_MG03['download'],\n            ));",
    1,
)
p.write_bytes(data)

# playall page.
p = Path('public_html/playall.php')
s = p.read_text(encoding='utf-8')
needle = "    'return_to_album' => $LANG_MG03['return_to_album'],\n"
if needle in s and "'lang_open_album'" not in s:
    s = s.replace(needle, needle + "    'lang_open_album' => $LANG_MG03['open_album'],\n    'lang_download_xspf' => $LANG_MG03['download_xspf'],\n", 1)
p.write_text(s, encoding='utf-8')

# Sessions admin.
p = Path('admin/sessions.php')
s = p.read_text(encoding='utf-8')
needle = "        'lang_action'               => $LANG_MG01['action'],\n"
if needle in s and "'lang_continue'" not in s:
    s = s.replace(needle, needle + "        'lang_continue'             => $LANG_MG01['continue'],\n", 1)
p.write_text(s, encoding='utf-8')

# Album cell.
p = Path('include/common.php')
s = p.read_text(encoding='utf-8')
needle = "        'lang_subalbums'       => (($subalbums > 0) ? $LANG_MG01['subalbums'] : ''),\n"
if needle in s and "'lang_media_count'" not in s:
    s = s.replace(needle, needle + "        'lang_media_count'      => $LANG_MG03['media_count_label'],\n", 1)
p.write_text(s, encoding='utf-8')

# Export admin: localized success screen and template variables.
p = Path('admin/export.php')
s = p.read_text(encoding='utf-8')
s = s.replace("    $display = '<h1>Media Gallery Export Script Ready for Download</h1>';\n    $display .= 'Media Gallery has completed building the import script.  Use the download button below to download the script to your local system, then run.';",
              "    $display = '<h1>' . $LANG_MG01['export_ready_title'] . '</h1>';\n    $display .= '<p>' . $LANG_MG01['export_ready_message'] . '</p>';", 1)
s = s.replace("    $display .= '<input type=\"submit\" name=\"mode\" value=\"download\">';",
              "    $display .= '<button type=\"submit\" name=\"mode\" value=\"download\">' . $LANG_MG01['export_download'] . '</button>';", 1)
needle = "    's_form_action' => $_MG_CONF['admin_url'] . 'export.php',\n"
if needle in s and "'lang_export_title'" not in s:
    vars = ''.join("    'lang_%s' => $LANG_MG01['%s'],\n" % (k, k) for k in export_en)
    s = s.replace(needle, needle + vars, 1)
p.write_text(s, encoding='utf-8')

# Rating AJAX responses.
p = Path('public_html/rater.php')
s = p.read_text(encoding='utf-8')
s = s.replace("function rater_sendResponse($response) {\n    if ($response['error'] == true) {\n        $response['server'] = '<strong>ERROR :</strong> ' . $response['server'];",
              "function rater_sendResponse($response) {\n    global $LANG_MG02;\n    if ($response['error'] == true) {\n        $response['server'] = '<strong>' . $LANG_MG02['error'] . '</strong> ' . $response['server'];", 1)
s = s.replace("'server' => '\"action\" post data not equal to \\'rating\\''", "'server' => $LANG_MG03['rating_action_invalid']")
s = s.replace("'server' => 'Sorry, user must login first'", "'server' => $LANG_MG03['rating_login_required']")
s = s.replace("'server' => 'An error occured during the request'", "'server' => $LANG_MG03['rating_request_error']")
s = s.replace("'server' => 'You have already voted'", "'server' => $LANG_MG03['rating_already_voted']")
s = s.replace("'server' => 'Speed limit error'", "'server' => $LANG_MG03['rating_speedlimit']")
s = s.replace("    'server' => '<strong>Thanks for your rate.</strong><br' . XHTML . '/>'\n              . '<strong>Rate received : ' . $vote_sent . '</strong>')",
              "    'server' => '<strong>' . $LANG_MG03['rating_thanks'] . '</strong><br' . XHTML . '/>'\n              . '<strong>' . sprintf($LANG_MG03['rating_received'], $vote_sent) . '</strong>')", 1)
p.write_text(s, encoding='utf-8')

# XML metadata (not a page label, but localized consistently).
p = Path('public_html/xml.php')
s = p.read_text(encoding='utf-8')
s = s.replace('$xml .= "        <description>XML Mini SlideShow for Media Gallery</description>\\n";',
              '$xml .= "        <description>" . htmlspecialchars($LANG_MG03[\'xml_slideshow_description\'], ENT_QUOTES, \'UTF-8\') . "</description>\\n";', 1)
p.write_text(s, encoding='utf-8')
