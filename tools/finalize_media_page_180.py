from pathlib import Path
import re

lib_path = Path('include/lib-media.php')
lib = lib_path.read_text(encoding='latin-1')

lib, n = re.subn(
    r"\n\s*\$media_desc = PLG_replaceTags\(nl2br\(\$media\['media_desc'\]\)\);\n\s*if \(strlen\(\$media_desc\) > 0\) \{\n\s*\$media_desc = '<p style=\\\"margin:5px\\\">'\.\$media_desc\.'</p>';\n\s*\}\n",
    "\n    $media_desc = PLG_replaceTags(nl2br($media['media_desc']));\n",
    lib,
    count=1,
)
if n != 1:
    raise SystemExit('Could not replace legacy description wrapper')

pattern = re.compile(
    r"    \$kwText = '';\n    \$lang_keywords = '';\n.*?\n    \$media_user_id = \$media\['media_user_id'\];",
    re.S,
)
replacement = """    $kwText = '';
    $lang_keywords = '';
    if ($mg_album->enable_keywords == 1 && !empty($media['media_keywords'])) {
        $lang_keywords = $LANG_MG01['keywords'];
        $keyWords = preg_split('/[\\s,]+/', trim($media['media_keywords']));
        if (!is_array($keyWords)) {
            $keyWords = array();
        }
        foreach ($keyWords as $keyword) {
            $keyword = trim(str_replace('\\\"', ' ', $keyword));
            if ($keyword === '') {
                continue;
            }
            $searchKeyword = rawurlencode($keyword);
            $displayKeyword = MG_escapeHTML(str_replace('_', ' ', $keyword));
            $kwText .= '<a class=\"mg-tag\" href=\"' . $_MG_CONF['site_url']
                . '/search.php?mode=search&amp;swhere=1&amp;keywords=' . $searchKeyword
                . '&amp;keyType=any\">' . $displayKeyword . '</a>';
        }
    }

    $media_user_id = $media['media_user_id'];"""
lib, n = pattern.subn(replacement, lib, count=1)
if n != 1:
    raise SystemExit('Could not replace keyword builder')
lib_path.write_text(lib, encoding='latin-1')

css_path = Path('public_html/style.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 media detail modernization */'
if marker not in css:
    css += r'''

/* MediaGallery 1.8 media detail modernization */
.mg_media_header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}
.mg_media_header .mg_album_context { min-width: 0; font-weight: 600; }
.mg_media_header .mg_search { margin-left: auto; }
.mg_media_header .mg_search form > div { display: flex; align-items: center; gap: .45rem; }
.mg_media_header .mg_search input[type="search"] { min-width: min(18rem, 55vw); max-width: 100%; }

.mg-media-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .75rem 1rem;
  flex-wrap: wrap;
  margin: .75rem 0 1.25rem;
  padding: .65rem .75rem;
}
.mg-media-pagination,
.mg-media-actions { display: flex; align-items: center; gap: .4rem; flex-wrap: wrap; }
.mg-media-position {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 3.75rem;
  min-height: 2.15rem;
  padding: .2rem .55rem;
  font-weight: 600;
  white-space: nowrap;
}
.mg_navbar a.button.mg-action {
  margin: 0;
  padding: .42rem .7rem;
  line-height: 1.25;
  border-radius: .35rem;
}
.mg_navbar a.button.mg-action-admin { font-weight: 600; }

.mg-media-article { width: 100%; max-width: 70rem; margin: 0 auto; }
.mg-media-article-header { text-align: center; }
.mg-media-article .mg_media_title {
  margin: 0 0 1rem;
  min-height: 0;
  line-height: 1.25;
  font-size: clamp(1.45rem, 2vw + .75rem, 2.15rem);
  overflow-wrap: anywhere;
}
.mg-media-figure { margin: 0; text-align: center; }
.mg-media-figure .mg_media_detail { margin: 0 auto; }
.mg-media-figure .mg_media_detail img,
.mg-media-figure video,
.mg-media-figure audio,
.mg-media-figure iframe { max-width: 100%; }
.mg-media-figure .mg_media_detail img,
.mg-media-figure video { height: auto; }
.mg-media-figure .mg_media_desc {
  max-width: 65ch;
  margin: .75rem auto 0;
  padding: 0 1rem;
  min-height: 0;
  line-height: 1.55;
  text-align: center;
  overflow-wrap: anywhere;
}

.mg-media-meta {
  margin: 1.25rem auto 1.5rem;
  padding: 1rem;
  border: 1px solid rgba(127, 127, 127, .22);
  border-radius: .65rem;
  background: rgba(127, 127, 127, .055);
}
.mg-media-meta-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .35rem 1rem;
  flex-wrap: wrap;
  text-align: center;
}
.mg-media-meta-primary > span { overflow-wrap: anywhere; }
.mg-media-rating { margin-top: .75rem; text-align: center; }
.mg-media-rating .ratingblock { margin-inline: auto; }
.mg-media-tags {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  flex-wrap: wrap;
  margin-top: .75rem;
}
.mg-tag-list {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .35rem;
  flex-wrap: wrap;
}
.mg-tag {
  display: inline-flex;
  align-items: center;
  min-height: 1.85rem;
  padding: .18rem .55rem;
  border: 1px solid currentColor;
  border-radius: 999px;
  text-decoration: none;
  line-height: 1.25;
}
.mg-tag:hover,
.mg-tag:focus-visible { text-decoration: underline; }
.mg-media-technical { max-width: 44rem; margin: .85rem auto 0; text-align: center; }
.mg-media-technical summary { cursor: pointer; font-size: .9em; }
.mg-media-technical code { display: inline-block; margin-top: .35rem; overflow-wrap: anywhere; }
.mg-media-properties,
.mg_exif_info { margin-top: .75rem; }

@media (max-width: 640px) {
  .mg_media_header,
  .mg-media-toolbar { align-items: stretch; }
  .mg_media_header .mg_search,
  .mg_media_header .mg_search form,
  .mg_media_header .mg_search form > div,
  .mg-media-pagination,
  .mg-media-actions { width: 100%; }
  .mg_media_header .mg_search input[type="search"] { flex: 1 1 10rem; min-width: 0; }
  .mg-media-pagination { justify-content: space-between; }
  .mg-media-actions { justify-content: center; }
  .mg-media-pagination .mg-action { flex: 1 1 0; text-align: center; }
  .mg-media-meta-primary { flex-direction: column; gap: .3rem; }
}
'''
css_path.write_text(css, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
needle = '- [x] Complete final public markup audit: one H1 per Podcast page, semantic repeated-card headings, non-link anchors and table-free member enrollment.\n'
addition = '- [x] Modernize the default media-detail page with semantic article/figure markup, separated navigation/actions, compact metadata and normalized keyword tags.\n'
if addition not in roadmap:
    if needle not in roadmap:
        raise SystemExit('ROADMAP insertion point not found')
    roadmap = roadmap.replace(needle, needle + addition)
    roadmap_path.write_text(roadmap, encoding='utf-8')

print('Finalized MediaGallery media detail modernization')
