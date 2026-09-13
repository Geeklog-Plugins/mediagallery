from pathlib import Path

# functions_legacy/lib-media may contain historical non-UTF-8 bytes.
lib_path = Path('include/lib-media.php')
lib = lib_path.read_text(encoding='latin-1')

old_desc = '''    $media_desc = PLG_replaceTags(nl2br($media['media_desc']));\n    if (strlen($media_desc) > 0) {\n        $media_desc = '<p style=\"margin:5px\">'.$media_desc.'</p>';\n    }\n'''
new_desc = '''    $media_desc = PLG_replaceTags(nl2br($media['media_desc']));\n'''
if lib.count(old_desc) != 1:
    raise SystemExit('Expected exactly one legacy media description wrapper')
lib = lib.replace(old_desc, new_desc)

old_kw = '''    $kwText = '';\n    $lang_keywords = '';\n    if ($mg_album->enable_keywords == 1 && !empty($media['media_keywords'])) {\n        $lang_keywords = $LANG_MG01['keywords'];\n        $keyWords = array();\n        $keyWords = explode(' ', $media['media_keywords']);\n        $numKeyWords = count($keyWords);\n        for ($i=0; $i<$numKeyWords; $i++) {\n            $keyWords[$i] = str_replace('\\\"', ' ', $keyWords[$i]);\n            $searchKeyword = $keyWords[$i];\n            $keyWords[$i] = str_replace('_', ' ', $keyWords[$i]);\n            $kwText .= '<a href=\"' . $_MG_CONF['site_url'] . '/search.php?mode=search&amp;swhere=1&amp;keywords=' . $searchKeyword . '&amp;keyType=any\">' . $keyWords[$i] . '</a>';\n        }\n    }\n'''
new_kw = '''    $kwText = '';\n    $lang_keywords = '';\n    if ($mg_album->enable_keywords == 1 && !empty($media['media_keywords'])) {\n        $lang_keywords = $LANG_MG01['keywords'];\n        $keyWords = preg_split('/[\\s,]+/', trim($media['media_keywords']));\n        if (!is_array($keyWords)) {\n            $keyWords = array();\n        }\n        foreach ($keyWords as $keyword) {\n            $keyword = trim(str_replace('\\\"', ' ', $keyword));\n            if ($keyword === '') {\n                continue;\n            }\n            $searchKeyword = rawurlencode($keyword);\n            $displayKeyword = MG_escapeHTML(str_replace('_', ' ', $keyword));\n            $kwText .= '<a class=\"mg-tag\" href=\"' . $_MG_CONF['site_url']\n                . '/search.php?mode=search&amp;swhere=1&amp;keywords=' . $searchKeyword\n                . '&amp;keyType=any\">' . $displayKeyword . '</a>';\n        }\n    }\n'''
if lib.count(old_kw) != 1:
    raise SystemExit('Expected exactly one legacy keyword builder')
lib = lib.replace(old_kw, new_kw)
lib_path.write_text(lib, encoding='latin-1')

view_path = Path('templates/view_image.thtml')
view = view_path.read_text(encoding='utf-8')
old_view = view
view = '''<!-- start view_image.thtml -->
{lbslideshow}
<nav class="bc_navigation" aria-label="Breadcrumb">{birdseed}</nav>
<header class="mg_album_header mg_media_header">
  <div class="mg_album_context">{album_title}{!if rsslink}&nbsp;{rsslink}{!endif}</div>
  <div class="mg_search">
    <form name="mgsearch" method="post" action="{site_url}/search.php" class="uk-form" role="search"><div>
      <label for="mg-media-search-keywords" class="mg-visually-hidden">{lang_search}</label>
      <input id="mg-media-search-keywords" type="search" name="keywords" value="{keywords}" aria-label="{lang_search}"{xhtml}>
      <input type="hidden" name="mode" value="search"{xhtml}>
      <input type="hidden" name="swhere" value="0"{xhtml}>
      <input type="submit" value="{lang_search}"{xhtml}>
    </div></form>
  </div>
</header>
<nav class="mg_navbar mg-media-toolbar" aria-label="Media actions and navigation">
  <div class="mg-media-pagination">
    {!if prev_link}<a class="button mg-action mg-action-prev" href="{prev_link}">&larr; {lang_prev}</a>{!endif}
    {!if pagination}<span class="mg-media-position" aria-label="{item_number} {lang_of} {total_items}">{item_number} / {total_items}</span>{!endif}
    {!if next_link}<a class="button mg-action mg-action-next" href="{next_link}">{lang_next} &rarr;</a>{!endif}
  </div>
  <div class="mg-media-actions">
    {!if url_slideshow}<a class="button mg-action" href="{url_slideshow}"{slideshow_onclick}>{lang_slideshow}</a>{!endif}
    {!if download_link}<a class="button mg-action" href="{download_link}">{lang_download}</a>{!endif}
    {!if property}<a class="button mg-action" href="{property}" onclick="return popitup(this.href)">{lang_property}</a>{!endif}
    {!if switch_size}<a class="button mg-action" href="{switch_size}">{lang_switch_size}</a>{!endif}
    {!if edit_item_link}<a class="button mg-action mg-action-admin" href="{edit_item_link}">{lang_edit}</a>{!endif}
  </div>
</nav>
<article class="mg-media-article">
  <header class="mg-media-article-header">
    <h1 class="mg_media_title">{!if media_title}{media_title}{!else}{album_title}{!endif}</h1>
  </header>
  <figure class="mg-media-figure">
    <div class="mg_media_detail">{image_detail}</div>
    {!if media_desc}<figcaption class="mg_media_desc">{media_desc}</figcaption>{!endif}
  </figure>
  <footer class="mg-media-meta">
    <div class="mg-media-meta-primary">
      <span class="mg-media-author"><strong>{lang_uploaded_by}:</strong>&nbsp;{owner_username}</span>
      <span class="mg-media-date">{media_time}</span>
      <span class="mg-media-views">{lang_views} {media_views}</span>
    </div>
    {!if rating_box}<div class="mg-media-rating">{rating_box}</div>{!endif}
    {!if media_keywords}
    <div class="mg-media-tags">
      <strong class="mg-media-tags-label">{lang_keywords}</strong>
      <span class="mg-tag-list">{media_keywords}</span>
    </div>
    {!endif}
    {!if edit_item_link}
    <details class="mg-media-technical">
      <summary>Media ID</summary>
      <code>{media_id}</code>
      {!if media_properties}<div class="mg-media-properties">{getid3}{media_properties}{getid3end}</div>{!endif}
    </details>
    {!else}
      {!if media_properties}<div class="mg-media-properties">{getid3}{media_properties}{getid3end}</div>{!endif}
    {!endif}
    {!if exif_info}<div class="mg_exif_info">{exif_info}</div>{!endif}
  </footer>
</article>
{!if jumpbox}<div class="mg_jumpbox">{jumpbox}</div>{!endif}
<script type="text/javascript">
//<![CDATA[
function popitup(url)
{
    var newwindow = window.open(url,'name','height=600,width=450,resizable=yes,toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes');
    if (window.focus) {newwindow.focus()}
    return false;
}
//]]>
</script>
'''
if old_view == view:
    raise SystemExit('view_image.thtml already modernized unexpectedly')
view_path.write_text(view, encoding='utf-8')

css_path = Path('public_html/style.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 media detail modernization */'
if marker in css:
    raise SystemExit('Media detail CSS marker already exists')
css += r'''

/* MediaGallery 1.8 media detail modernization */
.mg_media_header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.mg_media_header .mg_album_context {
  min-width: 0;
  font-weight: 600;
}

.mg_media_header .mg_search {
  margin-left: auto;
}

.mg_media_header .mg_search form > div {
  display: flex;
  align-items: center;
  gap: .45rem;
}

.mg_media_header .mg_search input[type="search"] {
  min-width: min(18rem, 55vw);
  max-width: 100%;
}

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
.mg-media-actions {
  display: flex;
  align-items: center;
  gap: .4rem;
  flex-wrap: wrap;
}

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

.mg_navbar a.button.mg-action-admin {
  font-weight: 600;
}

.mg-media-article {
  width: 100%;
  max-width: 70rem;
  margin: 0 auto;
}

.mg-media-article-header {
  text-align: center;
}

.mg-media-article .mg_media_title {
  margin: 0 0 1rem;
  min-height: 0;
  line-height: 1.25;
  font-size: clamp(1.45rem, 2vw + .75rem, 2.15rem);
  overflow-wrap: anywhere;
}

.mg-media-figure {
  margin: 0;
  text-align: center;
}

.mg-media-figure .mg_media_detail {
  margin: 0 auto;
}

.mg-media-figure .mg_media_detail img,
.mg-media-figure video,
.mg-media-figure audio,
.mg-media-figure iframe {
  max-width: 100%;
}

.mg-media-figure .mg_media_detail img,
.mg-media-figure video {
  height: auto;
}

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

.mg-media-meta-primary > span {
  overflow-wrap: anywhere;
}

.mg-media-rating {
  margin-top: .75rem;
  text-align: center;
}

.mg-media-rating .ratingblock {
  margin-inline: auto;
}

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
.mg-tag:focus-visible {
  text-decoration: underline;
}

.mg-media-technical {
  max-width: 44rem;
  margin: .85rem auto 0;
  text-align: center;
}

.mg-media-technical summary {
  cursor: pointer;
  font-size: .9em;
}

.mg-media-technical code {
  display: inline-block;
  margin-top: .35rem;
  overflow-wrap: anywhere;
}

.mg-media-properties,
.mg_exif_info {
  margin-top: .75rem;
}

@media (max-width: 640px) {
  .mg_media_header,
  .mg-media-toolbar {
    align-items: stretch;
  }

  .mg_media_header .mg_search,
  .mg_media_header .mg_search form,
  .mg_media_header .mg_search form > div,
  .mg-media-pagination,
  .mg-media-actions {
    width: 100%;
  }

  .mg_media_header .mg_search input[type="search"] {
    flex: 1 1 10rem;
    min-width: 0;
  }

  .mg-media-pagination {
    justify-content: space-between;
  }

  .mg-media-actions {
    justify-content: center;
  }

  .mg-media-pagination .mg-action {
    flex: 1 1 0;
    text-align: center;
  }

  .mg-media-meta-primary {
    flex-direction: column;
    gap: .3rem;
  }
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

print('Modernized default MediaGallery media detail page')
