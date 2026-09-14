from pathlib import Path


def replace_required(path, old, new, all_occurrences=True):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit('Expected text not found in %s: %s' % (path, old))
    s = s.replace(old, new) if all_occurrences else s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')


def patch_bytes(path, marker, addition, once=False):
    p = Path(path)
    data = p.read_bytes()
    marker_b = marker.encode('ascii')
    addition_b = addition.encode('ascii')
    if addition_b in data:
        return
    count = data.count(marker_b)
    if count == 0:
        raise SystemExit('Binary marker not found in %s' % path)
    if once:
        data = data.replace(marker_b, marker_b + addition_b, 1)
    else:
        data = data.replace(marker_b, marker_b + addition_b)
    p.write_bytes(data)

# Canonical language keys.
for filename, values in [
    ('language/english_utf-8.php', {
        'aria_media_actions': 'Media actions and navigation',
        'media_id_label': 'Media ID',
        'aria_search_results_navigation': 'Search results navigation',
        'aria_album_navigation': 'Album navigation',
        'aria_media_list': 'Media list',
    }),
    ('language/french_france_utf-8.php', {
        'aria_media_actions': 'Actions et navigation du média',
        'media_id_label': 'ID du média',
        'aria_search_results_navigation': 'Navigation des résultats de recherche',
        'aria_album_navigation': 'Navigation de l’album',
        'aria_media_list': 'Liste des médias',
    }),
]:
    p = Path(filename)
    s = p.read_text(encoding='utf-8').rstrip() + '\n'
    for key, value in values.items():
        needle = "$LANG_MG03['%s']" % key
        if needle not in s:
            safe = value.replace("'", "\\'")
            s += "$LANG_MG03['%s'] = '%s';\n" % (key, safe)
    p.write_text(s, encoding='utf-8')

# Historical PHP files may contain legacy non-UTF-8 bytes. Patch only ASCII
# fragments so their original byte encoding remains untouched.
patch_bytes(
    'include/lib-media.php',
    "        'lang_search'         => $LANG_MG01['search'],\n",
    "        'lang_aria_breadcrumb' => $LANG_MG03['aria_breadcrumb'],\n"
    "        'lang_aria_media_actions' => $LANG_MG03['aria_media_actions'],\n"
    "        'lang_media_id' => $LANG_MG03['media_id_label'],\n",
    once=True,
)
patch_bytes(
    'public_html/search.php',
    "        'lang_search'          => $LANG_MG01['search'],\n",
    "        'lang_aria_search_results_navigation' => $LANG_MG03['aria_search_results_navigation'],\n",
    once=False,
)
patch_bytes(
    'public_html/album.php',
    "    'lang_aria_album_pagination_info' => $LANG_MG03['aria_album_pagination_info'],\n",
    "    'lang_aria_album_navigation' => $LANG_MG03['aria_album_navigation'],\n"
    "    'lang_aria_media_list' => $LANG_MG03['aria_media_list'],\n",
    once=True,
)

# Active media templates.
for path in ['templates/view_image.thtml', 'templates/view_video.thtml', 'templates/view_audio.thtml']:
    replace_required(path, 'aria-label="Breadcrumb"', 'aria-label="{lang_aria_breadcrumb}"')
    replace_required(path, 'aria-label="Media actions and navigation"', 'aria-label="{lang_aria_media_actions}"')

replace_required('templates/view_image.thtml', '<summary>Media ID</summary>', '<summary>{lang_media_id}</summary>')
for path in ['templates/view_video.thtml', 'templates/view_audio.thtml']:
    replace_required(path, '<strong>ID:</strong>', '<strong>{lang_media_id}:</strong>')

replace_required('templates/search_page.thtml', 'aria-label="Search results navigation"', 'aria-label="{lang_aria_search_results_navigation}"')

# Alternate active album themes.
theme_paths = [
    'templates/themes/jquery_ad-gallery/album_page.thtml',
    'templates/themes/filelist/album_page.thtml',
    'templates/themes/simpleviewer/album_page.thtml',
    'templates/themes/jquery_colorbox/album_page.thtml',
    'templates/themes/podcast/album_page.thtml',
]
for path in theme_paths:
    p = Path(path)
    if not p.exists():
        continue
    s = p.read_text(encoding='utf-8')
    s = s.replace('aria-label="Breadcrumb"', 'aria-label="{lang_aria_breadcrumb}"')
    s = s.replace('aria-label="Album navigation"', 'aria-label="{lang_aria_album_navigation}"')
    s = s.replace('aria-label="Media list"', 'aria-label="{lang_aria_media_list}"')
    p.write_text(s, encoding='utf-8')
