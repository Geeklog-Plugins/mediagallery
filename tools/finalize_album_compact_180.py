from pathlib import Path

# classMedia.php: expose a compact, user-timezone-aware date for album cards.
path = Path('include/classMedia.php')
text = path.read_text(encoding='utf-8')
old = """        if ($_MG_CONF['use_upload_time'] == 1) {
            $media_time = MG_getUserDateTimeFormat($this->upload_time);
        } else {
            $media_time = MG_getUserDateTimeFormat($this->time);
        }

        $media_title = (!empty($this->title)) ? PLG_replaceTags($this->title) : 'No Name';
"""
new = """        if ($_MG_CONF['use_upload_time'] == 1) {
            $media_time = MG_getUserDateTimeFormat($this->upload_time);
        } else {
            $media_time = MG_getUserDateTimeFormat($this->time);
        }
        $media_date_short = COM_strftime('%d %b %Y', $media_time[1]);

        $media_title = (!empty($this->title)) ? PLG_replaceTags($this->title) : 'No Name';
"""
if old not in text:
    raise SystemExit('media time block not found')
text = text.replace(old, new, 1)
old = "            'media_time'        => $media_time[0],\n"
new = "            'media_time'        => $media_time[0],\n            'media_date_short'  => $media_date_short,\n"
if old not in text:
    raise SystemExit('media_time template variable not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')

# CSS: reduce visual weight on album list pages only.
css_path = Path('public_html/style.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 compact album cards */'
if marker not in css:
    css += r'''

/* MediaGallery 1.8 compact album cards */
.mg-album-page-header {
  margin-bottom: .35rem;
}
.mg-album-heading {
  display: flex;
  align-items: baseline;
  gap: .5rem 1rem;
  flex-wrap: wrap;
}
.mg-album-inline-actions {
  display: inline-flex;
  align-items: center;
  gap: .75rem;
  font-size: .88rem;
  line-height: 1.3;
}
.mg-album-inline-actions a {
  color: inherit;
  opacity: .72;
  text-decoration: none;
  border-bottom: 1px solid transparent;
}
.mg-album-inline-actions a:hover,
.mg-album-inline-actions a:focus-visible {
  opacity: 1;
  border-bottom-color: currentColor;
}
.mg-album-admin-action::before {
  content: "\00b7";
  margin-right: .75rem;
  opacity: .6;
}
.mg-album-top-pagination {
  display: flex;
  justify-content: flex-end;
  margin: .35rem 0;
}

.mg-card-compact .mg-card-body {
  padding-top: .75rem;
  padding-bottom: .85rem;
}
.mg-card-compact .mg-card-title {
  margin-bottom: .55rem;
}
.mg-card-meta-compact {
  gap: .3rem .55rem;
  font-size: .84rem;
  opacity: .78;
}
.mg-card-meta-compact > span + span::before {
  content: "\00b7";
  margin-right: .55rem;
  opacity: .65;
}
.mg-card-compact .mg-card-edit {
  margin-top: .55rem;
  font-size: .82rem;
  opacity: .7;
}

.mg-album-footer-compact {
  margin-top: 1rem;
  padding-top: .65rem;
  border-top: 1px solid rgba(127, 127, 127, .18);
}
.mg-album-footer-compact .mg-album-pagination-bar {
  background: transparent;
  padding: 0;
}
.mg-album-footer-compact .mg-album-page-info {
  font-size: .9rem;
  opacity: .75;
}
.mg-secondary-control {
  font-size: .9rem;
}
.mg-secondary-control form > div {
  display: flex;
  align-items: center;
  gap: .4rem;
}
.mg-secondary-control input[type="submit"] {
  min-height: 2rem;
  padding: .25rem .55rem;
  font-size: .82rem;
  font-weight: 500;
  opacity: .72;
  filter: saturate(.45);
}
.mg-secondary-control input[type="submit"]:hover,
.mg-secondary-control input[type="submit"]:focus-visible {
  opacity: 1;
  filter: none;
}
.mg-secondary-control select {
  min-height: 2rem;
  padding-block: .2rem;
}

@media (max-width: 48rem) {
  .mg-album-heading {
    align-items: flex-start;
    flex-direction: column;
    gap: .25rem;
  }
  .mg-album-admin-action::before {
    display: none;
  }
  .mg-album-secondary-controls {
    gap: .5rem;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

# Roadmap: record the UX simplification and current automatic archive behavior.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
needle = '- [x] Modernize the default album page with centered auto-fit cards, compact metadata, unified controls and a responsive footer.\n'
addition = '- [x] Simplify default album cards to title, short date, views/comments only; keep rating, tags and technical detail on media-detail pages.\n'
if addition not in roadmap:
    if needle not in roadmap:
        raise SystemExit('roadmap album marker not found')
    roadmap = roadmap.replace(needle, needle + addition, 1)
roadmap = roadmap.replace(
    '- [x] Keep archive generation intentional rather than rebuilding after every source commit.\n',
    '- [x] Rebuild the test archive automatically after every validated branch change, excluding `dist/**` to prevent loops.\n'
)
roadmap_path.write_text(roadmap, encoding='utf-8')
print('Compact album finalization applied')
