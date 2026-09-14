from pathlib import Path


def replace_once(path, old, new, encoding='utf-8'):
    p = Path(path)
    s = p.read_text(encoding=encoding)
    if new not in s:
        if old not in s:
            raise SystemExit('pattern not found in ' + path)
        s = s.replace(old, new, 1)
    p.write_text(s, encoding=encoding)


# Preserve historical lib-media.php byte encoding.
p = Path('include/lib-media.php')
s = p.read_text(encoding='latin-1')
marker = "    $media = $media_array[$key];\n"
insert = marker + "\n    // One meaningful title is reused by the H1, page title and comments.\n    $media_title_plain = trim(strip_tags(isset($media['media_title']) ? $media['media_title'] : ''));\n    if ($media_title_plain === '') {\n        $media_title_plain = $LANG_MG03['image'] . ' ' . ($key + 1) . ' - ' . strip_tags($mg_album->title);\n    }\n    $media_title_display = (isset($media['media_title']) && trim(strip_tags($media['media_title'])) !== '')\n        ? PLG_replaceTags($media['media_title'])\n        : MG_escapeHTML($media_title_plain);\n"
if '$media_title_plain = trim(strip_tags' not in s:
    if marker not in s:
        raise SystemExit('media array marker not found')
    s = s.replace(marker, insert, 1)
s = s.replace("    if ($mg_album->enable_rating > 0) {", "    if ($mg_album->enable_rating > 0 && intval($media['media_votes']) > 0) {", 1)
s = s.replace("        'media_title'         => (isset($media['media_title']) && $media['media_title'] != ' ') ? PLG_replaceTags($media['media_title']) : '',", "        'media_title'         => $media_title_display,", 1)
s = s.replace("CMT_userComments($sid, $media['media_title'], 'mediagallery',", "CMT_userComments($sid, $media_title_plain, 'mediagallery',", 1)
s = s.replace("return array(strip_tags($media['media_title']), $retval, $aid);", "return array($media_title_plain, $retval, $aid);", 1)
p.write_text(s, encoding='latin-1')

# Keep JSON-LD title aligned with the visible/page fallback.
p = Path('public_html/media.php')
s = p.read_text(encoding='utf-8')
marker = "if ($metaResult !== false && DB_numRows($metaResult) === 1) {\n    $mediaMeta = DB_fetchArray($metaResult);\n}\n"
add = marker + "if (!empty($mediaMeta) && trim(strip_tags(isset($mediaMeta['media_title']) ? $mediaMeta['media_title'] : '')) === '' && $ptitle !== '') {\n    $mediaMeta['media_title'] = $ptitle;\n}\n"
if "$mediaMeta['media_title'] = $ptitle;" not in s:
    if marker not in s:
        raise SystemExit('media meta marker not found')
    s = s.replace(marker, add, 1)
p.write_text(s, encoding='utf-8')

old_album_search = '''    <div class="mg_search">\n      <form name="mgsearch" method="post" action="{site_url}/search.php" class="uk-form" role="search">\n        <div>\n          <label for="mg-search-keywords" class="mg-visually-hidden">{lang_search}</label>\n          <input id="mg-search-keywords" type="search" name="keywords" value="{keywords}" aria-label="{lang_search}"{xhtml}>\n          <input type="hidden" name="mode" value="search"{xhtml}>\n          <input type="hidden" name="swhere" value="0"{xhtml}>\n          <input type="submit" value="{lang_search}"{xhtml}>\n        </div>\n      </form>\n    </div>'''
new_album_search = '''    <details class="mg-compact-search">\n      <summary>{lang_search}</summary>\n      <div class="mg_search">\n        <form name="mgsearch" method="post" action="{site_url}/search.php" class="uk-form" role="search">\n          <div>\n            <label for="mg-search-keywords" class="mg-visually-hidden">{lang_search}</label>\n            <input id="mg-search-keywords" type="search" name="keywords" value="{keywords}" aria-label="{lang_search}"{xhtml}>\n            <input type="hidden" name="mode" value="search"{xhtml}>\n            <input type="hidden" name="swhere" value="0"{xhtml}>\n            <input type="submit" value="{lang_search}"{xhtml}>\n          </div>\n        </form>\n      </div>\n    </details>'''
replace_once('templates/album_page.thtml', old_album_search, new_album_search)

old_media_search = '''  <div class="mg_search">\n    <form name="mgsearch" method="post" action="{site_url}/search.php" class="uk-form" role="search"><div>\n      <label for="mg-media-search-keywords" class="mg-visually-hidden">{lang_search}</label>\n      <input id="mg-media-search-keywords" type="search" name="keywords" value="{keywords}" aria-label="{lang_search}"{xhtml}>\n      <input type="hidden" name="mode" value="search"{xhtml}>\n      <input type="hidden" name="swhere" value="0"{xhtml}>\n      <input type="submit" value="{lang_search}"{xhtml}>\n    </div></form>\n  </div>'''
new_media_search = '''  <details class="mg-compact-search">\n    <summary>{lang_search}</summary>\n    <div class="mg_search">\n      <form name="mgsearch" method="post" action="{site_url}/search.php" class="uk-form" role="search"><div>\n        <label for="mg-media-search-keywords" class="mg-visually-hidden">{lang_search}</label>\n        <input id="mg-media-search-keywords" type="search" name="keywords" value="{keywords}" aria-label="{lang_search}"{xhtml}>\n        <input type="hidden" name="mode" value="search"{xhtml}>\n        <input type="hidden" name="swhere" value="0"{xhtml}>\n        <input type="submit" value="{lang_search}"{xhtml}>\n      </div></form>\n    </div>\n  </details>'''
replace_once('templates/view_image.thtml', old_media_search, new_media_search)
replace_once('templates/view_image.thtml', '<h1 class="mg_media_title">{!if media_title}{media_title}{!else}{album_title}{!endif}</h1>', '<h1 class="mg_media_title">{media_title}</h1>')

p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('<span><strong>{lang_views}</strong> {views}</span>', '<span class="mg-card-album-views"><span class="mg-visually-hidden">{lang_views}: </span>{views}</span>')
p.write_text(s, encoding='utf-8')

# Prefer originals for immersive slideshows when permissions/config allow it.
p = Path('public_html/slideshow.php')
s = p.read_text(encoding='utf-8')
s = s.replace("$full      = COM_applyFilter(COM_getArgument('f'),    true);", "$fullArg   = COM_getArgument('f');\n$full      = ($fullArg === '') ? 1 : COM_applyFilter($fullArg, true);", 1)
p.write_text(s, encoding='utf-8')

p = Path('templates/slideshow.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('''      <button class="mg-slideshow-play" type="button" id="mgSlidePlay" aria-pressed="true">\n        <span id="mgSlidePlayText">{stop}</span>\n      </button>''', '''      <button class="mg-slideshow-play" type="button" id="mgSlidePlay" aria-pressed="true" aria-label="{stop}" title="{stop}">\n        <span id="mgSlidePlayText" aria-hidden="true">&#9208;</span>\n      </button>''', 1)
s = s.replace("        playText.textContent = playing ? '{stop}' : '{play}';\n        playButton.setAttribute('aria-pressed', playing ? 'true' : 'false');", "        playText.textContent = playing ? '\\u23f8' : '\\u25b6';\n        playButton.setAttribute('aria-pressed', playing ? 'true' : 'false');\n        playButton.setAttribute('aria-label', playing ? '{stop}' : '{play}');\n        playButton.setAttribute('title', playing ? '{stop}' : '{play}');", 1)
p.write_text(s, encoding='utf-8')

# Final visual overrides.
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 final visual polish */'
if marker not in s:
    s += r'''

/* MediaGallery 1.8 final visual polish */
.mg-compact-search { position: relative; flex: 0 0 auto; }
.mg-compact-search > summary {
  display: inline-flex; align-items: center; min-height: 2.25rem;
  padding: .35rem .65rem; border: 1px solid rgba(127,127,127,.3);
  border-radius: .45rem; background: rgba(255,255,255,.62);
  cursor: pointer; font-weight: 600; list-style: none;
}
.mg-compact-search > summary::-webkit-details-marker { display: none; }
.mg-compact-search > summary::before { content: "\2315"; margin-right: .35rem; font-size: .95em; opacity: .72; }
.mg-compact-search[open] > summary { background: rgba(255,255,255,.9); }
.mg-compact-search .mg_search {
  position: absolute; z-index: 30; top: calc(100% + .4rem); right: 0;
  width: min(26rem, calc(100vw - 2rem)); padding: .55rem;
  border: 1px solid rgba(127,127,127,.22); border-radius: .6rem;
  background: rgba(255,255,255,.98); box-shadow: 0 .65rem 2rem rgba(0,0,0,.12);
}
.mg-compact-search .mg_search form > div { display: flex; gap: .4rem; align-items: center; }
.mg-compact-search .mg_search input[type="search"] { flex: 1 1 auto; min-width: 0; }
.mg-compact-search .mg_search input[type="submit"] { flex: 0 0 auto; padding-inline: .75rem; }

.mg-album-page-header, .mg_media_header { padding-block: .55rem; }
.mg-album-controls { flex: 0 1 auto; gap: .4rem; }
.mg-album-controls .mg_adminbox { flex: 0 1 15rem; }
.mg-album-controls select { min-width: 9rem; }
.mg-album-inline-actions a { opacity: .76; text-decoration: none; transition: opacity .18s ease; }
.mg-album-inline-actions a:hover, .mg-album-inline-actions a:focus-visible { opacity: 1; text-decoration: underline; }

.mg-media-toolbar { margin-block: .45rem .9rem; padding: .25rem 0; }
.mg-media-pagination .mg-action-nav {
  min-height: 2rem; padding: .25rem .55rem; border: 1px solid rgba(127,127,127,.24);
  border-radius: .4rem; background: rgba(255,255,255,.45); text-decoration: none;
}
.mg-media-actions { gap: .75rem; }
.mg-media-actions .mg-action-secondary {
  padding: .2rem 0; border: 0; background: transparent; box-shadow: none;
  opacity: .74; text-decoration: none;
}
.mg-media-actions .mg-action-secondary:hover, .mg-media-actions .mg-action-secondary:focus-visible { opacity: 1; text-decoration: underline; }
.mg-media-actions .mg-action-admin { font-weight: 700; }
.mg-media-meta { max-width: 58rem; margin-top: 1rem; padding: .75rem 1rem; background: rgba(127,127,127,.035); }
.mg-media-meta-primary { font-size: .92rem; }
.mg-media-rating { margin-top: .5rem; }
.mg-media-tags { margin-top: .55rem; }
.mg-media-technical { margin-top: .55rem; }

.mg-album-default-grid .mg-card { transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.mg-album-default-grid .mg_thumbnail img { transition: transform .28s ease; }
.mg-album-default-grid .mg-card:hover, .mg-album-default-grid .mg-card:focus-within {
  transform: translateY(-.2rem); border-color: rgba(127,127,127,.32); box-shadow: 0 .55rem 1.5rem rgba(0,0,0,.1);
}
.mg-album-default-grid .mg-card:hover .mg_thumbnail img, .mg-album-default-grid .mg-card:focus-within .mg_thumbnail img { transform: scale(1.025); }
.mg-card-album-views { opacity: .68; font-size: .88rem; }

.mg-slideshow-play {
  display: inline-grid; place-items: center; width: 2.65rem; height: 2.65rem; min-width: 2.65rem;
  padding: 0; border-radius: 50%; font-size: 1.05rem;
}
.mg-slideshow-nav {
  width: min(20vw, 11rem); height: min(58vh, 31rem); border: 0; border-radius: 0;
  background: transparent; box-shadow: none; font-size: clamp(2.5rem,5vw,4.25rem); opacity: .78;
}
.mg-slideshow-prev { background: linear-gradient(90deg, rgba(5,8,14,.42), transparent); }
.mg-slideshow-next { background: linear-gradient(270deg, rgba(5,8,14,.42), transparent); }
.mg-slideshow-nav:hover, .mg-slideshow-nav:focus-visible { opacity: 1; }
.mg-slideshow-image { max-width: min(96vw, 100%); max-height: 94vh; }

@media (max-width: 42rem) {
  .mg-compact-search .mg_search { position: fixed; top: 4.25rem; right: 1rem; left: 1rem; width: auto; }
  .mg-media-actions { justify-content: center; gap: .65rem; }
  .mg-slideshow-nav { width: 24vw; height: 55vh; }
}
@media (prefers-reduced-motion: reduce) {
  .mg-album-default-grid .mg-card, .mg-album-default-grid .mg_thumbnail img { transition: none; transform: none !important; }
}
'''
    p.write_text(s, encoding='utf-8')

p = Path('ROADMAP.md')
s = p.read_text(encoding='utf-8')
line = '- [x] Final public visual polish: meaningful untitled-media fallback, zero-vote rating suppression, compact Search/Options UI, lighter metadata and immersive controls.\n'
if line not in s:
    p.write_text(s + '\n' + line, encoding='utf-8')
