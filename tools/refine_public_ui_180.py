from pathlib import Path

# classMedia.php: respect Geeklog shortdate configuration
p = Path('include/classMedia.php')
s = p.read_text(encoding='utf-8')
old = "$media_date_short = COM_strftime('%d %b %Y', $media_time[1]);"
new = "$media_date_short = COM_strftime(isset($_CONF['shortdate']) ? $_CONF['shortdate'] : '%x', $media_time[1]);"
if old not in s:
    raise SystemExit('short date marker not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# Root/subalbum cards: visual-first, no verbose updated date
p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('<h2 class="mg_album_item_title mg-card-title">{lang_album} {album_title} <span class="mg_item_count">({subalbum_media_count})</span></h2>', '<h2 class="mg_album_item_title mg-card-title">{album_title} <span class="mg_item_count" aria-label="Media count">{subalbum_media_count}</span></h2>')
s = s.replace('      {!if updated}<span><strong>{updated}</strong> {album_last_update}</span>{!endif}\n', '')
p.write_text(s, encoding='utf-8')

# Media toolbar: remove legacy button styling and make actions semantically distinct
p = Path('templates/view_image.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('class="button mg-action mg-action-prev"', 'class="mg-action mg-action-nav mg-action-prev"')
s = s.replace('class="button mg-action mg-action-next"', 'class="mg-action mg-action-nav mg-action-next"')
s = s.replace('class="button mg-action"', 'class="mg-action mg-action-secondary"')
s = s.replace('class="button mg-action mg-action-admin"', 'class="mg-action mg-action-secondary mg-action-admin"')
p.write_text(s, encoding='utf-8')

# CSS refinements
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 public UI refinement */'
if marker not in s:
    s += r'''

/* MediaGallery 1.8 public UI refinement */
.mg-album-default-grid .mg_album_item .mg-card-body {
  padding-top: .72rem;
}

.mg-album-default-grid .mg_album_item .mg-card-title {
  margin-bottom: .35rem;
}

.mg-album-default-grid .mg_item_count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.55rem;
  min-height: 1.55rem;
  margin-left: .25rem;
  padding: 0 .35rem;
  border-radius: 999px;
  background: rgba(127, 127, 127, .12);
  font-size: .78em;
  font-weight: 600;
  vertical-align: middle;
}

.mg-album-default-grid .mg-card-meta-album {
  margin-top: .2rem;
  opacity: .78;
}

.mg-media-toolbar {
  max-width: 70rem;
  margin: .55rem auto 1rem;
  padding: .25rem 0;
  background: transparent;
}

.mg-media-pagination,
.mg-media-actions {
  gap: .3rem;
}

.mg-media-toolbar .mg-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 1.9rem;
  margin: 0;
  padding: .22rem .48rem;
  border: 0;
  border-radius: .35rem;
  background: transparent;
  box-shadow: none;
  color: inherit;
  font-size: .82rem;
  line-height: 1.2;
  text-decoration: none;
}

.mg-media-toolbar .mg-action:hover,
.mg-media-toolbar .mg-action:focus-visible {
  background: rgba(127, 127, 127, .1);
  text-decoration: underline;
}

.mg-media-toolbar .mg-action-nav {
  border: 1px solid rgba(127, 127, 127, .22);
}

.mg-media-toolbar .mg-action-secondary {
  opacity: .78;
}

.mg-media-toolbar .mg-action-admin {
  opacity: .9;
  font-weight: 600;
}

.mg-media-position {
  min-width: 3.2rem;
  min-height: 1.9rem;
  padding: .15rem .35rem;
  font-size: .88rem;
}

.mg-album-page-header .mg_adminbox input[type="submit"],
.mg-album-secondary-controls input[type="submit"] {
  opacity: .68;
  box-shadow: none;
}

.mg-album-page-header .mg_adminbox input[type="submit"]:hover,
.mg-album-page-header .mg_adminbox input[type="submit"]:focus-visible,
.mg-album-secondary-controls input[type="submit"]:hover,
.mg-album-secondary-controls input[type="submit"]:focus-visible {
  opacity: 1;
}

@media (max-width: 640px) {
  .mg-media-toolbar {
    gap: .35rem;
  }
  .mg-media-actions {
    justify-content: flex-start;
  }
  .mg-media-toolbar .mg-action-secondary {
    flex: 0 0 auto;
  }
}
'''
p.write_text(s, encoding='utf-8')

# Roadmap note
p = Path('ROADMAP.md')
s = p.read_text(encoding='utf-8')
needle = '- [x] Modernize the default album page with centered auto-fit cards, compact metadata, unified controls and a responsive footer.\n'
addition = '- [x] Refine Root Album and media-detail controls: use Geeklog short-date formatting, lighter subalbum cards and compact media actions.\n'
if addition not in s:
    if needle not in s:
        raise SystemExit('roadmap insertion marker not found')
    s = s.replace(needle, needle + addition, 1)
p.write_text(s, encoding='utf-8')
